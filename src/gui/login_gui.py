import tkinter as tk
from tkinter import messagebox
from config import center_window
from logic.auth import check_login, register_user


def show_login_screen(root, main_app_callback):
    root.configure(bg="#e8f5e9")
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Đăng nhập", font=("Arial", 18, "bold"), fg="#1b5e20", bg="#e8f5e9").pack(pady=15)

    frame = tk.Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    tk.Label(frame, text="Email:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        
        if check_login(email, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            main_app_callback(email)
        else:
            messagebox.showerror("Thất bại", "Sai email hoặc mật khẩu.")

    def goto_register():
        show_register_screen(root, main_app_callback)

    tk.Button(root, text="Đăng nhập", command=login, bg="#43a047", fg="white", font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Tạo tài khoản mới", command=goto_register, bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

def show_register_screen(root, main_app_callback):
    root.configure(bg="#e8f5e9")
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Tạo tài khoản", font=("Arial", 18, "bold"), fg="#1b5e20", bg="#e8f5e9").pack(pady=15)

    frame = tk.Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    tk.Label(frame, text="Email:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def register():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ.")
            return
            
        if register_user(email, password):
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            show_login_screen(root, main_app_callback)
        else:
            messagebox.showerror("Lỗi", "Email đã tồn tại.")

    tk.Button(root, text="Đăng ký", command=register, bg="#43a047", fg="white", font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Quay lại đăng nhập", command=lambda: show_login_screen(root, main_app_callback), bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

class LoginApp:
    def __init__(self, root, main_app_callback):
        self.root = root
        self.main_app_callback = main_app_callback
        
    def start(self):
        self.root.title("Đăng nhập ứng dụng ghi chú")
        self.root.geometry("420x320")
        center_window(self.root, 420, 320)
        show_login_screen(self.root, self.main_app_callback)