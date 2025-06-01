# NoteApp

Ứng dụng quản lý ghi chú đơn giản được xây dựng bằng Python và Tkinter, tích hợp AI để hỗ trợ người dùng viết và chỉnh sửa ghi chú hiệu quả hơn.

## Mục lục
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cấu hình](#cấu-hình)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)

## Tính năng

### Quản lý người dùng
- Đăng ký tài khoản với mã hóa mật khẩu SHA-256
- Đăng nhập an toàn với xác thực
- Phân quyền người dùng (admin/user)

### Quản lý ghi chú
- Tạo, sửa, xóa ghi chú
- Tìm kiếm ghi chú theo tiêu đề và nội dung
- Lưu trữ timestamp tạo và cập nhật
- Thùng rác để khôi phục ghi chú đã xóa

### Tính năng AI (Google Gemini)
- **Tóm tắt văn bản**: Chỉ dành cho admin
- **Gợi ý tiêu đề**: Dành cho tất cả người dùng
- **Cải thiện văn bản**: Định dạng và tối ưu nội dung

### Giao diện
- UI hiện đại với theme tối
- Sidebar điều hướng trực quan
- Bảng hiển thị danh sách ghi chú
- Editor văn bản tích hợp

## Yêu cầu hệ thống
- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows, macOS, Linux
- **Kết nối internet**: Cần thiết cho các tính năng AI

## Cài đặt

### Cách 1:
### Bước 1: Clone repository
```bash
git clone <repository-url>
cd NoteApp
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy úng dụng bằng file python
```bash
python main.py
```

### Cách 1:
### Bước 1: Clone repository
```bash
git clone <repository-url>
cd NoteApp
```

### Bước 2: Chạy file .exe và bắt đầu sử dụng ứng dụng
```bash
NoteApp.exe
```

## Cấu trúc dự án
```
NoteApp/
├── data/                           # Dữ liệu ứng dụng
│   ├── users.json                 # Thông tin người dùng
│   ├── notes.json                 # Ghi chú của người dùng
│   └── trash.json                 # Thùng rác
├── src/                           # Mã nguồn
│   ├── config.py                  # Cấu hình và hằng số
│   ├── main.py                    # Entry point
│   ├── gui/                       # Giao diện người dùng
│   │   ├── login_gui.py          # Màn hình đăng nhập/đăng ký
│   │   ├── notes_gui.py          # Tạo ghi chú mới
│   │   └── trash_gui.py          # Quản lý thùng rác
│   └── logic/                     # Logic xử lý
│       ├── auth.py               # Xác thực người dùng
│       ├── notes.py              # Quản lý ghi chú
│       ├── trash.py              # Quản lý thùng rác
│       └── api_ai.py             # Tích hợp AI
├── .env                          # Cấu hình API keys
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Dependencies
└── README.md                     # Tài liệu dự án
```

## Cấu hình

### File config.py
Chứa các thiết lập chính:
- Đường dẫn các file dữ liệu
- API key cho Google Gemini
- Hàm tiện ích cho giao diện

### Dữ liệu lưu trữ
Ứng dụng sử dụng JSON để lưu trữ:

**users.json**: Thông tin người dùng
```json
[
    {
        "username": "admin",
        "password": "hashed_password",
        "role": "admin"
    }
]
```

**notes.json**: Ghi chú theo user
```json
{
    "username": [
        {
            "title": "Tiêu đề",
            "content": "Nội dung",
            "created_time": "18:04:14 01/06/2025",
            "updated_time": "18:06:32 01/06/2025"
        }
    ]
}
```

## Chạy ứng dụng

### Từ thư mục src
```bash
cd src
python main.py
```

### Chạy như module
```bash
python -m src.main
```

## Hướng dẫn sử dụng

### Đăng ký/Đăng nhập
1. Khởi động ứng dụng
2. Tạo tài khoản mới hoặc đăng nhập
3. Mật khẩu yêu cầu: ít nhất 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt

### Quản lý ghi chú
1. **Tạo ghi chú**: Nhấp "Thêm ghi chú" từ trang chủ
2. **Sửa ghi chú**: Chọn ghi chú trong bảng, nhấp "Sửa ghi chú"
3. **Xóa ghi chú**: Chọn ghi chú, nhấp "Xóa ghi chú" (chuyển vào thùng rác)
4. **Tìm kiếm**: Nhập từ khóa vào ô tìm kiếm

### Thùng rác
- Xem ghi chú đã xóa
- Khôi phục ghi chú về danh sách chính
- Xóa vĩnh viễn ghi chú
---