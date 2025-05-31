from datetime import datetime


def share_note_multiple(username, index, target_usernames):
    """Chia sẻ ghi chú với nhiều user cùng lúc."""
    from .notes import notes_data, save_notes
    from .auth import load_users  # Kiểm tra user tồn tại

    if username not in notes_data or not notes_data[username]:
        return False, "Không tìm thấy ghi chú"
    if index < 0 or index >= len(notes_data[username]):
        return False, "Chỉ mục ghi chú không hợp lệ"

    # Kiểm tra danh sách user tồn tại
    users = load_users()
    existing_users = [user["username"] for user in users]

    success_users = []
    failed_users = []

    for target_username in target_usernames:
        if target_username not in existing_users:
            failed_users.append(target_username)
            continue

        note = notes_data[username][index].copy()
        note["shared_from"] = username
        note["shared_time"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        note["shared_to"] = target_username

        if target_username not in notes_data:
            notes_data[target_username] = []
        notes_data[target_username].insert(0, note)
        success_users.append(target_username)

    save_notes()

    if success_users:
        return True, f"Chia sẻ thành công với: {', '.join(success_users)}"
    else:
        return (
            False,
            f"Không thể chia sẻ. User không tồn tại: {', '.join(failed_users)}",
        )


def get_shared_notes(username):
    """Lấy danh sách ghi chú được chia sẻ đến user."""
    from .notes import notes_data

    if username not in notes_data:
        return []

    shared_notes = []
    for note in notes_data[username]:
        if "shared_from" in note:
            shared_notes.append(note)
    return shared_notes


def unshare_note(username, index, target_username):
    """Hủy chia sẻ ghi chú với user cụ thể."""
    from .notes import notes_data, save_notes

    if target_username not in notes_data:
        return False, "User không tồn tại"

    # Tìm và xóa ghi chú được share từ username
    for i, note in enumerate(notes_data[target_username]):
        if note.get("shared_from") == username:
            # So sánh title và content để đảm bảo đúng note
            original_note = notes_data[username][index]
            if (
                note["title"] == original_note["title"]
                and note["content"] == original_note["content"]
            ):
                notes_data[target_username].pop(i)
                save_notes()
                return True, f"Đã hủy chia sẻ với {target_username}"

    return False, "Không tìm thấy ghi chú đã chia sẻ"
