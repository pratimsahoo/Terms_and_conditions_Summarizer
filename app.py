import streamlit as st
import requests

# ================= BACKEND =================
BACKEND_URL = "http://localhost:8000/api/summarize"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="terms and conditions ",
    page_icon="",
    layout="wide"
)

# ================= CSS + PLANETARY ANIMATIONS =================
st.markdown("""
<style>

/* Hide Streamlit UI */
header, [data-testid="stToolbar"], [data-testid="stHeader"] {
    display: none;
}

/* Background */
[data-testid="stAppViewContainer"] {
    background: #02040a;
    overflow: hidden;
}

/* ⭐ Faster Rotating Stars */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background-image:
        radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    animation: starsRotate 120s linear infinite; /* ⬅ faster */
    opacity: 0.4;
}

@keyframes starsRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 🌍 Faster Earth Rotation */
.earth-container {
    position: fixed;
    top: 30%;
    right: -15%;
    width: 70vw;
    height: 70vw;
    background: url('https://upload.wikimedia.org/wikipedia/commons/b/ba/The_Blue_Marble_-_Earth_from_Apollo_17.jpg');
    background-size: cover;
    border-radius: 50%;
    box-shadow:
        inset 50px 0 80px 10px rgba(0,0,0,1),
        inset -10px 0 20px rgba(255,255,255,0.2),
        -20px 0 80px 10px rgba(63, 101, 241, 0.3);
    animation: rotateEarth 45s linear infinite; /* ⬅ faster */
    z-index: 0;
}

@keyframes rotateEarth {
    from { background-position: 0 0; }
    to { background-position: 200% 0; }
}

/* Content Layer */
.content-wrapper {
    position: relative;
    z-index: 30;
}

/* Headings */
.hero-title {
    font-family: 'Times New Roman', serif;
    font-size: 80px;
    letter-spacing: 15px;
    color: white;
    text-shadow: 0 0 20px rgba(255,255,255,0.5);
}

/* Feature Tags */
.feature-tag {
    background: rgba(255,255,255,0.05);
    border-left: 3px solid #6366f1;
    padding: 15px;
    margin: 10px 0;
    color: #cbd5e1;
    width: fit-content;
}

/* Cards */
.input-card {
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 30px;
    backdrop-filter: blur(15px);
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid white;
    color: white;
}

.stButton > button:hover {
    background: white;
    color: black;
}

/* 🔥 SCROLLABLE SUMMARY BOX */
.summary-box {
    max-height: 350px;
    overflow-y: auto;
    padding: 20px;
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    border-radius: 6px;
    color: #e5e7eb;
    line-height: 1.6;
}

/* Scrollbar */
.summary-box::-webkit-scrollbar {
    width: 6px;
}

.summary-box::-webkit-scrollbar-thumb {
    background: #6366f1;
    border-radius: 10px;
}
</style>

<div class="earth-container"></div>
""", unsafe_allow_html=True)

# ================= CONTENT =================
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<h1 class="hero-title">EARTH</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6366f1; letter-spacing:5px;">THE LEGAL SUMMARIZER</p>', unsafe_allow_html=True)
    st.markdown('<div class="feature-tag">DOCUMENT ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-tag">RISK IDENTIFICATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-tag">MULTI-LANGUAGE SUPPORT</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    input_choice = st.radio("SELECT SOURCE", ["TEXT", "URL"], horizontal=True)

    with st.form("main_form"):
        if input_choice == "TEXT":
            text_input = st.text_area("PASTE TERMS", height=200)
            url_input = None
        else:
            url_input = st.text_input("WEBSITE URL")
            text_input = None

        submitted = st.form_submit_button("ANALYZE DOCUMENT")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RESULTS =================
if submitted:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    with st.spinner("COMMUNICATING WITH SATELLITE..."):
        payload = {"text": text_input, "url": url_input, "summary_type": "simple"}

        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                data = response.json()

                st.subheader("📄 Summary")
                st.markdown(
                    f'<div class="summary-box">{data.get("summary","")}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("## 🔑 Key Points")
                for kp in data.get("key_points", [
                    "User must comply with all applicable laws.",
                    "Company may suspend or terminate access.",
                    "Terms may be updated without notice."
                ]):
                    st.markdown(f"- {kp}")

                st.markdown("## ⚠️ Risk Notes")
                st.info(data.get("risk_notes", "No major risks identified."))

            else:
                st.error("API Connection Failed")

        except Exception:
            st.info("Visual Demo Mode: Backend not connected.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)