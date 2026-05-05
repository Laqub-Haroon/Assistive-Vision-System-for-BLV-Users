import streamlit as st
import subprocess
import pyttsx3
import cv2
import time

# ---------------- ENGINE ----------------


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="BLV Assistive System", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

.result-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: #f8fafc;  /* brighter white */
    border: 1px solid #38bdf8; /* glow border */
    box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.4);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🧠 BLV Assistive System</h1>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "run" not in st.session_state:
    st.session_state.run = False

if "executed" not in st.session_state:
    st.session_state.executed = False

FRAME_WINDOW = st.image([])

# ---------------- CAMERA CAPTURE ----------------
def capture_image(duration=5):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start = time.time()
    frame = None

    progress = st.progress(0)

    while time.time() - start < duration:
        ret, img = cap.read()
        if not ret:
            continue

        frame = img
        FRAME_WINDOW.image(img, channels="BGR")

        elapsed = time.time() - start
        progress.progress(min(int((elapsed / duration) * 100), 100))

    cap.release()
    progress.empty()
    return frame

# ---------------- CLEAN RUN ----------------
def run_clean(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    return lines[-1]

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start"):
        st.session_state.run = True
        st.session_state.executed = False

with col2:
    if st.button("🔄 Reset"):
        st.session_state.run = False
        st.session_state.executed = False

# ---------------- MAIN EXECUTION ----------------
if st.session_state.run and not st.session_state.executed:

    st.info("📸 Keep your face straight & show your sign")

    # STEP 1: Capture
    frame = capture_image(5)

    if frame is None:
        st.error("❌ Camera failed")
        st.session_state.run = False
        st.stop()

    cv2.imwrite("captured.jpg", frame)

    # STEP 2: Face Recognition
    st.info("🔍 Detecting face...")
    face = run_clean([
        r"C:\Users\DELL\Desktop\prmo\face_env\Scripts\python.exe",
        "face_system.py"
    ])

    time.sleep(0.5)

    # STEP 3: Sign Recognition
    st.info("✋ Detecting sign...")
    sign = run_clean([
        r"C:\Users\DELL\Desktop\prmo\mp_env\Scripts\python.exe",
        "sign_system.py"
    ])

    if sign.lower() == "none":
        sign = "Hello"

    # FINAL RESULT
    result = f"{face.replace('_',' ').title()} is in front of you and he is saying {sign}"

    st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)

    # IMAGE DISPLAY
    st.image("captured.jpg", caption="📷 Captured Frame", use_container_width=True)
    with st.spinner("🔊 Speaking..."):
        try:
            import subprocess

            subprocess.Popen([
                r"C:\Users\DELL\Desktop\prmo\face_env\Scripts\python.exe",
                "-c",
                f"import pyttsx3; e=pyttsx3.init(); e.setProperty('rate',120); e.say('{result}'); e.runAndWait()"
            ])
        except:
            pass

    st.success("✅ Done")
    st.session_state.executed = True
    st.session_state.run = False

    st.stop()