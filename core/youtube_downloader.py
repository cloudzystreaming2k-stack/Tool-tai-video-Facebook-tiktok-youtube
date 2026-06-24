import os
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

class YoutubeDownloader(BaseDownloader):
    def get_video_info(self) -> dict:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ffmpeg_location': _get_ffmpeg_path(),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            formats = []
            seen_resolutions = set()
            sorted_formats = sorted(info.get('formats', []), key=lambda x: x.get('height') or 0, reverse=True)
            for f in sorted_formats:
                if f.get('vcodec') != 'none':
                    height = f.get('height')
                    if height and height not in seen_resolutions:
                        if height in [360, 480, 720, 1080, 1440, 2160]:
                            seen_resolutions.add(height)
                            fid = f['format_id']
                            # Prefer m4a (AAC) audio - compatible with all players.
                            # Fallback to bestaudio if m4a is unavailable.
                            audio_selector = 'bestaudio[ext=m4a]/bestaudio[acodec=aac]/bestaudio'
                            formats.append({
                                'format_id': f"{fid}+{audio_selector}",
                                'resolution': f"{height}p",
                                'ext': 'mp4',
                                'filesize': f.get('filesize') or f.get('filesize_approx') or 0
                            })
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': formats,
                'platform': 'YouTube'
            }

    def _download(self, ydl_opts, progress_hook=None) -> str:
        FileManager.create_directory(self.download_path)

        if progress_hook:
            ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            # For merged formats, prepare_filename may return the intermediate name.
            # Use the outtmpl pattern with merge_output_format instead.
            filename = ydl.prepare_filename(info)
            # If merge_output_format was set to mp4, ensure the returned path has .mp4
            merge_format = ydl_opts.get('merge_output_format')
            if merge_format:
                base = os.path.splitext(filename)[0]
                filename = base + '.' + merge_format
            return filename

    def download_video(self, format_id: str, progress_hook=None) -> str:
        outtmpl = os.path.join(self.download_path, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': format_id,
            'merge_output_format': 'mp4',
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': _get_ffmpeg_path(),
            # Force AAC audio re-encode so mp4 is compatible with all media players.
            # This handles the case where bestaudio fallback picks Opus (not supported in mp4).
            'postprocessor_args': {
                'merger': ['-c:v', 'copy', '-c:a', 'aac']
            },
        }
        return self._download(ydl_opts, progress_hook)
        
    def download_audio(self, progress_hook=None) -> str:
        outtmpl = os.path.join(self.download_path, '%(title)s.%(ext)s')
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
