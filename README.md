# NoteApp
Đây là ứng dụng quản lý ghi chú đơn giản bằng python.

## Mục lục
- [Tính năng](#tính-năng)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Lưu trữ dữ liệu](#lưu-trữ-dữ-liệu)
- [Cấu hình](#cấu-hình)
- [Chạy ứng dụng](#chạy-ứng-dụng)

## Tính năng
- Đăng ký / Đăng nhập người dùng.
- Tạo, lưu và xem ghi chú với timestamp.
- Giao diện chính với sidebar điều hướng.
- Trang chức năng: Tasks, Files, Events, Tags (đang phát triển).

## Yêu cầu
- Python 3.7 trở lên.
- Thư viện Tkinter (có sẵn trong Python).
- (Không có dependencies bên ngoài. Nếu có, thêm vào `requirements.txt`.)

## Cài đặt
```bash
git clone https://github.com/username/NoteApp.git
cd NoteApp
pip install -r requirements.txt
```

## Cấu trúc dự án
```
NoteApp/
├── data/
│   ├── users.json       # Dữ liệu người dùng
│   └── notes.json       # Dữ liệu ghi chú
├── src/
│   ├── config.py        # Thiết lập cấu hình, hằng số
│   ├── main.py          # Entry point, logic UI chính
│   ├── gui/
│   │   ├── login_gui.py # Màn hình đăng nhập/đăng ký
│   │   └── note_gui.py  # UI tạo ghi chú
│   └── logic/
│       ├── auth.py      # Xử lý đăng nhập, đăng ký
│       └── notes.py     # Xử lý logic ghi chú
├── .gitignore
├── .gitattributes
├── README.md
└── requirements.txt
```

## Lưu trữ dữ liệu
- Dữ liệu được lưu trong thư mục `data/`:
  - `users.json`: thông tin đăng nhập người dùng.
  - `notes.json`: danh sách ghi chú (title, content, time).

## Cấu hình
- File `config.py` định nghĩa các hằng số và helper function.
- `BASE_DIR` trỏ đến thư mục gốc, `DATA_DIR` trỏ đến thư mục `data/`.
- `USER_FILE` và `NOTES_FILE` trỏ đến file JSON tương ứng.

## Chạy ứng dụng
```bash
cd src
python -m main
```
hoặc
```bash
python -m src.main
```