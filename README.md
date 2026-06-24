# 🎬 Social Media Downloader

**Social Media Downloader** là một ứng dụng Desktop mạnh mẽ, trực quan và hoàn toàn miễn phí được xây dựng bằng ngôn ngữ **Python** kết hợp với giao diện đồ họa **PyQt6**. Phần mềm cho phép người dùng dễ dàng tải xuống các video và đoạn âm thanh chất lượng cao từ nhiều nền tảng mạng xã hội lớn hiện nay mà không cần trải qua các bước cài đặt phần mềm phức tạp hay lo lắng về quảng cáo làm phiền.

🔗 **[👉 NHẤP VÀO ĐÂY ĐỂ TẢI ỨNG DỤNG NGAY (.EXE) 👈](https://github.com/cloudzystreaming2k-stack/Tool-t-i-video-Facebook-tiktok-youtube/releases/latest/download/SocialMediaDownloader.exe)**  
*(Lưu ý: Tải file `.exe` duy nhất này về, nhấp đúp chuột là phần mềm sẽ mở lên sử dụng được ngay lập tức mà không cần cài đặt mã nguồn hay bất kỳ thư viện hỗ trợ nào!)*

---

## 🌟 Các tính năng nổi bật
- **YouTube:** Hỗ trợ tải Video chất lượng cực cao (lên tới 4K/8K với định dạng gộp chuẩn âm thanh gốc) và tải riêng rẽ Audio (MP3).
- **TikTok:** Tải video TikTok cực nhanh, tự động xử lý định dạng video và loại bỏ lỗi chuẩn nén HEVC/H.265.
- **Facebook:** Hỗ trợ tải Facebook Video thông thường, Facebook Watch, và Facebook Reels (Lưu ý: Hiện tại chỉ hỗ trợ các video Công khai).
- **Trình quản lý lịch sử:** Tự động ghi lại toàn bộ lịch sử các video đã tải (Ngày giờ, Tên video, Link gốc, Nền tảng và Trạng thái) giúp bạn dễ dàng tra cứu.
- **Smart Directory (Quản lý thư mục thông minh):** Tự động tạo thư mục `downloads/` (để lưu video) và `data/` (để lưu lịch sử) ngay cạnh file chạy ứng dụng để đảm bảo hệ thống máy tính của bạn luôn gọn gàng.

---

## 📂 Cấu trúc Thư mục Dự án

```text
Social Media Downloader
│
├── core/                        # Chứa logic xử lý tải xuống cho từng nền tảng mạng xã hội
│   ├── base_downloader.py       # Lớp cơ sở (Base class) cho tất cả các downloader
│   ├── youtube_downloader.py    # Module xử lý link và tải từ YouTube
│   ├── tiktok_downloader.py     # Module xử lý link và tải từ TikTok
│   └── facebook_downloader.py   # Module xử lý link và tải từ Facebook
│
├── gui/                         # Mã nguồn Giao diện người dùng (PyQt6)
│   ├── main_window.py           # Cửa sổ ứng dụng chính (Chứa Sidebar & Tabs)
│   └── pages/                   # Các trang giao diện con (UI Components)
│       ├── download_page.py     # Trang xử lý dán link, hiện Thumbnail và tiến trình tải
│       ├── history_page.py      # Trang hiển thị bảng lịch sử (Có cột URL)
│       └── settings_page.py     # Trang cài đặt cấu hình phần mềm
│
├── services/                    # Các dịch vụ xử lý nền (Services)
│   ├── download_manager.py      # Quản lý luồng (Threads) không làm đơ UI khi tải
│   ├── file_manager.py          # Xử lý File, tự động nhận diện đường dẫn thông minh
│   ├── history_service.py       # Dịch vụ ghi/đọc lịch sử từ file history.json
│   └── url_parser.py            # Nhận diện đường dẫn thuộc mạng xã hội nào
│
├── dist/                        # Thư mục chứa file .exe thành phẩm sau khi Build
│   └── SocialMediaDownloader.exe 
│
├── data/                        # [Tự động sinh] Thư mục chứa cấu hình và lịch sử
│   ├── history.json             # File JSON lưu lịch sử
│   └── settings.json            # File JSON cấu hình
│
├── downloads/                   # [Tự động sinh] Nơi chứa video/audio được tải về
│
├── main.py                      # Tệp gốc khởi chạy toàn bộ chương trình
├── SocialMediaDownloader.spec   # File cấu hình đóng gói của hệ thống PyInstaller
└── requirements.txt             # Danh sách các thư viện Python (Dependencies) cần thiết
```

---

## 🛠️ Hướng dẫn dành cho Lập trình viên (Development Setup)

Phần này dành riêng cho những ai muốn đọc hiểu mã nguồn, nâng cấp tính năng hoặc chạy ứng dụng trực tiếp thông qua Terminal.

### Yêu cầu hệ thống
- Python 3.12 trở lên
- Git

### Các bước cài đặt
1. **Clone repository về máy tính:**
   ```bash
   git clone <đường-dẫn-repo>
   cd SocialMediaDownloader
   ```

2. **Tạo và kích hoạt môi trường ảo (Virtual Environment):**
   - Trên Windows:
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate
     ```

3. **Cài đặt thư viện (Dependencies):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Khởi chạy phần mềm bằng mã nguồn gốc:**
   ```bash
   python main.py
   ```

---

## 📦 Hướng dẫn tự Build ra file .exe mới

Nếu bạn có nâng cấp mã nguồn (ví dụ: bổ sung tính năng tải Instagram) và muốn tự đóng gói lại phần mềm thành 1 tệp `.exe` siêu xịn để chia sẻ:

1. Đảm bảo bạn đã **kích hoạt môi trường `.venv`** (Xem bước 2 phía trên).
2. Chạy lệnh Build sau tại thư mục gốc của dự án:
   ```cmd
   pyinstaller SocialMediaDownloader.spec
   ```
3. Chờ quá trình build kết thúc (khoảng 1-2 phút).
4. Bản build mới nhất sẽ là **1 tệp duy nhất** nằm trong thư mục `dist/` có tên `SocialMediaDownloader.exe`.
