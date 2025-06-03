import os
import sys
from dotenv import load_dotenv

def get_resource_path(relative_path):
    """Lấy đường dẫn tuyệt đối đến resource, hỗ trợ cả dev và exe."""
    try:
        base_path = sys._MEIPASS  # PyInstaller mode
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Dev mode
    
    return os.path.join(base_path, relative_path)


# Đường dẫn file
DATA_DIR = get_resource_path('data')
USER_FILE = os.path.join(DATA_DIR, 'users.json')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')
TRASH_FILE = os.path.join(DATA_DIR, 'trash.json')

# Cấu hình AI
try:
    dotenv_path = get_resource_path('.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    else:
        GEMINI_API_KEY = None
        print(f"Cảnh báo: Không tìm thấy file .env tại {dotenv_path}")
except Exception as e:
    GEMINI_API_KEY = None
    print(f"Lỗi cấu hình API từ .env: {e}")

MODEL_NAME = "gemini-2.0-flash"

# Hàm tiện ích
def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")