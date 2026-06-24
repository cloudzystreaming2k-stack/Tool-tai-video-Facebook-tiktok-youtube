from PyQt6.QtCore import QObject, pyqtSignal, QThread
from services.history_service import HistoryService
import traceback

class DownloadSignals(QObject):
    progress = pyqtSignal(dict)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

class InfoFetchSignals(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

class InfoFetchWorker(QThread):
    def __init__(self, downloader):
        super().__init__()
        self.downloader = downloader
        self.signals = InfoFetchSignals()
        
    def run(self):
        try:
            info = self.downloader.get_video_info()
            self.signals.finished.emit(info)
        except Exception as e:
            self.signals.error.emit(str(e))

class DownloadWorker(QThread):
    def __init__(self, downloader, video_title, format_id=None, is_audio=False):
        super().__init__()
        self.downloader = downloader
        self.video_title = video_title
        self.format_id = format_id
        self.is_audio = is_audio
        self.signals = DownloadSignals()
        self.is_cancelled = False

    def progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("Download cancelled by user.")
            
        if d['status'] == 'downloading':
            self.signals.progress.emit({
                'status': 'downloading',
                'downloaded_bytes': d.get('downloaded_bytes', 0),
                'total_bytes': d.get('total_bytes') or d.get('total_bytes_estimate') or 0,
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0)
            })
        elif d['status'] == 'finished':
            self.signals.progress.emit({'status': 'finished'})

    def run(self):
        try:
            if self.is_audio:
                file_path = self.downloader.download_audio(progress_hook=self.progress_hook)
            else:
                file_path = self.downloader.download_video(self.format_id, progress_hook=self.progress_hook)
            
            self.signals.finished.emit(file_path)
        except Exception as e:
            self.signals.error.emit(str(e))

class DownloadManager:
    def __init__(self):
        self.active_workers = []
        self.history_service = HistoryService()

    def fetch_info(self, downloader, on_finished=None, on_error=None):
        worker = InfoFetchWorker(downloader)
        
        if on_finished:
            worker.signals.finished.connect(on_finished)
        if on_error:
            worker.signals.error.connect(on_error)
            
        self.active_workers.append(worker)
        
        def cleanup(result_or_error=None):
            if worker in self.active_workers:
                self.active_workers.remove(worker)
                
        worker.signals.finished.connect(cleanup)
        worker.signals.error.connect(cleanup)
        
        worker.start()
        return worker

    def start_download(self, downloader, video_title, platform: str = 'unknown',
                       format_id=None, is_audio=False,
                       on_progress=None, on_finished=None, on_error=None):
        worker = DownloadWorker(downloader, video_title, format_id, is_audio)
        
        if on_progress:
            worker.signals.progress.connect(on_progress)
        
        def internal_finished(file_path):
            self.history_service.add_record(
                title=video_title,
                platform=platform.capitalize(),
                quality='Audio (MP3)' if is_audio else format_id,
                file_path=file_path,
                status='completed',
                url=downloader.url
            )
            if on_finished:
                on_finished(file_path)
            if worker in self.active_workers:
                self.active_workers.remove(worker)
                
        def internal_error(error_msg):
            if on_error:
                on_error(error_msg)
            if worker in self.active_workers:
                self.active_workers.remove(worker)
            
        worker.signals.finished.connect(internal_finished)
        worker.signals.error.connect(internal_error)
            
        self.active_workers.append(worker)
        worker.start()
        return worker

    def cancel_download(self, worker):
        if worker in self.active_workers:
            worker.is_cancelled = True
