# Import thư viện
import tkinter as tk
from tkinter import messagebox
from logic.notes import add_note

# Hằng số cấu hình
CONTENT_BG = "#252525"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"

# Hàm tiện ích
def clear_frame(frame):
    """Xóa tất cả widget trong một frame."""
    for widget in frame.winfo_children():
        widget.destroy()

# Hàm xử lý giao diện
def show_create_note_ui(content_frame):
    """Hiển thị giao diện tạo ghi chú mới."""
    clear_frame(content_frame)
    content_frame.configure(bg=CONTENT_BG)

    tk.Label(content_frame, text="Tạo ghi chú mới", bg=CONTENT_BG, 
            fg="white", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(content_frame, text="Tiêu đề:", bg=CONTENT_BG, fg="white").pack(anchor="w", padx=10)
    title_entry = tk.Entry(content_frame, font=("Arial", 12))
    title_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(content_frame, text="Nội dung:", bg=CONTENT_BG, fg="white").pack(anchor="w", padx=10)
    content_text = tk.Text(content_frame, height=15, font=("Arial", 12))
    content_text.pack(fill="both", padx=10, pady=5, expand=True)

    def save_note():
        """Lưu ghi chú mới vào danh sách và file."""
        title = title_entry.get()
        content = content_text.get("1.0", "end")
        
        if add_note(title, content):
            title_entry.delete(0, "end")
            content_text.delete("1.0", "end")
            messagebox.showinfo("Thành công", "Ghi chú đã được lưu.")
        else:
            messagebox.showwarning("Thiếu nội dung", "Vui lòng nhập nội dung ghi chú.")

    tk.Button(content_frame, text="Lưu ghi chú", bg=BUTTON_BG, fg=BUTTON_FG, 
            font=("Arial", 12), command=save_note).pack(pady=10)
