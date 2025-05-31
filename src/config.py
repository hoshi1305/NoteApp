import os
import sys
from dotenv import load_dotenv

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Hằng số cấu hình
DATA_DIR = os.path.join(BASE_DIR, 'data')
USER_FILE = os.path.join(DATA_DIR, 'users.json')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')
TRASH_FILE = os.path.join(DATA_DIR, 'trash.json')

# Cấu hình API AI
try:
    dotenv_path = os.path.join(BASE_DIR, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    else:
        GEMINI_API_KEY = None
        print("Không tìm thấy file .env. Các chức năng AI sẽ không hoạt động.")
except Exception as e:
    GEMINI_API_KEY = None
    print(f"Lỗi cấu hình API: {e}")

MODEL_NAME = "gemini-2.0-flash"

# Hàm tiện ích
def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")