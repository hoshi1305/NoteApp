import json
import os
import re
import hashlib
from config import USER_FILE

# Hằng số cấu hình
USERNAME_REGEX = r"^[a-zA-Z0-9_]{3,20}$"
PASSWORD_REGEX = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$"
)


# Hàm tiện ích
def validate_username(username):
    """Kiểm tra tên tài khoản có hợp lệ không."""
    return re.match(USERNAME_REGEX, username) is not None


def validate_password(password):
    """Kiểm tra mật khẩu có hợp lệ không."""
    return re.match(PASSWORD_REGEX, password) is not None


def hash_password(password):
    """Băm mật khẩu để lưu trữ an toàn."""
    return hashlib.sha256(password.encode()).hexdigest()


# Hàm xử lý logic
def load_users():
    """Đọc dữ liệu người dùng từ file JSON."""
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Lưu dữ liệu người dùng vào file JSON."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def check_login(username, password):
    """Kiểm tra thông tin đăng nhập có hợp lệ không."""
    users = load_users()
    if username in users:
        # Băm mật khẩu người dùng nhập vào
        hashed_input_password = hash_password(password)
        # So sánh mật khẩu đã băm với mật khẩu lưu trong file
        if users[username] == hashed_input_password:
            return True  # Đăng nhập thành công
        else:
            return False  # Sai mật khẩu
    else:
        return False  # Tài khoản không tồn tại


def register_user(username, password, confirm_password):
    """Đăng ký người dùng mới nếu tên tài khoản chưa tồn tại."""
    # Kiểm tra mật khẩu xác nhận có khớp không
    if password != confirm_password:
        return False, "Mật khẩu xác nhận không khớp"

    users = load_users()
    if username in users:
        return False, "Tên tài khoản đã tồn tại"

    # Băm mật khẩu trước khi lưu
    hashed_password = hash_password(password)
    users[username] = hashed_password
    save_users(users)
    return True, "Đăng ký thành công"