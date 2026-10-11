import random
import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Game Đoán Số Nâng Cao", page_icon="🎮", layout="centered")

st.title("🎮 Game Đoán Số Nâng Cao")
st.write("Thử thách trí tuệ với các cấp độ khó khác nhau và bảng loại trừ thông minh!")

# 1. Chọn cấp độ game
level = st.selectbox(
    "🏆 Chọn cấp độ:",
    ["Cấp 1: 1 - 100", "Cấp 2: 1 - 500", "Cấp 3: 1 - 1000"],
    index=0,
)

# Xác định khoảng số dựa theo cấp độ
if "1" in level:
    max_val = 100
elif "2" in level:
    max_val = 500
else:
    max_val = 1000

# Khởi tạo trạng thái trò chơi hoặc reset khi đổi cấp độ
if (
    "target_number" not in st.session_state
    or st.session_state.get("max_val") != max_val
):
    st.session_state.max_val = max_val
    st.session_state.target_number = random.randint(1, max_val)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    # Lưu khoảng giới hạn hiện tại của người chơi để làm bảng số
    st.session_state.min_limit = 1
    st.session_state.max_limit = max_val

# Nút đổi ván mới hoặc reset
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Chơi lại"):
        st.session_state.target_number = random.randint(1, max_val)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.min_limit = 1
        st.session_state.max_limit = max_val
        st.rerun()

# Form nhập số dự đoán
with st.form("guess_form"):
    user_guess = st.number_input(
        f"Nhập dự đoán của bạn (1 - {max_val}):",
        min_value=1,
        max_value=max_val,
        step=1,
    )
    submit_button = st.form_submit_button("Đoán ngay!")

# Xử lý khi nhấn nút Đoán
if submit_button and not st.session_state.game_over:
    st.session_state.attempts += 1

    if user_guess == st.session_state.target_number:
        st.success(
            f"🎉 Chính xác! Bạn đã đoán đúng số {st.session_state.target_number} sau {st.session_state.attempts} lần thử!"
        )
        st.session_state.game_over = True
    elif user_guess < st.session_state.target_number:
        st.warning(
            f"📈 Số bạn đoán **nhỏ hơn** số bí mật. (Khoảng hợp lệ hiện tại:"
            f" từ {user_guess + 1} đến {st.session_state.max_limit})"
        )
        if user_guess >= st.session_state.min_limit:
            st.session_state.min_limit = user_guess + 1
    else:
        st.warning(
            f"📉 Số bạn đoán **lớn hơn** số bí mật. (Khoảng hợp lệ hiện tại:"
            f" từ {st.session_state.min_limit} đến {user_guess - 1})"
        )
        if user_guess <= st.session_state.max_limit:
            st.session_state.max_limit = user_guess - 1

# 2. Hiển thị Bảng Trạng Thái (Các số bị loại sẽ bị mờ/gạch đi)
st.markdown("---")
st.subheader("📊 Bảng Trạng Thái Các Số (1 đến " + str(max_val) + ")")
st.write(
    "💡 *Các số nằm ngoài khoảng hợp lệ hoặc đã bị loại trừ sẽ tự động bị mờ"
    " đi!*"
)

# Tạo bảng lưới hiển thị các số
cols_per_row = 10
numbers = list(range(1, max_val + 1))

# Chia nhỏ danh sách thành các hàng để hiển thị đẹp mắt
for i in range(0, len(numbers), cols_per_row):
    row_nums = numbers[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    for idx, num in enumerate(row_nums):
        with cols[idx]:
            # Kiểm tra xem số có nằm trong khoảng hợp lệ không
            if (
                num < st.session_state.min_limit
                or num > st.session_state.max_limit
            ):
                # Số đã bị loại (hiển thị mờ/gạch ngang)
                st.markdown(
                    f"<p style='color: gray; text-decoration: line-through;"
                    f" text-align: center; margin: 0;'>{num}</p>",
                    unsafe_allow_html=True,
                )
            else:
                # Số vẫn còn khả năng chọn
                st.markdown(
                    f"<p style='color: green; font-weight: bold; text-align:"
                    f" center; margin: 0;'>{num}</p>",
                    unsafe_allow_html=True,
                )

# Sidebar hướng dẫn
with st.sidebar:
    st.markdown("### 💡 Hướng dẫn chơi")
    st.markdown(
        "- **Cấp độ**: Thay đổi độ khó tùy ý (1-100, 1-500, hoặc 1-1000)."
    )
    st.markdown("- **Bảng loại trừ**: Các số không phù hợp sẽ tự động mờ đi.")
    st.markdown("- **Mục tiêu**: Đoán trúng số bí mật với ít lần thử nhất.")import random
import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Game Đoán Số May Mắn", page_icon="🎮", layout="centered")

# Tiêu đề game
st.title("🎮 Game Đoán Số May Mắn")
st.write(
    "Tôi đã chọn một số ngẫu nhiên từ **1 đến 100**. Bạn hãy đoán xem đó là số mấy nhé!"
)

# Khởi tạo trạng thái trò chơi (session_state) để lưu dữ liệu
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

# Xử lý khi nhấn nút Đoán
if submit_button and not st.session_state.game_over:
    st.session_state.attempts += 1

    if user_guess == st.session_state.target_number:
        st.success(
            f"🎉 Chính xác! Bạn đã đoán đúng số {st.session_state.target_number} sau {st.session_state.attempts} lần thử!"
        )
        st.session_state.game_over = True
    elif user_guess < st.session_state.target_number:
        st.warning("📈 Số bạn đoán **nhỏ hơn** số bí mật. Hãy thử số lớn hơn!")
    else:
        st.warning("📉 Số bạn đoán **lớn hơn** số bí mật. Hãy thử số nhỏ hơn!")

# Nút chơi lại khi game kết thúc
if st.session_state.game_over:
    if st.button("🔄 Chơi ván mới"):
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.rerun()

# Sidebar hướng dẫn
with st.sidebar:
    st.markdown("### 💡 Hướng dẫn chơi")
    st.markdown("- **Mục tiêu**: Tìm ra con số bí mật từ 1 đến 100 trong ít lần thử nhất.")
    st.markdown("- **Gợi ý**: Hệ thống sẽ báo số bạn đoán đang lớn hơn hay nhỏ hơn số bí mật.")
    st.markdown("- **Nút chơi lại**: Nhấn Chơi ván mới để bắt đầu lượt chơi khác.")
