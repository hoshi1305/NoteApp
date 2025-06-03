import json
import os
from datetime import datetime
from config import NOTES_FILE

# Hằng số cấu hình
notes_data = {}


# Hàm tiện ích
def validate_note_title(title):
    """Kiểm tra tiêu đề ghi chú có hợp lệ không."""
    # Kiểm tra xem title có phải là chuỗi text không
    if not isinstance(title, str):
        return False

    # Loại bỏ khoảng trắng đầu cuối
    title = title.strip()

    # Kiểm tra độ dài tiêu đề (tối đa 100 ký tự)
    if len(title) > 100:
        return False

    return True


def get_user_notes(username):
    """Trả về danh sách ghi chú của user."""
    # Nếu user có ghi chú trong hệ thống
    if username in notes_data:
        return notes_data[username]
    else:
        # User chưa có ghi chú nào, trả về danh sách rỗng
        return []


# Hàm xử lý logic
def load_notes():
    """Đọc dữ liệu ghi chú từ file JSON."""
    global notes_data

    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(NOTES_FILE):
        notes_data = {}
        return

    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError khi đọc {NOTES_FILE}: {e}")
        notes_data = {}
    except Exception as e:
        print(f"Lỗi bất ngờ khi đọc {NOTES_FILE}: {e}")
        notes_data = {}


def save_notes():
    """Lưu dữ liệu ghi chú vào file JSON."""
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=4)
    except (IOError, OSError) as e:
        print(f"Lỗi ghi file {NOTES_FILE}: {e}")
    except TypeError as e:
        print(f"Lỗi serialize dữ liệu: {e}")


def add_note(username, title, content):
    """Thêm ghi chú mới vào danh sách của user."""
    # Xử lý tiêu đề: loại bỏ khoảng trắng thừa
    title = title.strip()
    if not title:  # Nếu tiêu đề rỗng
        title = "Không tiêu đề"

    # Xử lý nội dung: loại bỏ khoảng trắng thừa
    content = content.strip()
    if not content:  # Nếu nội dung rỗng
        return False

    # Tạo ghi chú mới với thời gian hiện tại
    now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    note = {
        "title": title,
        "content": content,
        "created_time": now_str,
        "updated_time": now_str,
    }

    # Tạo danh sách ghi chú cho user nếu chưa có
    if username not in notes_data:
        notes_data[username] = []

    # Thêm ghi chú vào đầu danh sách (mới nhất lên trên)
    notes_data[username].insert(0, note)
    save_notes()
    return True


def update_note(username, index, title, content):
    """Cập nhật ghi chú tại vị trí index của user."""
    # Kiểm tra xem user có ghi chú không
    if username not in notes_data:
        return False

    # Kiểm tra danh sách ghi chú có rỗng không
    if not notes_data[username]:
        return False

    # Kiểm tra index có hợp lệ không
    if index >= len(notes_data[username]):
        return False

    # Xử lý tiêu đề: loại bỏ khoảng trắng thừa
    title = title.strip()
    if not title:  # Nếu tiêu đề rỗng
        title = "Không tiêu đề"

    # Xử lý nội dung: loại bỏ khoảng trắng thừa
    content = content.strip()
    if not content:  # Nếu nội dung rỗng
        return False

    # Cập nhật ghi chú với thời gian mới
    now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    note = notes_data[username][index]

    note["title"] = title
    note["content"] = content
    note["updated_time"] = now_str

    save_notes()
    return True


def delete_note(username, index):
    """Xóa ghi chú tại vị trí index của user."""
    # Kiểm tra xem user có ghi chú không
    if username not in notes_data:
        return False

    # Kiểm tra danh sách ghi chú có rỗng không
    if not notes_data[username]:
        return False

    # Kiểm tra index có hợp lệ không
    if index >= len(notes_data[username]):
        return False

    # Xóa ghi chú khỏi danh sách
    notes_data[username].pop(index)
    save_notes()
    return True


def search_notes(username, keyword):
    """Tìm kiếm ghi chú theo từ khóa."""
    # Kiểm tra xem user có ghi chú không
    if username not in notes_data:
        return []

    results = []
    # Chuyển keyword về chữ thường để so sánh không phân biệt hoa thường
    keyword_lower = keyword.lower()

    # Duyệt qua từng ghi chú để tìm kiếm
    for note in notes_data[username]:
        title_lower = note["title"].lower()
        content_lower = note["content"].lower()

        # Kiểm tra keyword có trong title hoặc content không
        if keyword_lower in title_lower or keyword_lower in content_lower:
            results.append(note)

    return results
