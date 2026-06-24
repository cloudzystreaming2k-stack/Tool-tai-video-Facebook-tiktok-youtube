from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
from services.url_parser import URLParser
from core.youtube_downloader import YoutubeDownloader
from core.tiktok_downloader import TikTokDownloader
from core.facebook_downloader import FacebookDownloader
from services.file_manager import FileManager, DEFAULT_SETTINGS_PATH

SUPPORTED_PLATFORMS = {'youtube', 'tiktok', 'facebook'}

def _create_downloader(url: str, platform: str, download_path: str):
    """Factory: return the correct downloader for the detected platform."""
    if platform == 'youtube':
        return YoutubeDownloader(url, download_path)
    elif platform == 'tiktok':
        return TikTokDownloader(url, download_path)
    elif platform == 'facebook':
        return FacebookDownloader(url, download_path)
    # Fallback: attempt with YoutubeDownloader (yt-dlp handles many sites)
    return YoutubeDownloader(url, download_path)

class DownloadPage(QWidget):
    def __init__(self, download_manager, platform_filter: str, page_title: str):
        super().__init__()
        self.download_manager = download_manager
        self.platform_filter = platform_filter
        self.page_title = page_title
        self.current_downloader = None
        self.current_video_info = None
        self.current_platform = 'unknown'
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title_label = QLabel(self.page_title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # URL Input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(f"Enter {self.page_title} URL")
        self.url_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.fetch_btn = QPushButton("Fetch Info")
        self.fetch_btn.setStyleSheet("padding: 8px 15px; font-size: 14px;")
        self.fetch_btn.clicked.connect(self.on_fetch_clicked)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.fetch_btn)
        layout.addLayout(url_layout)

        # Video Info display
        self.info_label = QLabel("No video loaded.")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(self.info_label)

        # Quality selection
        self.format_combo = QComboBox()
        self.format_combo.setEnabled(False)
        self.format_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.format_combo)

        # Download button
        self.download_btn = QPushButton("Download")
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #27ae60; color: white; font-weight: bold;")
        self.download_btn.clicked.connect(self.on_download_clicked)
        layout.addWidget(self.download_btn)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("QProgressBar { border: 1px solid #ccc; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #3498db; }")
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 13px; color: #666;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)

    def on_fetch_clicked(self):
        url = self.url_input.text().strip()
        if not url or not URLParser.is_valid_url(url):
            QMessageBox.warning(self, "Error", "Invalid URL")
            return

        platform = URLParser.detect_platform(url)
        self.current_platform = platform

        if platform != self.platform_filter:
            QMessageBox.warning(
                self, "Unsupported URL",
                f"Please enter a valid {self.platform_filter.capitalize()} URL for this page."
            )
            return

        # Create downloader with path from settings
        settings = FileManager.load_json(DEFAULT_SETTINGS_PATH)
        download_path = settings.get("download_path", "")

        self.current_downloader = _create_downloader(url, platform, download_path)

        self.fetch_btn.setEnabled(False)
        self.fetch_btn.setText("Fetching...")
        self.info_label.setText(f"Fetching {platform.capitalize()} video information...")
        self.format_combo.clear()
        self.format_combo.setEnabled(False)
        self.download_btn.setEnabled(False)

        self.download_manager.fetch_info(
            self.current_downloader,
            on_finished=self.on_info_fetched,
            on_error=self.on_fetch_error
        )

    def on_info_fetched(self, info):
        self.current_video_info = info
        self.fetch_btn.setEnabled(True)
        self.fetch_btn.setText("Fetch Info")
        
        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        mins, secs = divmod(duration, 60)
        self.info_label.setText(f"<b>Title:</b> {title}<br><b>Duration:</b> {mins}m {secs}s")
        
        self.format_combo.clear()
        self.format_combo.addItem("Audio Only (MP3)", "audio")
        
        for f in info.get('formats', []):
            res = f.get('resolution')
            ext = f.get('ext')
            fid = f.get('format_id')
            self.format_combo.addItem(f"Video: {res} ({ext})", fid)
            
        self.format_combo.setEnabled(True)
        self.download_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready.")

    def on_fetch_error(self, err):
        self.fetch_btn.setEnabled(True)
        self.fetch_btn.setText("Fetch Info")
        self.info_label.setText("Error fetching info.")
        QMessageBox.critical(self, "Error", f"Failed to fetch video info:\n{err}")

    def on_download_clicked(self):
        if not self.current_downloader or not self.current_video_info:
            return
            
        data = self.format_combo.currentData()
        is_audio = (data == "audio")
        format_id = None if is_audio else data
        
        title = self.current_video_info.get('title', 'Unknown')
        
        self.download_btn.setEnabled(False)
        self.fetch_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting download...")
        
        self.download_manager.start_download(
            self.current_downloader,
            video_title=title,
            platform=self.current_platform,
            format_id=format_id,
            is_audio=is_audio,
            on_progress=self.on_download_progress,
            on_finished=self.on_download_finished,
            on_error=self.on_download_error
        )

    def on_download_progress(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = int(downloaded * 100 / total)
                self.progress_bar.setValue(percent)
            
            speed = d.get('speed', 0)
            if speed:
                speed_mb = speed / 1024 / 1024
                self.status_label.setText(f"Downloading... Speed: {speed_mb:.2f} MB/s")
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            self.status_label.setText("Processing finished (Merging/Converting)...")

    def on_download_finished(self, file_path):
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)
        self.status_label.setText(f"Downloaded successfully: {file_path}")
        QMessageBox.information(self, "Success", "Download completed successfully!")

    def on_download_error(self, err):
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)
        self.status_label.setText("Download failed.")
        QMessageBox.critical(self, "Error", f"Download failed:\n{err}")
