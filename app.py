import random
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Game Ra Đề & Đoán Số 2 Người", page_icon="🎮", layout="centered"
)

st.title("🎮 Game Ra Đề & Đoán Số 2 Người")
st.write(
    "Một người sẽ ra đề (chọn số bí mật), người kia nhắm mắt lại đoán. Sau đó"
    " đổi vai cho nhau xem ai đoán ít lần hơn!"
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

# 2. Khởi tạo trạng thái an toàn
if "max_val" not in st.session_state or st.session_state.max_val != current_max:
  st.session_state.max_val = current_max
  st.session_state.secret_setter = (
      "Người chơi 1"  # Người ra đề (chọn số bí mật)
  )
  st.session_state.secret_guesser = (
      "Người chơi 2"  # Người đoán số
  )
  st.session_state.step = (
      "setting"  # Giai đoạn: 'setting' (chọn số) hoặc 'guessing' (đoán số)
  )
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = current_max
  st.session_state.message = ""

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

# GIAO DIỆN 1: NGƯỜI RA ĐỀ CHỌN SỐ BÍ MẬT (NGƯỜI ĐOÁN PHẢI NHẮM MẮT)
if st.session_state.step == "setting":
  st.info(
      f"🎯 **Lượt ra đề**: **{st.session_state.secret_setter}** sẽ chọn số bí"
      f" mật."
  )
  st.warning(
      f"🙈 **{st.session_state.secret_guesser}** hãy **NHẮM MẮT LẠI** hoặc quay"
      " đi để không nhìn thấy số được chọn!"
  )

  with st.form("set_secret_form"):
    chosen_num = st.number_input(
        f"{st.session_state.secret_setter}, nhập con số bí mật từ 1 đến"
        f" {max_val}:",
        min_value=1,
        max_value=max_val,
        step=1,
    )
    submitted = st.form_submit_button(
        "🔒 Xác nhận số bí mật & Cho phép mở mắt"
    )

    if submitted:
      st.session_state.target_number = chosen_num
      st.session_state.step = "guessing"
      st.session_state.attempts = 0
      st.session_state.min_limit = 1
      st.session_state.max_limit = max_val
      st.session_state.message = (
          f"🎮 Bắt đầu! **{st.session_state.secret_guesser}** hãy đoán số mà"
          f" **{st.session_state.secret_setter}** vừa chọn."
      )
      st.rerun()

# GIAO DIỆN 2: NGƯỜI ĐOÁN SỐ TRÊN BẢNG TƯƠNG TÁC
elif st.session_state.step == "guessing":
  st.success(f"👀 **{st.session_state.secret_guesser}** đã mở mắt và bắt đầu đoán!")
  st.info(
      f"🎯 Số lần thử của {st.session_state.secret_guesser}:"
      f" {st.session_state.attempts} | {st.session_state.message}"
  )

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
            key=f"guess_btn_{max_val}_{num}",
            disabled=is_disabled,
            use_container_width=True,
        ):
          st.session_state.attempts += 1

          if num == st.session_state.target_number:
            st.session_state.game_over = True
            st.session_state.message = (
                f"🎉 Chúc mừng **{st.session_state.secret_guesser}** đã đoán"
                f" đúng số {num} sau {st.session_state.attempts} lần thử! 🏆"
            )
          elif num < st.session_state.target_number:
            st.session_state.message = (
                f"📈 Số {num} nhỏ hơn số bí mật! Các số nhỏ hơn hoặc bằng"
                f" {num} đã bị loại."
            )
            if num >= st.session_state.min_limit:
              st.session_state.min_limit = num + 1
          else:
            st.session_state.message = (
                f"📉 Số {num} lớn hơn số bí mật! Các số lớn hơn hoặc bằng"
                f" {num} đã bị loại."
            )
            if num <= st.session_state.max_limit:
              st.session_state.max_limit = num - 1
          st.rerun()

  # Nếu đã đoán trúng, hiển thị nút đổi vai để chơi ngược lại
  if st.session_state.game_over:
    st.balloons()
    if st.button(
        "🔄 Đổi vai trò (Người đoán thành người ra đề)",
        use_container_width=True,
    ):
      # Đổi vai cho nhau
      (
          st.session_state.secret_setter,
          st.session_state.secret_guesser,
      ) = (
          st.session_state.secret_guesser,
          st.session_state.secret_setter,
      )
      st.session_state.step = "setting"
      st.session_state.target_number = None
      st.session_state.attempts = 0
      st.session_state.game_over = False
      st.session_state.min_limit = 1
      st.session_state.max_limit = max_val
      st.session_state.message = ""
      st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
  st.markdown("### 💡 Hướng dẫn chơi Ra Đề & Đoán")
  st.markdown(
      "- **Bước 1**: Người ra đề chọn một số bí mật (người kia phải nhắm mắt"
      " lại)."
  )
  st.markdown(
      "- **Bước 2**: Người đoán mở mắt và bấm các ô số trên bảng. Số sai sẽ"
      " tự động mờ đi."
  )
  st.markdown(
      "- **Bước 3**: Khi đoán trúng, hai bạn có thể bấm **Đổi vai** để thi xem"
      " ai đoán nhanh hơn!"
  )
