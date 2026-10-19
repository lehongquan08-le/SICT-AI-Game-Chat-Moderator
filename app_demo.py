import streamlit as st
import google.generativeai as genai

# ==============================================================================
# 1. CẤU HÌNH API KEY (Thay bằng API Key của bạn)
# ==============================================================================
API_KEY = "YOUR_API_KEY_HERE"

# ==============================================================================
# 2. HƯỚNG DẪN HỆ THỐNG (SYSTEM INSTRUCTION) DÀNH CHO AI MODERATOR
# ==============================================================================
SYSTEM_INSTRUCTION = """
Bạn là một AI kiểm duyệt kênh chat của giải đấu eSports tại Việt Nam.
Nhiệm vụ của bạn là phân loại tin nhắn người xem thành 1 trong 3 nhãn:
- [Bình thường]: Những câu cổ vũ, trò chuyện lịch sự, icon cổ vũ.
- [Spam]: Nhắn link lạ, lặp lại icon/từ ngữ vô nghĩa nhiều lần làm trôi chat.
- [Toxic]: Chửi thề, dùng teencode lách luật (ví dụ: ng.u, ch.ó, t0i t3, v.l, v.ã.i), công kích cá nhân, kích war, phân biệt vùng miền.

Chỉ trả về kết quả theo đúng định dạng 2 dòng sau, không giải thích dài dòng:
Nhãn: [Bình thường / Spam / Toxic]
Lý do: [Lý do ngắn gọn trong 1 câu]
"""

# ==============================================================================
# 3. GIAO DIỆN ỨNG DỤNG STREAMLIT
# ==============================================================================
st.set_page_config(page_title="AI Moderator eSports", page_icon="🛡️", layout="centered")

st.title("🛡️ Demo AI Moderator eSports")
st.caption("Dự án: Ứng dụng AI phân tích ngữ nghĩa và teencode lách luật trong eSports - SICT AI For Game")
st.markdown("---")

# Ô nhập liệu tin nhắn từ người dùng
user_input = st.text_input(
    "Nhập tin nhắn kênh chat để kiểm tra:", 
    placeholder="Thử nhập teencode lách luật: thằ.ng này đ.ánh ngu vãiii"
)

# Nút bấm kích hoạt AI kiểm duyệt
if st.button("Kiểm duyệt bằng AI", use_container_width=True):
    if not user_input.strip():
        st.info("Vui lòng nhập nội dung tin nhắn trước khi bấm kiểm duyệt.")
    elif API_KEY == "DÁN_API_KEY_CỦA_BẠN_VÀO_ĐÂY" or len(API_KEY.strip()) < 10:
        st.error("⚠️ Bạn chưa nhập API Key vào file app_demo.py!")
    else:
        with st.spinner("AI đang phân tích ngữ cảnh và teencode..."):
            try:
                # Cấu hình API Key
                genai.configure(api_key=API_KEY.strip())
                
                # Khởi tạo mô hình Gemini 3.8 Flash
                model = genai.GenerativeModel(
                    model_name="gemini-3.8-flash",
                    system_instruction=SYSTEM_INSTRUCTION
                )
                
                # Gửi yêu cầu phân tích
                response = model.generate_content(user_input)
                result_text = response.text.strip()
                
                # Hiển thị kết quả trực quan
                if "Bình thường" in result_text:
                    st.success(f"✅ **AN TOÀN**\n\n{result_text}")
                elif "Spam" in result_text:
                    st.warning(f"⚠️ **CẢNH BÁO SPAM**\n\n{result_text}")
                else:
                    st.error(f"🚫 **VI PHẠM (TOXIC)**\n\n{result_text}")
                    
            except Exception as e:
                st.error(f"❌ Lỗi kỹ thuật chi tiết: {e}")