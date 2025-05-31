import tkinter as tk
from tkinter import ttk, messagebox
from logic import trash

MAIN_BG = "#1e1e1e"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"


def show_trash_ui(content_frame, username):
    content_frame.configure(bg=MAIN_BG)
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Thùng rác - Ghi chú đã xóa", bg=MAIN_BG,
             fg="white", font=("Arial", 16, "bold")).pack(pady=(10, 0))

    tree = ttk.Treeview(content_frame, columns=("title", "deleted_time"), show="headings", height=15)
    tree.heading("title", text="Tiêu đề")
    tree.heading("deleted_time", text="Thời điểm xóa")
    tree.column("title", width=400)
    tree.column("deleted_time", width=200)
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    selected_index = tk.IntVar(value=-1)

    def on_row_select(event):
        selected = tree.selection()
        if selected:
            selected_index.set(int(selected[0]))
        else:
            selected_index.set(-1)

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def load_table():
        tree.delete(*tree.get_children())
        trash.load_trash()
        trash_list = trash.get_trash_notes(username)
        for idx, note in enumerate(trash_list):
            tree.insert("", "end", iid=idx, values=(
                note.get("title", "Không tiêu đề"),
                note.get("deleted_time", "Không rõ")
            ))

    def restore_note():
        idx = selected_index.get()
        if idx == -1:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn ghi chú.")
            return
        if trash.restore_from_trash(username, idx):
            messagebox.showinfo("Đã khôi phục", "Ghi chú đã được khôi phục.")
            load_table()
        else:
            messagebox.showerror("Lỗi", "Không thể khôi phục ghi chú.")

    def delete_forever():
        idx = selected_index.get()
        if idx == -1:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn ghi chú.")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa vĩnh viễn ghi chú này?"):
            if trash.permanently_delete_from_trash(username, idx):
                messagebox.showinfo("Đã xóa", "Ghi chú đã bị xóa vĩnh viễn.")
                load_table()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa ghi chú.")

    action_frame = tk.Frame(content_frame, bg=MAIN_BG)
    action_frame.pack(pady=10)
    tk.Button(action_frame, text="Khôi phục", command=restore_note,
              bg=BUTTON_BG, fg="white", font=("Arial", 11), width=15).pack(side="left", padx=10)
    tk.Button(action_frame, text="Xóa vĩnh viễn", command=delete_forever,
              bg="red", fg="white", font=("Arial", 11), width=15).pack(side="left", padx=10)

    load_table()
