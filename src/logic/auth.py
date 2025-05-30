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
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    """Lưu dữ liệu người dùng vào file JSON."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def check_login(username, password):
    """Kiểm tra xem username và password có hợp lệ không."""
    users = load_users()  # Tải danh sách người dùng từ file
    for user in users:  # Duyệt qua từng người dùng
        if user["username"] == username:  # Tìm thấy username
            hashed_input_password = hash_password(password)  # Băm password nhập vào
            if user["password"] == hashed_input_password:  # So sánh password đã băm
                return True, "Đăng nhập thành công"  # Đăng nhập thành công
            else:
                return False, "Sai mật khẩu"  # Sai mật khẩu
    return False, "Tên tài khoản không tồn tại"  # Không tìm thấy username


def register_user(username, password, confirm_password):
    """Đăng ký người dùng mới nếu tên tài khoản chưa tồn tại."""
    # Kiểm tra tính hợp lệ tên tài khoản
    if not validate_username(username):
        return False, "Tên tài khoản không hợp lệ"

    # Kiểm tra tính hợp lệ mật khẩu
    if not validate_password(password):
        return False, "Mật khẩu yêu cầu ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt"
    
    # Kiểm tra tính hợp lệ mật khẩu xác nhận
    if not validate_password(confirm_password):
        return False, "Mật khẩu xác nhận không trung khớp với mật khẩu"

    # Kiểm tra khớp mật khẩu và xác nhận
    if password != confirm_password:
        return False, "Mật khẩu xác nhận không khớp"

    users = load_users()
    for user in users:
        if user["username"] == username:
            return False, "Tên tài khoản đã tồn tại"

    hashed_password = hash_password(password)
    new_user = {"username": username, "password": hashed_password}
    users.append(new_user)
    save_users(users)
    return True, "Đăng ký thành công"

def get_user_info(username):
    """Lấy thông tin người dùng."""
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None