import random
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Game Đoán Số Tương Tác", page_icon="🎮", layout="centered"
)

st.title("🎮 Game Đoán Số Tương Tác")
st.write(
    "Chọn cấp độ và bấm trực tiếp vào các ô số bên dưới để đoán. Các số không"
    " hợp lệ sẽ tự động bị khóa lại!"
)

# 1. Chọn cấp độ game (Đặt lên đầu để nhận diện cấp độ trước khi khởi tạo)
level = st.selectbox(
    "🏆 Chọn cấp độ:",
    ["Cấp 1: 1 - 100", "Cấp 2: 1 - 500", "Cấp 3: 1 - 1000"],
    index=0,
)

# Xác định max_val theo cấp độ được chọn
if "1" in level:
  target_max = 100
elif "2" in level:
  target_max = 500
else:
  target_max = 1000

# 2. Khởi tạo hoặc Reset game nếu đổi cấp độ hoặc bấm nút chơi lại
if (
    "max_val" not in st.session_state
    or st.session_state.max_val != target_max
    or "target_number" not in st.session_state
):
  st.session_state.max_val = target_max
  st.session_state.target_number = random.randint(1, target_max)
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = target_max
  st.session_state.message = (
      f"🎮 Bắt đầu ván mới với khoảng từ 1 đến {target_max}!"
  )

max_val = st.session_state.max_val

# Nút chơi lại thủ công
if st.button("🔄 Chơi ván mới / Reset"):
  st.session_state.target_number = random.randint(1, max_val)
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.session_state.message = "🔄 Đã reset ván mới. Chúc bạn may mắn!"
  st.rerun()

# Hiển thị thông báo trạng thái lượt chơi
st.markdown("---")
if st.session_state.game_over:
  st.success(st.session_state.message)
else:
  st.info(
      f"🎯 Số lần thử: {st.session_state.attempts} |"
      f" {st.session_state.message}"
  )

# 3. Bảng chọn số tương tác (Bấm trực tiếp để đoán)
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
          key=f"btn_{num}_{max_val}",
          disabled=is_disabled,
          use_container_width=True,
      ):
        st.session_state.attempts += 1

        if num == st.session_state.target_number:
          st.session_state.game_over = True
          st.session_state.message = (
              f"🎉 Chính xác! Bạn đã đoán đúng số {num} sau"
              f" {st.session_state.attempts} lần thử!"
          )
        elif num < st.session_state.target_number:
          st.session_state.message = (
              f"📈 Số {num} nhỏ hơn số bí mật! Các số từ"
              f" {st.session_state.min_limit} đến {num} đã bị loại."
          )
          if num >= st.session_state.min_limit:
            st.session_state.min_limit = num + 1
        else:
          st.session_state.message = (
              f"📉 Số {num} lớn hơn số bí mật! Các số từ {num} đến"
              f" {st.session_state.max_limit} đã bị loại."
          )
          if num <= st.session_state.max_limit:
            st.session_state.max_limit = num - 1
        st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
  st.markdown("### 💡 Hướng dẫn chơi")
  st.markdown(
      "- **Cấp độ**: Thay đổi độ khó tùy ý (Cấp 1: 1-100, Cấp 2: 1-500, Cấp"
      " 3: 1-1000)."
  )
  st.markdown(
      "- **Bảng bấm**: Bấm trực tiếp vào số để đoán. Số sai sẽ tự động mờ đi và"
      " khóa lại."
  )
  st.markdown("- **Mục tiêu**: Tìm ra con số bí mật với ít lần thử nhất.")
