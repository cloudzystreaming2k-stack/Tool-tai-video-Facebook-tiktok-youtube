import os
import datetime
import yt_dlp
from core.base_downloader import BaseDownloader
from services.file_manager import FileManager


def _get_ffmpeg_path() -> str:
    """Return FFmpeg executable path from imageio-ffmpeg if available."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'  # Fall back to system PATH


class TikTokDownloader(BaseDownloader):
    """Downloader for TikTok videos using yt-dlp."""

    def get_video_info(self) -> dict:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ffmpeg_location': _get_ffmpeg_path(),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)

            # TikTok videos typically have a single quality.
            # Collect unique resolutions available.
            formats = []
            seen_resolutions = set()
            sorted_formats = sorted(
                info.get('formats', []),
                key=lambda x: x.get('height') or 0,
                reverse=True
            )
            for f in sorted_formats:
                vcodec = f.get('vcodec', '') or ''
                acodec = f.get('acodec', '') or ''
                if vcodec.lower() not in ('none', '') and acodec.lower() not in ('none', ''):
                    # Skip HEVC/H.265 to ensure compatibility with standard Windows Media Player
                    if 'hevc' in vcodec.lower() or 'hvc' in vcodec.lower() or '265' in vcodec.lower():
                        continue
                        
                    height = f.get('height')
                    if height and height not in seen_resolutions:
                        seen_resolutions.add(height)
                        formats.append({
                            'format_id': f['format_id'],
                            'resolution': f"{height}p",
                            'ext': f.get('ext', 'mp4'),
                            'filesize': f.get('filesize') or f.get('filesize_approx') or 0
                        })

            # Fallback: if no combined format, expose a single "best" option preferring H.264
            if not formats:
                formats.append({
                    'format_id': 'bestvideo[vcodec*=avc]+bestaudio/best[vcodec*=avc]/best',
                    'resolution': 'Best Available',
                    'ext': 'mp4',
                    'filesize': 0
                })

            return {
                'title': info.get('title') or info.get('description', 'TikTok Video'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': formats,
                'platform': 'TikTok'
            }

    def _download(self, ydl_opts: dict, progress_hook=None) -> str:
        FileManager.create_directory(self.download_path)

        if progress_hook:
            ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)
            merge_format = ydl_opts.get('merge_output_format')
            if merge_format:
                base = os.path.splitext(filename)[0]
                filename = base + '.' + merge_format
            return filename

    def download_video(self, format_id: str, progress_hook=None) -> str:
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        outtmpl = os.path.join(self.download_path, f'TikTok_{now_str}.%(ext)s')
        ydl_opts = {
            'format': format_id,
            'merge_output_format': 'mp4',
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': _get_ffmpeg_path(),
            # Re-encode audio to AAC for universal compatibility
            'postprocessor_args': {
                'merger': ['-c:v', 'copy', '-c:a', 'aac']
            },
        }
        return self._download(ydl_opts, progress_hook)

    def download_audio(self, progress_hook=None) -> str:
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        outtmpl = os.path.join(self.download_path, f'TikTok_{now_str}.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': _get_ffmpeg_path(),
        }
        return self._download(ydl_opts, progress_hook)
