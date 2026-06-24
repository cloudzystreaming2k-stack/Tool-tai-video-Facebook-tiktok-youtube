# AGENTS.md

## Project Overview

### Project Name

Social Media Downloader

### Description

Desktop application built with Python and PyQt6 that allows users to download videos and audio from multiple social media platforms.

Supported platforms:

* YouTube
* Facebook
* TikTok
* Instagram
* Threads

Main features:

* Download videos in multiple qualities
* Download audio (MP3)
* View download progress
* Manage download history
* Configure application settings

---

# Technology Stack

## Backend

* Python 3.12+
* yt-dlp
* FFmpeg
* threading

## Frontend

* PyQt6

## Data Storage

### JSON Files

The application does not use a database.

JSON files are used for:

* Download history
* Application settings

---

# Project Architecture

```text
Social Media Downloader
│
├── GUI
│   ├── MainWindow
│   ├── DownloadPage
│   ├── HistoryPage
│   └── SettingsPage
│
├── Core
│   ├── BaseDownloader
│   ├── YoutubeDownloader
│   ├── FacebookDownloader
│   ├── TikTokDownloader
│   ├── InstagramDownloader
│   └── ThreadsDownloader
│
├── Services
│   ├── DownloadManager
│   ├── URLParser
│   ├── FileManager
│   ├── FFmpegService
│   └── HistoryService
│
├── Data
│   ├── history.json
│   └── settings.json
│
└── Assets
```

---

# Directory Structure

```text
social-media-downloader/
│
├── main.py
│
├── gui/
│   ├── main_window.py
│   ├── pages/
│   │   ├── download_page.py
│   │   ├── history_page.py
│   │   └── settings_page.py
│   │
│   └── widgets/
│
├── core/
│   ├── base_downloader.py
│   ├── youtube_downloader.py
│   ├── facebook_downloader.py
│   ├── tiktok_downloader.py
│   ├── instagram_downloader.py
│   └── threads_downloader.py
│
├── services/
│   ├── download_manager.py
│   ├── url_parser.py
│   ├── file_manager.py
│   ├── ffmpeg_service.py
│   └── history_service.py
│
├── data/
│   ├── history.json
│   └── settings.json
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── logo.png
│
├── logs/
│
├── tests/
│
├── requirements.txt
│
└── AGENTS.md
```

---

# Layer Responsibilities

## GUI Layer

Responsible for:

* User interaction
* Displaying video information
* Showing download progress
* Displaying download history
* Managing settings

GUI must not contain business logic.

---

## Core Layer

Responsible for:

* Platform-specific implementations
* Video metadata extraction
* Format retrieval
* Download execution

Each downloader must inherit from BaseDownloader.

Example:

```python
class YoutubeDownloader(BaseDownloader):
    pass
```

---

## Services Layer

### DownloadManager

Responsible for:

* Start download
* Pause download
* Resume download
* Cancel download
* Download queue management

### URLParser

Responsible for:

* Detecting platform from URL
* URL validation

Example:

```python
{
    "platform": "youtube",
    "video_id": "xxxx"
}
```

### FileManager

Responsible for:

* Create directories
* Handle file names
* Prevent duplicate names
* Manage download folders

### FFmpegService

Responsible for:

* Merge video and audio
* Convert audio to MP3
* Format conversion

### HistoryService

Responsible for:

* Save download history
* Load history
* Delete history
* Export history

History must be stored in JSON format.

---

# Data Files

## settings.json

```json
{
    "download_path": "D:/Downloads",
    "theme": "light",
    "language": "en",
    "max_concurrent_downloads": 3
}
```

---

## history.json

```json
[
    {
        "title": "Python Tutorial",
        "platform": "YouTube",
        "quality": "1080p",
        "file_path": "D:/Downloads/python.mp4",
        "status": "completed",
        "download_date": "2026-06-24 10:30:00"
    }
]
```

---

# History Rules

Each successful download must append a new record to history.json.

Example:

```python
history.append(download_record)
```

History file must be created automatically if it does not exist.

Maximum history records:

```text
1000 records
```

When the limit is exceeded:

* Remove the oldest records first.
* Keep only the newest records.

---

# Coding Standards

## General Rules

* Follow PEP8
* Use type hints
* Follow SOLID principles where applicable
* Keep functions small and reusable
* Avoid duplicated code

Example:

```python
def get_video_info(url: str) -> dict:
    pass
```

---

## Naming Convention

### Classes

```python
DownloadManager
YoutubeDownloader
HistoryService
FileManager
```

### Methods

```python
download_video()
get_video_info()
save_history()
load_history()
```

### Constants

```python
DEFAULT_DOWNLOAD_PATH
MAX_HISTORY_RECORDS
SUPPORTED_PLATFORMS
```

---

# Logging

Store logs inside:

```text
logs/
```

Example:

```text
2026-06-24.log
```

All exceptions must be logged.

Example:

```python
try:
    download()
except Exception as e:
    logger.error(str(e))
```

---

# Supported Platforms

Current Version:

* YouTube
* Facebook
* TikTok
* Instagram
* Threads

Future Versions:

* X (Twitter)
* Vimeo
* Dailymotion

---

# Development Roadmap

## Phase 1

* Main Window
* Download Page
* YouTube Downloader
* Settings Management
* History Management

## Phase 2

* Facebook Downloader
* TikTok Downloader
* Instagram Downloader
* Threads Downloader

## Phase 3

* Download Queue
* Multi-thread Downloads
* Advanced File Management

## Phase 4

* Batch Downloads
* Playlist Downloads
* Auto Update
* Plugin System

---

# Project Goal

Build a lightweight and extensible desktop application capable of downloading media from multiple social platforms while maintaining a clean architecture, modular design, and JSON-based local storage.
