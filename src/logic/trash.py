import json
import os
from config import TRASH_FILE
from datetime import datetime

# Hằng số cấu hình
trash_data = {}


# Hàm xử lý logic
def load_trash():
    """Đọc dữ liệu thùng rác từ file JSON."""
    global trash_data

    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(TRASH_FILE):
        trash_data = {}
        return

    try:
        with open(TRASH_FILE, "r", encoding="utf-8") as f:
            trash_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError khi đọc {TRASH_FILE}: {e}")
        trash_data = {}
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

    # Kiểm tra xem user có ghi chú không
    if username not in notes_data:
        return False

    if not notes_data[username]:  # Danh sách ghi chú rỗng
        return False

    # Kiểm tra index có hợp lệ không
    if index >= len(notes_data[username]):
        return False

    # Lấy ghi chú ra khỏi danh sách chính
    note = notes_data[username].pop(index)

    # Thêm thời gian xóa vào ghi chú
    note["deleted_time"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    # Tạo danh sách thùng rác cho user nếu chưa có
    if username not in trash_data:
        trash_data[username] = []

    # Thêm ghi chú vào thùng rác
    trash_data[username].append(note)

    save_notes()
    save_trash()
    return True


def restore_from_trash(username, index):
    """Khôi phục ghi chú tại vị trí index từ thùng rác về danh sách ghi chú."""
    from .notes import notes_data, save_notes

    # Kiểm tra xem user có ghi chú trong thùng rác không
    if username not in trash_data:
        return False

    if not trash_data[username]:  # Thùng rác rỗng
        return False

    # Kiểm tra index có hợp lệ không
    if index >= len(trash_data[username]):
        return False

    # Lấy ghi chú ra khỏi thùng rác
    note = trash_data[username].pop(index)

    # Xóa thời gian xóa vì đã khôi phục
    if "deleted_time" in note:
        del note["deleted_time"]

    # Tạo danh sách ghi chú cho user nếu chưa có
    if username not in notes_data:
        notes_data[username] = []

    # Thêm ghi chú vào danh sách chính
    notes_data[username].append(note)

    save_notes()
    save_trash()
    return True


def get_trash_notes(username):
    """Trả về danh sách ghi chú trong thùng rác của user."""
    # Nếu user không có trong thùng rác, trả về danh sách rỗng
    if username in trash_data:
        return trash_data[username]
    else:
        return []


def permanently_delete_from_trash(username, index):
    """Xóa vĩnh viễn ghi chú tại vị trí index trong thùng rác."""

    # Kiểm tra xem user có ghi chú trong thùng rác không
    if username not in trash_data:
        return False

    if not trash_data[username]:  # Thùng rác rỗng
        return False

    # Kiểm tra index có hợp lệ không
    if index >= len(trash_data[username]):
        return False

    # Xóa ghi chú khỏi thùng rác (xóa vĩnh viễn)
    trash_data[username].pop(index)

    save_trash()
    return True


def permanently_delete_all_from_trash(username):
    """Xóa tất cả ghi chú trong thùng rác của user."""

    # Kiểm tra xem user có trong thùng rác không
    if username not in trash_data:
        return False

    # Xóa tất cả ghi chú trong thùng rác của user
    trash_data[username] = []

    save_trash()
    return True
