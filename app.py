import streamlit as st

st.set_page_config(
    page_title="Game Đoán Số - Thầy Chọn Lớp Đoán",
    page_icon="👨‍🏫",
    layout="centered",
)

st.title("👨‍🏫 Game Đoán Số (Thầy Chọn - Lớp Đoán)")
st.write(
    "Hãy chọn số bí mật, sau đó mọi người sẽ cùng nhau đoán trên bảng tương"
    " tác!"
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

# 2. Khởi tạo trạng thái game
if "max_val" not in st.session_state or st.session_state.max_val != current_max:
  st.session_state.max_val = current_max
  st.session_state.step = "setting"
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = current_max

max_val = st.session_state.max_val

# Nút chơi lại / Đổi số mới
if st.button("🔄 Chọn số mới (Ván mới)"):
  st.session_state.step = "setting"
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.rerun()

st.markdown("---")

# GIAO DIỆN 1: NHẬP SỐ BÍ MẬT
if st.session_state.step == "setting":
  st.info("🎯 **Hãy chọn số** bí mật bên dưới.")
  st.warning("🙈 Mọi người hãy **nhắm mắt lại** để giữ bí mật!")

  with st.form("setter_form"):
    chosen_num = st.number_input(
        f"Hãy chọn số (từ 1 đến {max_val}):",
        min_value=1,
        max_value=max_val,
        step=1,
    )
    submitted = st.form_submit_button(
        "🔒 Khóa số bí mật & Mời mọi người mở mắt đoán!"
    )

    if submitted:
      st.session_state.target_number = chosen_num
      st.session_state.step = "guessing"
      st.session_state.attempts = 0
      st.session_state.min_limit = 1
      st.session_state.max_limit = max_val
      st.rerun()

# GIAO DIỆN 2: ĐOÁN SỐ TRÊN BẢNG TƯƠNG TÁC
elif st.session_state.step == "guessing":
  st.success("👀 Mọi người đã mở mắt! Hãy cùng nhau bấm chọn số để đoán.")
  st.info(f"🎯 Số lần đã đoán: {st.session_state.attempts}")

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
            st.success(
                f"🎉 CHÍNH XÁC! Đã tìm ra số bí mật **{num}** sau"
                f" {st.session_state.attempts} lần thử! 🏆"
            )
          elif num < st.session_state.target_number:
            st.session_state.min_limit = num + 1
          else:
            st.session_state.max_limit = num - 1
          st.rerun()

  if st.session_state.game_over:
    st.balloons()
    if st.button("🔄 Hãy chọn số mới cho ván tiếp theo", use_container_width=True):
      st.session_state.step = "setting"
      st.session_state.game_over = False
      st.rerun()
