import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Đoán Số - Thầy Chọn Lớp Đoán",
    page_icon="👨‍🏫",
    layout="centered",
)


# Hàm tổng hợp âm thanh và nhạc nền chạy bằng Web Audio API & HTML5 Audio
def play_sound(sound_type):
  js_code = f"""
    <script>
    try {{
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playTone(freq, type, duration, delay = 0) {{
            setTimeout(() => {{
                if (audioCtx.state === 'suspended') {{
                    audioCtx.resume();
                }}
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.value = freq;
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            }}, delay);
        }}

        if ("{sound_type}" == "click") {{
            // Tiếng bấm chọn số (Ting thanh thoát)
            playTone(587.33, 'sine', 0.1, 0); // D5
        }} else if ("{sound_type}" == "wrong") {{
            // Tiếng đoán sai (Buzzer trầm)
            playTone(150, 'sawtooth', 0.2, 0);
            playTone(110, 'sawtooth', 0.3, 100);
        }} else if ("{sound_type}" == "win") {{
            // Nhạc chiến thắng hào hùng
            let notes = [523.25, 659.25, 783.99, 1046.50, 783.99, 1046.50];
            let times = [0, 150, 300, 450, 700, 900];
            let durations = [0.15, 0.15, 0.15, 0.3, 0.15, 0.5];
            for(let i=0; i<notes.length; i++) {{
                playTone(notes[i], 'triangle', durations[i], times[i]);
            }}
        }}
    }} catch(e) {{}}
    </script>
    """
  components.html(js_code, height=0, width=0)


# Nhạc nền lofi/vui nhộn chạy vòng lặp ngầm
def play_background_music():
  bg_js = """
    <script>
    if (!window.bgMusicStarted) {
        window.bgMusicStarted = true;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Tạo giai điệu nhạc nền game nhẹ nhàng lặp lại tự động
        const melody = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63]; // C E G C5 G E
        let index = 0;
        
        setInterval(() => {
            if (audioCtx.state === 'suspended') { audioCtx.resume(); }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.value = melody[index];
            
            gain.gain.setValueAtTime(0.03, audioCtx.currentTime); // Âm lượng nhỏ êm dịu làm nền
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.4);
            
            index = (index + 1) % melody.length;
        }, 500); // Nhịp điệu mỗi nốt cách nhau 0.5 giây
    }
    </script>
    """
  components.html(bg_js, height=0, width=0)


# Kích hoạt nhạc nền
play_background_music()

st.title("👨‍🏫 Game Đoán Số (Thầy Chọn - Lớp Đoán có Nhạc & Âm Thanh)")
st.write("Cùng tham gia game show đoán số với hiệu ứng âm thanh cực cuốn hút!")

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
  st.session_state.trigger_win_sound = False

max_val = st.session_state.max_val

# Nút chơi lại / Đổi số mới
if st.button("🔄 Chọn số mới (Ván mới)"):
  st.session_state.step = "setting"
  st.session_state.target_number = None
  st.session_state.attempts = 0
  st.session_state.game_over = False
  st.session_state.min_limit = 1
  st.session_state.max_limit = max_val
  st.session_state.trigger_win_sound = False
  play_sound("click")
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
      st.session_state.trigger_win_sound = False
      play_sound("click")
      st.rerun()

# GIAO DIỆN 2: ĐOÁN SỐ TRÊN BẢNG TƯƠNG TÁC
elif st.session_state.step == "guessing":
  st.success("👀 Mọi người đã mở mắt! Hãy cùng nhau bấm chọn số để đoán.")
  st.info(f"🎯 Số lần đã đoán: {st.session_state.attempts}")

  # Phát nhạc chiến thắng nếu vừa đoán trúng
  if st.session_state.get("trigger_win_sound", False):
    play_sound("win")
    st.session_state.trigger_win_sound = False

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
            st.session_state.trigger_win_sound = True
            st.success(
                f"🎉 CHÍNH XÁC! Đã tìm ra số bí mật **{num}** sau"
                f" {st.session_state.attempts} lần thử! 🏆"
            )
          else:
            play_sound("wrong")  # Âm thanh khi học sinh chọn sai
            if num < st.session_state.target_number:
              st.session_state.min_limit = num + 1
            else:
              st.session_state.max_limit = num - 1
          st.rerun()

  if st.session_state.game_over:
    st.balloons()
    if st.button("🔄 Hãy chọn số mới cho ván tiếp theo", use_container_width=True):
      st.session_state.step = "setting"
      st.session_state.game_over = False
      st.session_state.trigger_win_sound = False
      play_sound("click")
      st.rerun()
