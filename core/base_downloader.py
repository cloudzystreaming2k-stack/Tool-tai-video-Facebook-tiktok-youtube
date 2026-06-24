from abc import ABC, abstractmethod

class BaseDownloader(ABC):
    def __init__(self, url: str, download_path: str):
        self.url = url
        self.download_path = download_path

    @abstractmethod
    def get_video_info(self) -> dict:
        """Fetch metadata about the video"""
        pass

    @abstractmethod
    def download_video(self, format_id: str, progress_hook=None) -> str:
        """Download the video in the specified format"""
        pass
        
    @abstractmethod
    def download_audio(self, progress_hook=None) -> str:
        """Download only the audio"""
        pass
