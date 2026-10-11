import random
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Game Đoán Số 2 Người", page_icon="🎮", layout="centered"
)

st.title("🎮 Game Đoán Số 2 Người (Chơi Chung Máy)")
st.write(
    "Hai người chơi luân phiên nhau chọn số trên bảng. Ai bấm trúng số bí"
    " mật trước sẽ giành chiến thắng!"
)

# 1. Chọn cấp độ game
level = st.selectbox(
    "🏆 Chọn cấp độ:",
    ["Cấp 1: 1 - 100", "Cấp 2: 1 - 500", "Cấp 3: 1 - 1000"],
    key="selected_level",
)

if "Cấp 1" in level:
  current_max = 100
elif "Cấp 2" in level:
  current_max = 500
else:
  current_max = 1000

# 2. Khởi tạo trạng thái game hoặc reset khi đổi cấp độ
if "max_val" not in st.session_state or st.session_state.max_val != current_max:
  st.session_state.max_val = current_max
  st.session_state.target_number = random.randint(1, current_max)
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = current_max
  st.session_state.turn = "Người chơi 1"
  st.session_state.message = (
      "🎮 Trò chơi bắt đầu! Lượt đầu tiên thuộc về **Người chơi 1 🔴**."
  )

max_val = st.session_state.max_val

# Nút chơi lại thủ công
if st.button("🔄 Chơi ván mới / Reset"):
  st.session_state.target_number = random.randint(1, max_val)
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.session_state.turn = "Người chơi 1"
  st.session_state.message = (
      "🔄 Đã reset ván mới! Lượt đầu tiên thuộc về **Người chơi 1 🔴**."
  )
  st.rerun()

# Hiển thị thông báo lượt chơi hiện tại
st.markdown("---")
if st.session_state.game_over:
  st.success(st.session_state.message)
else:
  turn_icon = "🔴" if st.session_state.turn == "Người chơi 1" else "🔵"
  st.info(
      f"{turn_icon} **Lượt hiện tại: {st.session_state.turn}** |"
      f" {st.session_state.message}"
  )

# 3. Bảng chọn số tương tác cho 2 người
st.subheader(
    f"📊 Bảng Chọn Số (Khoảng hợp lệ: {st.session_state.min_limit} đến"
    f" {st.session_state.max_limit})"
)

cols_per_row = 10
numbers = list(range(1, max_val + 1))

for i in range(0, len(numbers), cols_per_row):
  row_nums = numbers[i : i + cols_per_row]
  cols = st.columns(cols_per_row)
  for idx, num in enumerate(row_nums):
    with cols[idx]:
      is_disabled = (
          num < st.session_state.min_limit
          or num > st.session_state.max_limit
          or st.session_state.game_over
      )

      if st.button(
          str(num),
          key=f"btn_2p_{max_val}_{num}",
          disabled=is_disabled,
          use_container_width=True,
      ):
        current_player = st.session_state.turn

        if num == st.session_state.target_number:
          st.session_state.game_over = True
          st.session_state.message = (
              f"🎉 Chúc mừng **{current_player}** đã bấm trúng số {num} và giành"
              " chiến thắng tuyệt đối! 🏆"
          )
        else:
          if num < st.session_state.target_number:
            hint = "nhỏ hơn"
            if num >= st.session_state.min_limit:
              st.session_state.min_limit = num + 1
          else:
            hint = "lớn hơn"
            if num <= st.session_state.max_limit:
              st.session_state.max_limit = num - 1

          # Đổi lượt cho người chơi tiếp theo
          next_player = (
              "Người chơi 2"
              if current_player == "Người chơi 1"
              else "Người chơi 1"
          )
          st.session_state.turn = next_player
          st.session_state.message = (
              f"❌ **{current_player}** chọn số {num} (Số bí mật **{hint}** số"
              f" này). Đổi lượt cho **{next_player}**!"
          )
        st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
  st.markdown("### 💡 Hướng dẫn chơi 2 người")
  st.markdown(
      "- **Chế độ**: Hai người dùng chung một máy, luân phiên nhau bấm chọn"
      " số."
  )
  st.markdown(
      "- **Đổi lượt**: Nếu đoán sai, hệ thống sẽ gợi ý lớn/nhỏ và tự động chuyển"
      " lượt cho người còn lại."
  )
  st.markdown(
      "- **Chiến thắng**: Ai bấm trúng con số bí mật cuối cùng sẽ chiến"
      " thắng!"
  )
