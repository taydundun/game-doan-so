import random
import streamlit as st

st.set_page_config(
    page_title="Game Ra Đề & Đoán Số", page_icon="🎮", layout="centered"
)

st.title("🎮 Game Ra Đề & Đoán Số 2 Người")
st.write(
    "Một người ra đề chọn số bí mật (người kia nhắm mắt), sau đó người kia mở"
    " mắt đoán số trên bảng!"
)

# Chọn cấp độ
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

# Khởi tạo trạng thái game
if "max_val" not in st.session_state or st.session_state.max_val != current_max:
  st.session_state.max_val = current_max
  st.session_state.step = "setting"
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = current_max

max_val = st.session_state.max_val

# Nút reset ván mới
if st.button("🔄 Chơi ván mới / Reset"):
  st.session_state.step = "setting"
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.rerun()

st.markdown("---")

# Giai đoạn 1: Người ra đề chọn số (người đoán nhắm mắt)
if st.session_state.step == "setting":
  st.info("🎯 **Lượt ra đề**: Người chơi 1 hãy chọn số bí mật.")
  st.warning("🙈 Người chơi 2 hãy **NHẮM MẮT LẠI** để giữ bí mật!")

  with st.form("set_form"):
    chosen = st.number_input(
        f"Nhập số bí mật từ 1 đến {max_val}:",
        min_value=1,
        max_value=max_val,
        step=1,
    )
    if st.form_submit_button("🔒 Xác nhận số & Cho phép mở mắt"):
      st.session_state.target_number = chosen
      st.session_state.step = "guessing"
      st.session_state.attempts = 0
      st.session_state.min_limit = 1
      st.session_state.max_limit = max_val
      st.rerun()

# Giai đoạn 2: Người đoán mở mắt chọn số trên bảng
elif st.session_state.step == "guessing":
  st.success("👀 Người đoán đã mở mắt và bắt đầu thử thách!")
  st.info(f"🎯 Số lần thử: {st.session_state.attempts}")

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
            key=f"btn_{max_val}_{num}",
            disabled=is_disabled,
            use_container_width=True,
        ):
          st.session_state.attempts += 1
          if num == st.session_state.target_number:
            st.session_state.game_over = True
            st.success(
                f"🎉 Chính xác! Bạn đã đoán đúng số {num} sau"
                f" {st.session_state.attempts} lần thử!"
            )
          elif num < st.session_state.target_number:
            st.session_state.min_limit = num + 1
          else:
            st.session_state.max_limit = num - 1
          st.rerun()

  if st.session_state.game_over:
    st.balloons()
    if st.button("🔄 Chơi ván mới (Đổi người ra đề)", use_container_width=True):
      st.session_state.step = "setting"
      st.session_state.game_over = False
      st.rerun()
