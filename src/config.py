import os
import sys
from dotenv import load_dotenv

# --- START: Phần thêm mới hoặc chỉnh sửa để đóng gói ---
def get_resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến resource, hoạt động cả khi dev và khi đã đóng gói. """
    try:
        # PyInstaller tạo một thư mục tạm _MEIPASS và lưu trữ resource ở đó
        # khi chạy từ file .exe đóng gói bằng --onefile
        base_path = sys._MEIPASS
    except Exception:
        # Khi chạy từ source code (dev mode)
        # __file__ trong config.py là src/config.py
        # os.path.dirname(__file__) là src/
        # os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) sẽ trỏ về thư mục gốc của dự án (NoteApp/)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)
# --- END: Phần thêm mới hoặc chỉnh sửa ---

# Cấu hình đường dẫn
# BASE_DIR cũ không còn cần thiết theo cách này nữa, hoặc có thể định nghĩa lại nếu muốn
# sys.path.append(BASE_DIR) # Dòng này có thể không cần thiết nữa nếu cấu trúc import của bạn chuẩn

# Hằng số cấu hình - SỬ DỤNG get_resource_path
DATA_DIR = get_resource_path('data')
USER_FILE = os.path.join(DATA_DIR, 'users.json')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')
TRASH_FILE = os.path.join(DATA_DIR, 'trash.json')

# Cấu hình API AI - SỬ DỤNG get_resource_path
try:
    dotenv_path = get_resource_path('.env') # .env nằm ở thư mục gốc dự án
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    else:
        GEMINI_API_KEY = None
        # Giữ lại print này hoặc dùng logging để debug khi đóng gói nếu .env không tìm thấy
        print(f"Cảnh báo: Không tìm thấy file .env tại {dotenv_path}. Các chức năng AI có thể không hoạt động.")
except Exception as e:
    GEMINI_API_KEY = None
    print(f"Lỗi cấu hình API từ .env: {e}")

MODEL_NAME = "gemini-2.0-flash" # Tên model giữ nguyên

# Hàm tiện ích
def center_window(window, width, height): # Hàm này giữ nguyên
    """Căn giữa cửa sổ trên màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")