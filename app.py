import streamlit as st

from src.ai_engine.inference import run_inference
from src.core.url_extractor import extract_tc_text

# ================= GLOBAL STYLING =================
st.markdown("""
<style>
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stHeader"] {display: none;}

/* ================= SPACE BACKGROUND ================= */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at bottom, #020617 0%, #000000 65%);
    color: white;
    position: relative;
    overflow: hidden;
}

/* FAR STARS */
@keyframes starsFar {
    from { background-position: 0 0; }
    to { background-position: 6000px 3000px; }
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/stardust.png");
    animation: starsFar 260s linear infinite;
    opacity: 0.45;
    pointer-events: none;
    z-index: 0;
}

/* NEAR STARS */
@keyframes starsNear {
    from { background-position: 0 0; }
    to { background-position: -8000px 4000px; }
}
.stars-near {
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/tiny-stars.png");
    animation: starsNear 180s linear infinite;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}

/* NEBULA */
.nebula {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 30% 40%, rgba(99,102,241,0.25), transparent 45%),
        radial-gradient(circle at 70% 60%, rgba(14,165,233,0.22), transparent 50%);
    filter: blur(90px);
    opacity: 0.6;
    pointer-events: none;
    z-index: 0;
}

/* ================= SHOOTING STARS ================= */
@keyframes shooting {
    0% { transform: translate(0,0) rotate(-45deg); opacity: 0; }
    10% { opacity: 1; }
    40% { transform: translate(-1200px,1200px) rotate(-45deg); opacity: 0; }
    100% { opacity: 0; }
}

.shooting-star {
    position: fixed;
    top: -150px;
    width: 3px;
    height: 250px;
    background: linear-gradient(to bottom, rgba(255,255,255,0), #ffffff);
    filter: drop-shadow(0 0 10px rgba(255,255,255,0.9));
    animation: shooting 8s linear infinite;
    z-index: 1;
    pointer-events: none;
}

/* ================= EARTH SYSTEM ================= */
.earth-system {
    position: fixed;
    bottom: -42%;
    right: -26%;
    width: 760px;
    height: 760px;
    pointer-events: none;
    z-index: 0;
    animation: earth-drift 150s ease-in-out infinite;
}

/* EARTH */
.earth {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-image:
        url("https://raw.githubusercontent.com/visualizedata/globe-map/master/world.topo.bathy.200412.3x5400x2700.jpg");
    background-size: cover;
    animation: earth-spin 220s linear infinite;
    box-shadow:
        inset -180px 0 260px rgba(0,0,0,0.92),
        0 0 180px rgba(0,170,255,0.45);
    position: relative;
}

/* ATMOSPHERE */
.earth::before {
    content: "";
    position: absolute;
    inset: -22px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(0,170,255,0.35),
        rgba(0,170,255,0.08) 45%,
        transparent 75%
    );
}

/* AURORA */
.aurora {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background:
        radial-gradient(circle at 50% 20%, rgba(34,197,94,0.35), transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(59,130,246,0.25), transparent 40%);
    mix-blend-mode: screen;
    animation: aurora-pulse 14s ease-in-out infinite;
}

/* CLOUDS */
.clouds {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background:
        url("https://raw.githubusercontent.com/turban/webgl-earth/master/images/clouds.png");
    background-size: cover;
    opacity: 0.4;
    animation: cloud-spin 400s linear infinite;
}

/* MOON */
.moon-orbit {
    position: absolute;
    inset: -120px;
    animation: moon-orbit 120s linear infinite;
}
.moon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: url("https://raw.githubusercontent.com/rajatkulkarni95/EarthMoonSimulation/main/moon.jpg");
    background-size: cover;
    position: absolute;
    top: 50%;
    left: -40px;
    box-shadow: 0 0 40px rgba(255,255,255,0.25);
}

/* SATELLITE ORBIT */
.orbit-ring {
    position: absolute;
    inset: -90px;
    border-radius: 50%;
    border: 1px dashed rgba(255,255,255,0.15);
}

/* ANIMATIONS */
@keyframes earth-spin {
    from { background-position: 0 0; }
    to { background-position: -5400px 0; }
}
@keyframes cloud-spin {
    from { background-position: 0 0; }
    to { background-position: -5400px 0; }
}
@keyframes earth-drift {
    0% { transform: translate(0,0); }
    50% { transform: translate(-80px, 30px); }
    100% { transform: translate(0,0); }
}
@keyframes moon-orbit {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes aurora-pulse {
    0%,100% { opacity: 0.4; }
    50% { opacity: 0.75; }
}

/* ================= GLASS UI ================= */
.full-summary-box {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    position: relative;
    z-index: 2;
}
</style>

<div class="stars-near"></div>
<div class="nebula"></div>

<!-- Shooting stars (multiple instances) -->
<div class="shooting-star" style="right:10%; animation-delay:0s;"></div>
<div class="shooting-star" style="right:35%; animation-delay:3s;"></div>
<div class="shooting-star" style="right:60%; animation-delay:6s;"></div>

<div class="earth-system">
    <div class="earth">
        <div class="aurora"></div>
        <div class="clouds"></div>
        <div class="orbit-ring"></div>
        <div class="moon-orbit">
            <div class="moon"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= APP UI =================
st.title("📜 Terms & Conditions Risk Analyzer")

mode = st.radio("Choose input type", ["Paste Text", "Enter URL"])

input_text = ""

if mode == "Paste Text":
    input_text = st.text_area("Paste Terms & Conditions text", height=250)

if mode == "Enter URL":
    url = st.text_input("Enter Terms & Conditions URL")
    if url:
        with st.spinner("Extracting text from URL..."):
            input_text = extract_tc_text(url)[:6000]

# ================= ANALYZE =================
if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please provide input text or URL.")
    else:
        with st.spinner("Analyzing using local AI model..."):
            result = run_inference(input_text)

        st.markdown("<div class='full-summary-box'>", unsafe_allow_html=True)

        st.subheader("Summary")
        for s in result["summary"]:
            st.write("•", s)

        st.subheader("Risk Level")
        st.write(f"{result['risk_level']} ({result['risk_score']}/10)")

        st.subheader("Key Risks")
        for r in result["key_risks"]:
            st.write("•", r)

        st.caption(result["disclaimer"])
        st.markdown("</div>", unsafe_allow_html=True)
