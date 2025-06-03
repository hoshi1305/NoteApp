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


def get_user_info(username):
    """Lấy thông tin người dùng."""
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None


def is_admin(username):
    """Kiểm tra xem user có quyền admin không."""
    user = get_user_info(username)
    return user and user.get("role") == "admin"


# Hàm xử lý logic
def load_users():
    """Đọc dữ liệu người dùng từ file JSON."""
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(USER_FILE):
        return []
    
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Lỗi JSONDecodeError khi đọc {USER_FILE}: {e}")
        return []
    except Exception as e:
        print(f"Lỗi bất ngờ khi đọc {USER_FILE}: {e}")
        return []


def save_users(users):
    """Lưu dữ liệu người dùng vào file JSON."""
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        print(f"Lỗi ghi file {USER_FILE}: {e}")
    except TypeError as e:
        print(f"Lỗi serialize dữ liệu: {e}")


def check_login(username, password):
    """Kiểm tra xem username và password có hợp lệ không."""
    users = load_users()
    
    # Duyệt qua từng người dùng để tìm username
    for user in users:
        if user["username"] == username:
            # Băm password nhập vào và so sánh với password đã lưu
            hashed_input_password = hash_password(password)
            if user["password"] == hashed_input_password:
                return True, "Đăng nhập thành công"
            else:
                return False, "Sai mật khẩu"
    
    return False, "Tên tài khoản không tồn tại"


def register_user(username, password, confirm_password):
    """Đăng ký người dùng mới (mặc định role user)."""
    # Kiểm tra tính hợp lệ tên tài khoản
    if not validate_username(username):
        return False, "Tên tài khoản không hợp lệ"

    # Kiểm tra tính hợp lệ mật khẩu
    if not validate_password(password):
        return (
            False,
            "Mật khẩu yêu cầu ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt",
        )

    # Kiểm tra khớp mật khẩu và xác nhận
    if password != confirm_password:
        return False, "Mật khẩu xác nhận không khớp"

    users = load_users()
    
    # Kiểm tra tên tài khoản đã tồn tại chưa
    for user in users:
        if user["username"] == username:
            return False, "Tên tài khoản đã tồn tại"

    # Tạo user mới
    hashed_password = hash_password(password)
    new_user = {
        "username": username,
        "password": hashed_password,
        "role": "user",
    }
    
    users.append(new_user)
    save_users(users)
    return True, "Đăng ký thành công"