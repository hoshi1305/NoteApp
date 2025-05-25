# 1. 📦 Import thư viện
import tkinter as tk
import json
import os
from datetime import datetime
from tkinter import messagebox
from config import center_window, NOTES_FILE
from gui.login_gui import LoginApp
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

notes_data = []

def load_notes():
    global notes_data
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    else:
        notes_data = []

def save_notes():
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=2)

def show_create_note_ui_only(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    content_frame.configure(bg="#252525")

    tk.Label(content_frame, text="Tạo ghi chú mới", bg="#252525", fg="white", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(content_frame, text="Tiêu đề:", bg="#252525", fg="white").pack(anchor="w", padx=10)
    title_entry = tk.Entry(content_frame, font=("Arial", 12))
    title_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(content_frame, text="Nội dung:", bg="#252525", fg="white").pack(anchor="w", padx=10)
    content_text = tk.Text(content_frame, height=15, font=("Arial", 12))
    content_text.pack(fill="both", padx=10, pady=5, expand=True)

    def save_note():
        title = title_entry.get().strip() or "Không tiêu đề"
        content = content_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Thiếu nội dung", "Vui lòng nhập nội dung ghi chú.")
            return

        now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        notes_data.insert(0, {
            "title": title,
            "content": content,
            "time": now_str
        })
        save_notes()

        title_entry.delete(0, "end")
        content_text.delete("1.0", "end")
        messagebox.showinfo("Thành công", "Ghi chú đã được lưu.")

    tk.Button(content_frame, text="Lưu ghi chú", bg="#43a047", fg="white", font=("Arial", 12), command=save_note).pack(pady=10)

def main_app(root, user_email):
    root.geometry("900x600")
    center_window(root, 900, 600)
    root.configure(bg="#1e1e1e")
    for widget in root.winfo_children():
        widget.destroy()

    # Sidebar
    sidebar = tk.Frame(root, bg="#2b2b2b", width=300)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="👤", bg="#2b2b2b", fg="white",
             font=("Arial", 22, "bold")).pack(pady=15)
    tk.Label(sidebar, text=user_email, bg="#2b2b2b", fg="white",
             font=("Arial", 10), wraplength=180).pack(pady=5)

    # Content area
    content_frame = tk.Frame(root, bg="#1e1e1e")
    content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Các hàm hiển thị nội dung khi bấm menu
    def show_home():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Trang chủ", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_tasks():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Tasks - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_files():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Files - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_events():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Events - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_tags():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Tags - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_create_note():
        show_create_note_ui_only(content_frame)
        
    def logout():
        from gui.login_gui import show_login_screen
        show_login_screen(root, main_app)

    menu_items = [
        ("Home", show_home),
        ("Tasks", show_tasks),
        ("Files", show_files),
        ("Events", show_events),
        ("Tags", show_tags)
    ]

    for text, command in menu_items:
        tk.Button(sidebar, text=text, command=command, bg="#2b2b2b", fg="white",
                  font=("Arial", 11), relief="flat", anchor="w", padx=20,
                  activebackground="#3a3a3a").pack(fill="x", pady=2)

    tk.Button(sidebar, text="Đăng xuất", command=logout,
              bg="#43a047", fg="white", font=("Arial", 11, "bold"),
              relief="flat", pady=8).pack(side="bottom", pady=20, fill="x", padx=10)

    # Mặc định khi đăng nhập hiển thị trang Home
    show_home()

class NoteApp:
    def __init__(self):
        self.root = tk.Tk()
        
    def start(self):
        load_notes()
        login_app = LoginApp(self.root, main_app)
        login_app.start()
        self.root.mainloop()

def main():
    app = NoteApp()
    app.start()

if __name__ == "__main__":
    main()