# 1. Import thư viện
import tkinter as tk
import sys
import os
from config import center_window
from gui.login_gui import LoginApp
from gui.note_gui import show_create_note_ui, clear_frame
from logic.notes import load_notes

# Thêm đường dẫn gốc vào sys.path để import đúng
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. Hằng số cấu hình
MAIN_BG = "#1e1e1e"
SIDEBAR_BG = "#2b2b2b"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"

# 3. Hàm xử lý giao diện
def main_app(root, username):
    """Hiển thị giao diện chính của ứng dụng."""
    root.geometry("900x600")
    center_window(root, 900, 600)
    root.configure(bg=MAIN_BG)
    clear_frame(root)

    # Sidebar
    sidebar = tk.Frame(root, bg=SIDEBAR_BG, width=300)
    sidebar.pack(side="left", fill="y")

    # User info
    tk.Label(sidebar, text="Người dùng", bg=SIDEBAR_BG, fg="white",
            font=("Arial", 14, "bold")).pack(pady=15)
    tk.Label(sidebar, text=username, bg=SIDEBAR_BG, fg="white",
            font=("Arial", 10), wraplength=180).pack(pady=5)

    # Content area
    content_frame = tk.Frame(root, bg=MAIN_BG)
    content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Các hàm hiển thị nội dung khi bấm menu
    def show_home():
        """Hiển thị trang chủ."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Trang chủ", bg=MAIN_BG, 
                fg="white", font=("Arial", 20)).pack(pady=20)

    def show_tasks():
        """Hiển thị trang quản lý công việc."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Tasks - Chức năng đang phát triển", 
                bg=MAIN_BG, fg="white", font=("Arial", 20)).pack(pady=20)

    def show_files():
        """Hiển thị trang quản lý tệp."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Files - Chức năng đang phát triển", 
                bg=MAIN_BG, fg="white", font=("Arial", 20)).pack(pady=20)

    def show_events():
        """Hiển thị trang sự kiện."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Events - Chức năng đang phát triển", 
                bg=MAIN_BG, fg="white", font=("Arial", 20)).pack(pady=20)

    def show_tags():
        """Hiển thị trang quản lý thẻ."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Tags - Chức năng đang phát triển", 
                bg=MAIN_BG, fg="white", font=("Arial", 20)).pack(pady=20)

    def show_create_note():
        """Hiển thị trang tạo ghi chú mới."""
        show_create_note_ui(content_frame)
        
    def logout():
        """Đăng xuất và quay lại màn hình đăng nhập."""
        from gui.login_gui import show_login_screen
        show_login_screen(root, main_app)

    # Tạo menu điều hướng
    menu_items = [
        ("Home", show_home),
        ("Tasks", show_tasks),
        ("Files", show_files),
        ("Events", show_events),
        ("Tags", show_tags),
        ("Tạo ghi chú", show_create_note)
    ]

    for text, command in menu_items:
        tk.Button(sidebar, text=text, command=command, bg=SIDEBAR_BG, fg="white",
                font=("Arial", 11), relief="flat", anchor="w", padx=20,
                activebackground="#3a3a3a").pack(fill="x", pady=2)

    tk.Button(sidebar, text="Đăng xuất", command=logout,
            bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"),
            relief="flat", pady=8).pack(side="bottom", pady=20, fill="x", padx=10)

    # Mặc định khi đăng nhập hiển thị trang Home
    show_home()

# 4. Class
class NoteApp:
    """Lớp khởi tạo ứng dụng ghi chú."""
    def __init__(self):
        self.root = tk.Tk()
        
    def start(self):
        """Bắt đầu ứng dụng với màn hình đăng nhập."""
        load_notes()
        login_app = LoginApp(self.root, main_app)
        login_app.start()
        self.root.mainloop()

# 5. Hàm main
def main():
    """Hàm chính để khởi động ứng dụng."""
    app = NoteApp()
    app.start()

# 6. Điểm bắt đầu chương trình
if __name__ == "__main__":
    main()