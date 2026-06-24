from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt
from gui.pages.download_page import DownloadPage
from gui.pages.history_page import HistoryPage
from gui.pages.settings_page import SettingsPage
from services.download_manager import DownloadManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Media Downloader")
        self.resize(900, 600)
        
        self.download_manager = DownloadManager()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setStyleSheet("background-color: #f5f6fa;")
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2f3640;
                color: #f5f6fa;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 15px 25px;
                text-align: left;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #353b48;
            }
            QPushButton:checked {
                background-color: #00a8ff;
                border-left: 4px solid #fff;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 0)
        sidebar_layout.setSpacing(5)
        
        self.btn_youtube = QPushButton("▶ YouTube")
        self.btn_youtube.setCheckable(True)
        self.btn_youtube.setChecked(True)
        self.btn_tiktok = QPushButton("🎵 TikTok")
        self.btn_tiktok.setCheckable(True)
        self.btn_facebook = QPushButton("📘 Facebook")
        self.btn_facebook.setCheckable(True)
        self.btn_history = QPushButton("🕒 History")
        self.btn_history.setCheckable(True)
        self.btn_settings = QPushButton("⚙ Settings")
        self.btn_settings.setCheckable(True)
        
        sidebar_layout.addWidget(self.btn_youtube)
        sidebar_layout.addWidget(self.btn_tiktok)
        sidebar_layout.addWidget(self.btn_facebook)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()
        
        # Main Content Area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #ffffff;")
        
        self.page_youtube = DownloadPage(self.download_manager, platform_filter="youtube", page_title="YouTube Downloader")
        self.page_tiktok = DownloadPage(self.download_manager, platform_filter="tiktok", page_title="TikTok Downloader")
        self.page_facebook = DownloadPage(self.download_manager, platform_filter="facebook", page_title="Facebook Downloader")
        self.page_history = HistoryPage()
        self.page_settings = SettingsPage()
        
        self.stacked_widget.addWidget(self.page_youtube)
        self.stacked_widget.addWidget(self.page_tiktok)
        self.stacked_widget.addWidget(self.page_facebook)
        self.stacked_widget.addWidget(self.page_history)
        self.stacked_widget.addWidget(self.page_settings)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        self.setCentralWidget(central_widget)
        
        # Connections
        self.btn_youtube.clicked.connect(lambda: self.switch_page(0))
        self.btn_tiktok.clicked.connect(lambda: self.switch_page(1))
        self.btn_facebook.clicked.connect(lambda: self.switch_page(2))
        self.btn_history.clicked.connect(lambda: self.switch_page(3))
        self.btn_settings.clicked.connect(lambda: self.switch_page(4))

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_youtube.setChecked(index == 0)
        self.btn_tiktok.setChecked(index == 1)
        self.btn_facebook.setChecked(index == 2)
        self.btn_history.setChecked(index == 3)
        self.btn_settings.setChecked(index == 4)
        
        if index == 3:
            self.page_history.load_data()
