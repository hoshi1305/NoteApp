import json
import os
from datetime import datetime
from config import NOTES_FILE

# Biến toàn cục
notes_data = []

# Hàm xử lý logic
def load_notes():
    """Đọc dữ liệu ghi chú từ file JSON."""
    global notes_data
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    else:
        notes_data = []

def save_notes():
    """Lưu dữ liệu ghi chú vào file JSON."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=2)

def add_note(title, content):
    """Thêm ghi chú mới vào danh sách."""
    title = title.strip() or "Không tiêu đề"
    if not content.strip():
        return False
        
    now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    notes_data.insert(0, {
        "title": title,
        "content": content,
        "time": now_str
    })
    save_notes()
    return True
