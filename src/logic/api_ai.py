import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

# Cấu hình API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# Hàm xử lý logic AI
def get_gemini_response(prompt_text):
    """Gửi prompt đến Gemini và nhận phản hồi."""
    if not GEMINI_API_KEY:
        return "Không có API Key. Vui lòng cấu hình trong file .env"

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt_text)

        if not response.candidates:
            return "AI không thể xử lý yêu cầu này."

        return response.text
    except Exception as e:
        return f"Lỗi khi gọi API: {e}"


def summarize_text_ai(text_content, num_sentences=3):
    """Tóm tắt văn bản (chỉ admin)."""
    if not text_content.strip():
        return "Nội dung trống, không có gì để tóm tắt."

    prompt = (
        f"Hãy tóm tắt đoạn văn bản sau đây một cách ngắn gọn và súc tích trong khoảng {num_sentences} câu. "
        f"Chỉ trả về phần nội dung tóm tắt, không thêm bất kỳ lời dẫn, giải thích hay câu mở đầu/kết thúc nào khác.\n\n"
        f"---\n{text_content}\n---"
    )
    return get_gemini_response(prompt)


def suggest_title_ai(text_content, num_suggestions=3):
    """Gợi ý tiêu đề."""
    if not text_content.strip():
        return []

    prompt = (
        f"Dựa vào nội dung văn bản dưới đây, hãy gợi ý {num_suggestions} tiêu đề thật hấp dẫn, ngắn gọn và phù hợp. "
        f"Mỗi tiêu đề trên một dòng riêng biệt. Chỉ trả về các tiêu đề, không thêm bất kỳ lời giải thích hay câu dẫn nào khác.\n\n"
        f"---\n{text_content}\n---"
    )
    suggestions_text = get_gemini_response(prompt)

    if (
        suggestions_text
        and "Lỗi" not in suggestions_text
        and "API Key" not in suggestions_text
    ):
        return [
            line.strip()
            for line in suggestions_text.strip().split("\n")
            if line.strip()
        ]
    return []


def format_text_ai(text_content):
    """Định dạng văn bản."""
    if not text_content.strip():
        return "Văn bản rỗng."

    prompt = (
        "Hãy định dạng lại đoạn văn bản sau đây để dễ đọc, có cấu trúc rõ ràng và mạch lạc. "
        "Nếu nội dung có các ý liệt kê hoặc các bước tuần tự, hãy sử dụng danh sách có thứ tự (ví dụ: 1., 2., 3.). "
        "Nếu trong một mục lớn có thứ tự (ví dụ: mục 1.) có các mục con, hãy sử dụng cách đánh số phụ (ví dụ: 1.1., 1.2.). "
        "Với các ý không theo thứ tự rõ ràng nhưng cần liệt kê thành danh sách, hãy sử dụng dấu gạch đầu dòng ('- '). "
        "Nếu một mục được đánh dấy bằng gạch đầu dòng ('- ') lại có các ý con chi tiết hơn, hãy sử dụng dấu cộng ('+ ') để thụt vào và đánh dấu các ý con đó. Ví dụ:\n"
        "- Ý chính dùng gạch đầu dòng\n"
        "  + Ý con đầu tiên của gạch đầu dòng\n"
        "  + Ý con thứ hai của gạch đầu dòng\n"
        "Sử dụng các đoạn văn ngắn và xuống dòng hợp lý cho các phần văn xuôi. "
        "Quan trọng: Giữ nguyên là văn bản thuần túy, không sử dụng cú pháp Markdown phức tạp (ví dụ: không dùng ### hay **). "
        "Chỉ trả về nội dung đã được định dạng, không thêm bất kỳ lời giới thiệu, giải thích hay bình luận nào.\n\n"
        f"---\n{text_content}\n---"
    )
    return get_gemini_response(prompt)


# Phân quyền AI theo role
def get_available_ai_features(username):
    """Trả về danh sách tính năng AI theo quyền user."""
    from .auth import is_admin

    if is_admin(username):
        return {
            "summarize": True,  # Chỉ admin
            "suggest_title": True,
            "format_text": True,
        }
    else:
        return {
            "summarize": False,  # User thường không được
            "suggest_title": True,
            "format_text": True,
        }


def check_ai_permission(username, feature):
    """Kiểm tra quyền sử dụng tính năng AI."""
    features = get_available_ai_features(username)
    return features.get(feature, False)
