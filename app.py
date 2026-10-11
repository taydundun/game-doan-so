import random
import streamlit as st

st.set_page_config(page_title="Game Đoán Số May Mắn", page_icon="🎮", layout="centered")

# Tiêu đề game
st.title("🎮 Game Đoán Số May Mắn")
st.write(
    "Tôi đã chọn một số ngẫu nhiên từ **1 đến 100**. Bạn hãy đoán xem đó là số mấy nhé!"
)

# Khởi tạo trạng thái trò chơi (session_state) để lưu giữ dữ liệu khi chơi
if "target_number" not in st.session_state:
  st.session_state.target_number = random.randint(1, 100)
  st.session_state.attempts = 0
  st.session_state.game_over = False

# Form nhập số dự đoán
with st.form("guess_form"):
  user_guess = st.number_input(
      "Nhập dự đoán của bạn:", min_value=1, max_value=100, step=1
  )
  submit_button = st.form_submit_button("Đoán ngay!")

if submit_button and not st.session_state.game_over:
  st.session_state.attempts += 1
  diff = user_guess - st.session_state.target_number

  if user_guess == st.session_state.target_number:
    st.success(
        f"🎉 Chính xác! Bạn đã đoán đúng số {st.session_state.target_number}"
        f" sau {st.session_state.attempts} lần thử!"
    )
    st.session_state.game_over = True
  elif user_guess < st.session_state.target_number:
    st.warning("📈 Số bạn đoán **nhỏ hơn** số bí mật. Hãy thử số lớn hơn!")
  else:
    st.warning("📉 Số bạn đoán **lớn hơn** số bí mật. Hãy thử số nhỏ hơn!")

# Nút chơi lại
if st.session_state.game_over:
  if st.button("🔄 Chơi ván mới"):
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
  ## Hướng dẫn chơi
  *   **Mục tiêu**: Tìm ra con số bí mật trong ít lần thử nhất.
  *   Gợi ý hệ thống sẽ cho biết bạn đang đoán thấp hơn hay cao hơn.
  *   Nhấn **Chơi ván mới** bất cứ lúc nào bạn muốn reset game.
