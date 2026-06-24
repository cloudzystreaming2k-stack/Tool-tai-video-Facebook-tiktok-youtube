import os
import sys
import json
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_DOWNLOAD_PATH = str(BASE_DIR / "downloads")
DEFAULT_HISTORY_PATH = str(BASE_DIR / "data" / "history.json")
DEFAULT_SETTINGS_PATH = str(BASE_DIR / "data" / "settings.json")

class FileManager:
    @staticmethod
    def create_directory(path: str):
        os.makedirs(path, exist_ok=True)
        
    @staticmethod
    def get_safe_filename(title: str, extension: str) -> str:
        # Keep only alphanumeric and some safe chars
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
        if not safe_title:
            safe_title = "downloaded_media"
        return f"{safe_title}.{extension}"
        
    @staticmethod
    def ensure_default_settings(settings_path: str):
        if not os.path.exists(settings_path):
            FileManager.create_directory(os.path.dirname(settings_path))
            default_settings = {
                "download_path": DEFAULT_DOWNLOAD_PATH,
                "theme": "light",
                "language": "en",
                "max_concurrent_downloads": 3
            }
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=4)
                
    @staticmethod
    def load_json(filepath: str, default_val=None):
        if not os.path.exists(filepath):
            return default_val if default_val is not None else {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default_val if default_val is not None else {}
            
    @staticmethod
    def save_json(filepath: str, data):
        FileManager.create_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
