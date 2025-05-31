import json
import os
from datetime import datetime
from config import NOTES_FILE

# Hằng số cấu hình
notes_data = {}


# Hàm tiện ích
def validate_note_title(title):
    """Kiểm tra tiêu đề ghi chú có hợp lệ không."""
    if not isinstance(title, str):
        return False
    title = title.strip()
    if len(title) > 100:
        return False
    return True


def get_user_notes(username):
    """Trả về danh sách ghi chú của user."""
    return notes_data.get(username, [])


# Hàm xử lý logic
def load_notes():
    """Đọc dữ liệu ghi chú từ file JSON."""
    global notes_data
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    else:
        notes_data = {}


def save_notes():
    """Lưu dữ liệu ghi chú vào file JSON."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=4)


def add_note(username, title, content):
    """Thêm ghi chú mới vào danh sách của user."""
    title = title.strip() or "Không tiêu đề"
    content = content.strip()
    if not content:
        return False

    now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    note = {
        "title": title,
        "content": content,
        "created_time": now_str,
        "updated_time": now_str
    }

    if username not in notes_data:
        notes_data[username] = []

    notes_data[username].insert(0, note)
    save_notes()
    return True


def update_note(username, index, title, content):
    """Cập nhật ghi chú tại vị trí index của user."""
    if username not in notes_data or not notes_data[username]:
        return False
    if index < 0 or index >= len(notes_data[username]):
        return False

    title = title.strip() or "Không tiêu đề"
    content = content.strip()
    if not content:
        return False

    now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    note = notes_data[username][index]

    note["title"] = title
    note["content"] = content
    note["updated_time"] = now_str

    save_notes()
    return True



def delete_note(username, index):
    """Xóa ghi chú tại vị trí index của user."""
    if username not in notes_data or not notes_data[username]:
        return False
    if index < 0 or index >= len(notes_data[username]):
        return False

    notes_data[username].pop(index)
    save_notes()
    return True


def search_notes(username, keyword):
    """Tìm kiếm ghi chú theo từ khóa."""
    if username not in notes_data:
        return []

    results = []
    for note in notes_data[username]:
        if (
            keyword.lower() in note["title"].lower()
            or keyword.lower() in note["content"].lower()
        ):
            results.append(note)
    return results
