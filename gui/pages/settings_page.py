from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFormLayout
from services.file_manager import FileManager, DEFAULT_SETTINGS_PATH
import os

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_file = DEFAULT_SETTINGS_PATH
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Download path
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setStyleSheet("padding: 8px;")
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setStyleSheet("padding: 8px 15px;")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        
        label_path = QLabel("Download Path:")
        label_path.setStyleSheet("font-size: 14px;")
        form_layout.addRow(label_path, path_layout)
        
        layout.addLayout(form_layout)
        
        # Save button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #2980b9; color: white;")
        self.save_btn.clicked.connect(self.save_settings)
        
        save_layout = QHBoxLayout()
        save_layout.addWidget(self.save_btn)
        save_layout.addStretch()
        
        layout.addLayout(save_layout)
        layout.addStretch()
        
        self.setLayout(layout)

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.path_input.text())
        if folder:
            self.path_input.setText(folder)

    def load_settings(self):
        settings = FileManager.load_json(self.settings_file)
        if settings:
            self.path_input.setText(settings.get("download_path", ""))

    def save_settings(self):
        settings = FileManager.load_json(self.settings_file)
        settings["download_path"] = self.path_input.text()
        FileManager.save_json(self.settings_file, settings)
        QMessageBox.information(self, "Success", "Settings saved successfully!")
