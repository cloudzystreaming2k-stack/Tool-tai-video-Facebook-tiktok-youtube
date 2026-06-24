import os
import json
from datetime import datetime
from services.file_manager import FileManager, DEFAULT_HISTORY_PATH

MAX_HISTORY_RECORDS = 1000

class HistoryService:
    def __init__(self, history_file: str = DEFAULT_HISTORY_PATH):
        self.history_file = history_file

    def load_history(self) -> list:
        return FileManager.load_json(self.history_file, default_val=[])
        
    def save_history(self, history: list):
        # Keep only the newest records
        if len(history) > MAX_HISTORY_RECORDS:
            history = history[-MAX_HISTORY_RECORDS:]
        FileManager.save_json(self.history_file, history)
        
    def add_record(self, title: str, platform: str, quality: str, file_path: str, status: str = "completed", url: str = ""):
        record = {
            "title": title,
            "url": url,
            "platform": platform,
            "quality": quality,
            "file_path": file_path,
            "status": status,
            "download_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        history = self.load_history()
        history.append(record)
        self.save_history(history)
