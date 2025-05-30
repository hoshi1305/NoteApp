import tkinter as tk
from tkinter import messagebox
from config import center_window
from logic.auth import check_login, register_user

# Hằng số cấu hình
LOGIN_BG = "#e8f5e9"
LOGIN_FG = "#1b5e20"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"

# Hàm xử lý logic
def validate_login_input(username, password):
    """Kiểm tra dữ liệu đầu vào đăng nhập."""
    return username.strip() and password.strip()

# Hàm xử lý giao diện
def show_login_screen(root, main_app_callback):
    """Hiển thị màn hình đăng nhập."""
    root.configure(bg=LOGIN_BG)
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Đăng nhập", font=("Arial", 18, "bold"), 
            fg=LOGIN_FG, bg=LOGIN_BG).pack(pady=15)

    frame = tk.Frame(root, bg=LOGIN_BG)
    frame.pack(pady=10)

    tk.Label(frame, text="Tên tài khoản:", bg=LOGIN_BG, fg=LOGIN_FG, 
            font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg=LOGIN_BG, fg=LOGIN_FG, 
            font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)
    
    def login():
        """Xử lý sự kiện khi nhấn nút đăng nhập."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not validate_login_input(username, password):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin đăng nhập.")
            return
            
        # Kiểm tra đăng nhập
        success, message = check_login(username, password)
        if success:
            messagebox.showinfo("Thành công", message)
            main_app_callback(root, username)
        else:
            messagebox.showerror("Thất bại", message)

    def goto_register():
        """Chuyển sang màn hình đăng ký."""
        show_register_screen(root, main_app_callback)

    tk.Button(root, text="Đăng nhập", command=login, 
            bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Tạo tài khoản mới", command=goto_register, 
            bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

def show_register_screen(root, main_app_callback):
    """Hiển thị màn hình đăng ký."""
    root.configure(bg=LOGIN_BG)
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Tạo tài khoản", font=("Arial", 18, "bold"), 
            fg=LOGIN_FG, bg=LOGIN_BG).pack(pady=15)

    frame = tk.Frame(root, bg=LOGIN_BG)
    frame.pack(pady=10)

    tk.Label(frame, text="Tên tài khoản:", bg=LOGIN_BG, fg=LOGIN_FG, 
            font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg=LOGIN_BG, fg=LOGIN_FG, 
            font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(frame, text="Nhập lại mật khẩu:", bg=LOGIN_BG, fg=LOGIN_FG,
             font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
    confirm_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    confirm_entry.grid(row=2, column=1, pady=5)

    def register():
        """Xử lý sự kiện khi nhấn nút đăng ký."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_entry.get().strip()
        
        if not username or not password or not confirm_password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return
            
        success, message = register_user(username, password, confirm_password)
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    tk.Button(root, text="Đăng ký", command=register, 
            bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Quay lại đăng nhập", command=lambda: show_login_screen(root, main_app_callback), 
            bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

# Class
class LoginApp:
    """Lớp khởi tạo ứng dụng đăng nhập."""
    def __init__(self, root, main_app_callback):
        self.root = root
        self.main_app_callback = main_app_callback
        
    def start(self):
        """Bắt đầu hiển thị màn hình đăng nhập."""
        self.root.title("Đăng nhập ứng dụng ghi chú")
        self.root.geometry("420x320")
        center_window(self.root, 420, 320)
        show_login_screen(self.root, self.main_app_callback)
