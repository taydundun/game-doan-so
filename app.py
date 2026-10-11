import random
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Game Đoán Số 2 Người", page_icon="🎮", layout="centered"
)

st.title("🎮 Game Đoán Số 2 Người (Bí Mật & Chơi Chung Máy)")
st.write(
    "Hai người chơi luân phiên nhau chọn số. Khi đến lượt ai, người kia phải"
    " **nhắm mắt lại/quay đi** để đảm bảo bí mật!"
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

# 2. Khởi tạo toàn bộ session_state an toàn để tránh mọi lỗi KeyError
if "max_val" not in st.session_state or st.session_state.max_val != current_max:
  st.session_state.max_val = current_max
  st.session_state.target_number = random.randint(1, current_max)
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = current_max
  st.session_state.turn = "Người chơi 1"
  st.session_state.show_board = False  # Trạng thái ẩn/hiện bảng chọn để bảo mật
  st.session_state.message = (
      "🎮 Trò chơi bắt đầu! Lượt đầu tiên thuộc về **Người chơi 1 🔴**."
  )

# Đảm bảo các biến luôn tồn tại
if "turn" not in st.session_state:
  st.session_state.turn = "Người chơi 1"
if "show_board" not in st.session_state:
  st.session_state.show_board = False
if "game_over" not in st.session_state:
  st.session_state.game_over = False
if "message" not in st.session_state:
  st.session_state.message = "Trò chơi bắt đầu!"

max_val = st.session_state.max_val

# Nút chơi lại thủ công
if st.button("🔄 Chơi ván mới / Reset"):
  st.session_state.target_number = random.randint(1, max_val)
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.session_state.turn = "Người chơi 1"
  st.session_state.show_board = False
  st.session_state.message = (
      "🔄 Đã reset ván mới! Lượt đầu tiên thuộc về **Người chơi 1 🔴**."
  )
  st.rerun()

st.markdown("---")

# Hiển thị thông báo trạng thái lượt chơi
if st.session_state.game_over:
  st.success(st.session_state.message)
else:
  turn_icon = "🔴" if st.session_state.turn == "Người chơi 1" else "🔵"
  st.info(f"{turn_icon} **Lượt hiện tại: {st.session_state.turn}**")
  st.write(st.session_state.message)

  # 3. Cơ chế bảo mật: Yêu cầu người kia nhắm mắt trước khi hiện bảng chọn
  if not st.session_state.show_board:
    st.warning(
        f"🙈 **{st.session_state.turn} chuẩn bị chọn số!** Người chơi còn lại"
        " hãy **NHẮM MẮT LẠI** hoặc quay đi để giữ bí mật."
    )
    if st.button(
        f"👀 Đã nhắm mắt xong! Mở bảng chọn cho {st.session_state.turn}",
        use_container_width=True,
    ):
      st.session_state.show_board = True
      st.rerun()
  else:
    # Bảng chọn số tự do cho người chơi hiện tại
    st.subheader(
        f"📊 Bảng Chọn Số của {st.session_state.turn} (Khoảng hợp lệ:"
        f" {st.session_state.min_limit} đến {st.session_state.max_limit})"
    )
    st.write(
        "👉 Hãy tự do bấm chọn một số bất kỳ trong khoảng hợp lệ bên dưới:"
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
              key=f"btn_secret_{max_val}_{num}",
              disabled=is_disabled,
              use_container_width=True,
          ):
            current_player = st.session_state.turn

            if num == st.session_state.target_number:
              st.session_state.game_over = True
              st.session_state.message = (
                  f"🎉 Chúc mừng **{current_player}** đã bấm trúng số {num} và"
                  " giành chiến thắng tuyệt đối! 🏆"
              )
              st.session_state.show_board = True
            else:
              if num < st.session_state.target_number:
                hint = "nhỏ hơn"
                if num >= st.session_state.min_limit:
                  st.session_state.min_limit = num + 1
              else:
                hint = "lớn hơn"
                if num <= st.session_state.max_limit:
                  st.session_state.max_limit = num - 1

              # Chuyển lượt cho người còn lại và ẩn bảng đi để bắt đầu màn hình nhắm mắt mới
              next_player = (
                  "Người chơi 2"
                  if current_player == "Người chơi 1"
                  else "Người chơi 1"
              )
              st.session_state.turn = next_player
              st.session_state.show_board = False
              st.session_state.message = (
                  f"❌ **{current_player}** đã chọn số {num} (Số bí mật"
                  f" **{hint}** số này). Đổi lượt cho **{next_player}**!"
              )
            st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
  st.markdown("### 💡 Hướng dẫn chơi 2 người bí mật")
  st.markdown(
      "- **Bảo mật**: Khi đến lượt ai, người kia phải nhắm mắt lại/quay đi."
  )
  st.markdown(
      "- **Mở bảng**: Bấm nút mở bảng sau khi người kia đã nhắm mắt để tự do"
      " chọn số."
  )
  st.markdown(
      "- **Chiến thắng**: Ai đoán trúng con số bí mật sẽ giành chiến thắng!"
  )
