# 1. Import thư viện
import os

# 2. Hằng số cấu hình (giá trị không đổi)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USER_FILE = os.path.join(DATA_DIR, 'users.json')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')

# 3. Helper function (Hàm tiện ích, chỉ dùng khi cần gọi nhiều lần)
def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")