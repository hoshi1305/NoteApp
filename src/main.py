import tkinter as tk
import sys
import os
from config import center_window
from gui.login_gui import LoginApp
from gui.notes_gui import show_create_note_ui, clear_frame
from logic.notes import load_notes, save_notes, notes_data
from logic.share import share_note_multiple, get_shared_notes
from tkinter import messagebox, simpledialog

# Thêm đường dẫn gốc vào sys.path để import đúng
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Hằng số cấu hình
MAIN_BG = "#1e1e1e"
SIDEBAR_BG = "#2b2b2b"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"

# Hàm xử lý giao diện
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
        """Hiển thị trang chủ với 3 nút chức năng trên, thanh tìm kiếm dưới, rồi danh sách ghi chú."""
        clear_frame(content_frame)

        # Khung chứa 3 nút Thêm, Sửa, Xóa - căn phải
        btn_frame = tk.Frame(content_frame, bg=MAIN_BG)
        btn_frame.pack(fill="x", pady=(10, 5))  # full width, dễ căn phải

        btn_inner_frame = tk.Frame(btn_frame, bg=MAIN_BG)
        btn_inner_frame.pack(anchor="e", padx=20)  # căn phải

        tk.Button(btn_inner_frame, text="Thêm ghi chú", command=show_create_note,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=0, padx=5)

        tk.Button(btn_inner_frame, text="Sửa ghi chú", command=lambda: print("Chức năng sửa ghi chú"),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=1, padx=5)

        tk.Button(btn_inner_frame, text="Xóa ghi chú", command=lambda: print("Chức năng xóa ghi chú"),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=2, padx=5)

        # Thanh tìm kiếm lớn bên dưới các nút
        search_frame = tk.Frame(content_frame, bg=MAIN_BG)
        search_frame.pack(pady=(5, 15))

        tk.Label(search_frame, text="Tìm kiếm:", bg=MAIN_BG, fg="white",
                 font=("Arial", 12, "bold")).pack(side="left", padx=8)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40,
                                font=("Arial", 12))
        search_entry.pack(side="left", padx=10, ipady=4)

        def perform_search():
            keyword = search_var.get().strip()
            display_notes(keyword)

        tk.Button(search_frame, text="Tìm", command=perform_search,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), padx=10, pady=2).pack(side="left", padx=8)

        # Khung chứa danh sách ghi chú
        notes_list_frame = tk.Frame(content_frame, bg=MAIN_BG)
        notes_list_frame.pack(fill="both", expand=True, pady=10)

        def display_notes(keyword=""):
            for widget in notes_list_frame.winfo_children():
                widget.destroy()

            user_notes = notes_data.get(username, [])
            filtered_notes = [
                note for note in user_notes
                if (keyword.lower() in note.get("title", "").lower() or
                    keyword.lower() in note.get("content", "").lower())
                   and not note.get("deleted", False)
            ]

            if not filtered_notes:
                tk.Label(notes_list_frame, text="Không tìm thấy ghi chú nào.", bg=MAIN_BG, fg="gray").pack(pady=10)
                return

            for idx, note in enumerate(filtered_notes):
                note_frame = tk.Frame(notes_list_frame, bg="#2b2b2b", pady=8, padx=10)
                note_frame.pack(fill="x", pady=5, padx=20)

                tk.Label(note_frame, text=note.get("title", "Không có tiêu đề"),
                         bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w")

                tk.Label(note_frame, text=note.get("content", "")[:100] + "...",
                         bg="#2b2b2b", fg="white", anchor="w", justify="left", wraplength=600).pack(anchor="w", pady=2)

                def create_share_callback(index=user_notes.index(note)):
                    def share():
                        target_user = simpledialog.askstring("Chia sẻ ghi chú", "Nhập tên người dùng để chia sẻ:")
                        if target_user:
                            success, msg = share_note_multiple(username, index, target_user)
                            if success:
                                messagebox.showinfo("Thành công", msg)
                            else:
                                messagebox.showerror("Lỗi", msg)

                    return share

                tk.Button(note_frame, text="Chia sẻ", command=create_share_callback(),
                          bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 10), width=10).pack(anchor="e", pady=5)

        display_notes()

    def show_trash():
        """Hiển thị thùng rác."""
        clear_frame(content_frame)
        tk.Label(content_frame, text="Thùng rác - Chức năng đang phát triển",
                bg=MAIN_BG, fg="white", font=("Arial", 20)).pack(pady=20)

    def show_share():
        """Hiển thị ghi chú được chia sẻ với thanh tìm kiếm và danh sách như trang chủ."""
        clear_frame(content_frame)

        # Thanh tìm kiếm (bên dưới giống trang chủ)
        search_frame = tk.Frame(content_frame, bg=MAIN_BG)
        search_frame.pack(pady=(10, 15))

        tk.Label(search_frame, text="Tìm kiếm:", bg=MAIN_BG, fg="white",
                 font=("Arial", 12, "bold")).pack(side="left", padx=8)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                                width=40, font=("Arial", 12))
        search_entry.pack(side="left", padx=10, ipady=4)

        def perform_search():
            keyword = search_var.get().strip()
            display_shared_notes(keyword)

        tk.Button(search_frame, text="Tìm", command=perform_search,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"),
                  padx=10, pady=2).pack(side="left", padx=8)

        # Khung chứa danh sách ghi chú chia sẻ (giống trang chủ)
        shared_notes_frame = tk.Frame(content_frame, bg=MAIN_BG)
        shared_notes_frame.pack(fill="both", expand=True, pady=10)

        def display_shared_notes(keyword=""):
            for widget in shared_notes_frame.winfo_children():
                widget.destroy()

            shared_notes_multiple = get_shared_notes(username)

            filtered_notes = [
                note for note in shared_notes_multiple
                if keyword.lower() in note.get("title", "").lower()
                   or keyword.lower() in note.get("content", "").lower()
            ]

            if not filtered_notes:
                tk.Label(shared_notes_frame, text="Không có ghi chú được chia sẻ.",
                         bg=MAIN_BG, fg="gray", font=("Arial", 11)).pack(pady=10)
                return

            for note in filtered_notes:
                note_frame = tk.Frame(shared_notes_frame, bg="#2b2b2b", pady=8, padx=10)
                note_frame.pack(fill="x", pady=5, padx=20)

                # Tiêu đề
                tk.Label(note_frame, text=note.get("title", "Không có tiêu đề"),
                         bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w")

                # Nội dung (rút gọn 100 ký tự)
                tk.Label(note_frame, text=note.get("content", "")[:100] + "...",
                         bg="#2b2b2b", fg="white", anchor="w",
                         justify="left", wraplength=600).pack(anchor="w", pady=2)

        # Hiển thị ghi chú khi mở giao diện
        display_shared_notes()

    def show_create_note():
        """Hiển thị trang tạo ghi chú mới."""
        show_create_note_ui(content_frame)
        
    def logout():
        """Đăng xuất và quay lại màn hình đăng nhập."""
        from gui.login_gui import show_login_screen
        show_login_screen(root, main_app)

    # Tạo menu điều hướng
    menu_items = [
        ("Trang chủ", show_home),
        ("Chia sẽ ghi chú", show_share),
        ("Thùng rác",show_trash)
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

# Class
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

# Hàm main
def main():
    """Hàm chính để khởi động ứng dụng."""
    app = NoteApp()
    app.start()

# Điểm bắt đầu chương trình
if __name__ == "__main__":
    main()
