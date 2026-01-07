import streamlit as st
from src.ai_engine.interface import analyze_text, analyze_url


# ------------------ STYLING ------------------
st.markdown("""
<style>
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stHeader"] {display: none;}
[data-testid="stAppViewContainer"] {
    background: #020205 !important;
    color: white;
}
.full-summary-box {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ APP ------------------
st.title("📜 Terms & Conditions Risk Analyzer")

mode = st.radio("Choose input type", ["Paste Text", "Enter URL"])

text = ""
url = ""

if mode == "Paste Text":
    text = st.text_area("Paste Terms & Conditions", height=250)

if mode == "Enter URL":
    url = st.text_input("Enter Terms & Conditions URL")

if st.button("Analyze"):
    if mode == "Paste Text" and not text.strip():
        st.warning("Please paste some text.")
    elif mode == "Enter URL" and not url.strip():
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_text(text) if mode == "Paste Text" else analyze_url(url)

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
