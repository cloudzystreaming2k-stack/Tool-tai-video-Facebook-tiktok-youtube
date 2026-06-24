import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from services.file_manager import FileManager, DEFAULT_SETTINGS_PATH

def main():
    # Ensure default settings and directories exist
    FileManager.ensure_default_settings(DEFAULT_SETTINGS_PATH)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
