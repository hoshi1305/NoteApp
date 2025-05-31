import tkinter as tk
from tkinter import messagebox, simpledialog
from logic.notes import load_notes, save_notes, notes_data
from logic import notes, trash
from config import center_window
from gui.login_gui import LoginApp
from gui.notes_gui import show_create_note_ui, clear_frame

MAIN_BG = "#1e1e1e"
SIDEBAR_BG = "#2b2b2b"
BUTTON_BG = "#43a047"
BUTTON_FG = "white"

def main_app(root, username):
    root.geometry("900x600")
    center_window(root, 900, 600)
    root.configure(bg=MAIN_BG)
    clear_frame(root)

    sidebar = tk.Frame(root, bg=SIDEBAR_BG, width=300)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="Người dùng", bg=SIDEBAR_BG, fg="white",
             font=("Arial", 14, "bold")).pack(pady=15)
    tk.Label(sidebar, text=username, bg=SIDEBAR_BG, fg="white",
             font=("Arial", 10), wraplength=180).pack(pady=5)

    content_frame = tk.Frame(root, bg=MAIN_BG)
    content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def show_home():
        clear_frame(content_frame)
        from tkinter import ttk

        btn_frame = tk.Frame(content_frame, bg=MAIN_BG)
        btn_frame.pack(fill="x", pady=(10, 5))
        btn_inner = tk.Frame(btn_frame, bg=MAIN_BG)
        btn_inner.pack(anchor="center")

        tk.Button(btn_inner, text="Thêm ghi chú", command=show_create_note,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=0, padx=10)

        tk.Button(btn_inner, text="Sửa ghi chú", command=lambda: edit_selected_note(),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=1, padx=10)

        tk.Button(btn_inner, text="Xóa ghi chú", command=lambda: delete_selected_note(),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), width=15).grid(row=0, column=2, padx=10)

        search_frame = tk.Frame(content_frame, bg=MAIN_BG)
        search_frame.pack(pady=(5, 15))
        search_var = tk.StringVar()
        tk.Label(search_frame, text="Tìm kiếm:", bg=MAIN_BG, fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=8)
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40, font=("Arial", 12))
        search_entry.pack(side="left", padx=10, ipady=4)
        tk.Button(search_frame, text="Tìm", command=lambda: load_table(search_var.get().strip()),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"), padx=10, pady=2).pack(side="left", padx=8)

        table_frame = tk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(table_frame, columns=("title", "created", "updated"), show="headings", height=15, yscrollcommand=scrollbar.set)
        tree.heading("title", text="Tên ghi chú")
        tree.heading("created", text="Ngày tạo")
        tree.heading("updated", text="Lần sửa cuối")
        tree.column("title", width=250)
        tree.column("created", width=150)
        tree.column("updated", width=150)
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        selected_index = tk.IntVar(value=-1)
        displayed_notes = []

        def on_row_select(event):
            selected = tree.selection()
            if selected:
                selected_index.set(int(selected[0]))
            else:
                selected_index.set(-1)

        tree.bind("<<TreeviewSelect>>", on_row_select)

        def load_table(keyword=""):
            nonlocal displayed_notes
            displayed_notes = []
            tree.delete(*tree.get_children())
            notes_list = notes.notes_data.get(username, [])
            for idx, note in enumerate(notes_list):
                if keyword.lower() in note.get("title", "").lower() or keyword.lower() in note.get("content", "").lower():
                    tree.insert("", "end", iid=str(len(displayed_notes)), values=(
                        note.get("title", "Không tiêu đề"),
                        note.get("created_time", "Không rõ"),
                        note.get("updated_time", "Không rõ")
                    ))
                    displayed_notes.append((idx, note))

        def delete_selected_note():
            idx = selected_index.get()
            if idx == -1 or idx >= len(displayed_notes):
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn ghi chú.")
                return
            real_index = displayed_notes[idx][0]
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa ghi chú này?"):
                if trash.move_to_trash(username, real_index):
                    messagebox.showinfo("Đã xóa", "Ghi chú đã được đưa vào thùng rác.")
                    load_table()
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa ghi chú.")

        def edit_selected_note():
            idx = selected_index.get()
            if idx == -1 or idx >= len(displayed_notes):
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn ghi chú.")
                return
            real_index = displayed_notes[idx][0]
            note = notes.notes_data[username][real_index]

            clear_frame(content_frame)
            tk.Label(content_frame, text="Sửa ghi chú", bg=MAIN_BG,
                     fg="white", font=("Arial", 16, "bold")).pack(pady=10)

            tk.Label(content_frame, text="Tiêu đề:", bg=MAIN_BG, fg="white").pack(anchor="w", padx=10)
            title_entry = tk.Entry(content_frame, font=("Arial", 12))
            title_entry.insert(0, note["title"])
            title_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(content_frame, text="Nội dung:", bg=MAIN_BG, fg="white").pack(anchor="w", padx=10)
            content_text = tk.Text(content_frame, height=15, font=("Arial", 12))
            content_text.insert("1.0", note["content"])
            content_text.pack(fill="both", padx=10, pady=5, expand=True)

            def save_update():
                new_title = title_entry.get()
                new_content = content_text.get("1.0", "end").strip()
                if notes.update_note(username, real_index, new_title, new_content):
                    messagebox.showinfo("Thành công", "Ghi chú đã được cập nhật.")
                    show_home()
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật ghi chú.")

            tk.Button(content_frame, text="Lưu", command=save_update,
                      bg=BUTTON_BG, fg="white", font=("Arial", 12), width=15).pack(pady=10)

        load_table()

    def show_trash():
        clear_frame(content_frame)
        from tkinter import ttk

        tk.Label(content_frame, text="🗑️ Thùng rác - Ghi chú đã xóa", bg=MAIN_BG,
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

    def show_create_note():
        show_create_note_ui(content_frame, username)

    def logout():
        from gui.login_gui import show_login_screen
        show_login_screen(root, main_app)

    menu_items = [
        ("Trang chủ", show_home),
        ("Thùng rác", show_trash),
    ]

    for text, command in menu_items:
        tk.Button(sidebar, text=text, command=command, bg=SIDEBAR_BG, fg="white",
                  font=("Arial", 11), relief="flat", anchor="w", padx=20,
                  activebackground="#3a3a3a").pack(fill="x", pady=2)

    tk.Button(sidebar, text="Đăng xuất", command=logout,
              bg=BUTTON_BG, fg=BUTTON_FG, font=("Arial", 11, "bold"),
              relief="flat", pady=8).pack(side="bottom", pady=20, fill="x", padx=10)

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
