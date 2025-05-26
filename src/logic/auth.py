import json
import os
from config import USER_FILE

def load_users():
    """Đọc dữ liệu người dùng từ file JSON."""
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Lưu dữ liệu người dùng vào file JSON."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def check_login(username, password):
    """Kiểm tra thông tin đăng nhập có hợp lệ không."""
    users = load_users()
    return username in users and users[username] == password

def register_user(username, password):
    """Đăng ký người dùng mới nếu tên tài khoản chưa tồn tại."""
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True