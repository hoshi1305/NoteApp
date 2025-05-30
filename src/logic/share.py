import datetime

def share_note(username, index, target_username):
    """Chia sẻ ghi chú với user khác."""
    from .notes import notes_data, save_notes
    
    if username not in notes_data or not notes_data[username]:
        return False, "Không tìm thấy ghi chú"
    if index < 0 or index >= len(notes_data[username]):
        return False, "Chỉ mục ghi chú không hợp lệ"
    
    note = notes_data[username][index].copy()
    note["shared_from"] = username
    note["shared_time"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    
    if target_username not in notes_data:
        notes_data[target_username] = []
    notes_data[target_username].insert(0, note)
    
    save_notes()
    return True, "Chia sẻ ghi chú thành công"