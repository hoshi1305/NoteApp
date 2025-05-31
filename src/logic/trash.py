import json
import os
from config import TRASH_FILE
from datetime import datetime
# Hằng số cấu hình
trash_data = {}

def load_trash():
    """Đọc dữ liệu thùng rác từ file JSON."""
    global trash_data
    if not os.path.exists(TRASH_FILE):
        trash_data = {}
        return

    try:
        with open(TRASH_FILE, "r", encoding="utf-8") as f:
            trash_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError khi đọc {TRASH_FILE}: {e}")
        trash_data = {}  # Hoặc chuyển file lỗi sang backup
    except Exception as e:
        print(f"Lỗi bất ngờ khi đọc {TRASH_FILE}: {e}")
        trash_data = {}

def save_trash():
    """Lưu dữ liệu thùng rác vào file JSON."""
    try:
        with open(TRASH_FILE, "w", encoding="utf-8") as f:
            json.dump(trash_data, f, ensure_ascii=False, indent=4)
    except (IOError, OSError) as e:
        print(f"Lỗi ghi file {TRASH_FILE}: {e}")
    except TypeError as e:
        print(f"Lỗi serialize dữ liệu: {e}")

def move_to_trash(username, index):
    """Di chuyển ghi chú tại vị trí index của user vào thùng rác."""
    from .notes import notes_data, save_notes

    if username not in notes_data or not notes_data[username]:
        return False
    if index < 0 or index >= len(notes_data[username]):
        return False

    note = notes_data[username].pop(index)
    note["deleted_time"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")  # ✅ thêm dòng này

    if username not in trash_data:
        trash_data[username] = []

    trash_data[username].append(note)
    save_notes()
    save_trash()
    return True

def restore_from_trash(username, index):
    """Khôi phục ghi chú tại vị trí index từ thùng rác về danh sách ghi chú."""
    from .notes import notes_data, save_notes

    if username not in trash_data or not trash_data[username]:
        return False
    if index < 0 or index >= len(trash_data[username]):
        return False

    note = trash_data[username].pop(index)

    if username not in notes_data:
        notes_data[username] = []

    notes_data[username].append(note)
    save_notes()
    save_trash()
    return True

def get_trash_notes(username):
    """Trả về danh sách ghi chú trong thùng rác của user."""
    return trash_data.get(username, [])

def permanently_delete_from_trash(username, index):
    """Xóa vĩnh viễn ghi chú tại vị trí index trong thùng rác."""
    if username not in trash_data or not trash_data[username]:
        return False
    if index < 0 or index >= len(trash_data[username]):
        return False

    trash_data[username].pop(index)
    save_trash()
    return True

def permanently_delete_all_from_trash(username):
    """Xóa tất cả ghi chú trong thùng rác của user."""
    if username not in trash_data:
        return False

    trash_data[username] = []
    save_trash()
    return True
