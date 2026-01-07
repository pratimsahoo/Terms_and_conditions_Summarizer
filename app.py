import streamlit as st

from src.ai_engine.inference import run_inference
from src.core.url_extractor import extract_tc_text

# ------------------ GLOBAL STYLING ------------------
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

# ------------------ APP UI ------------------
st.title("📜 Terms & Conditions Risk Analyzer")

mode = st.radio("Choose input type", ["Paste Text", "Enter URL"])

input_text = ""

if mode == "Paste Text":
    input_text = st.text_area(
        "Paste Terms & Conditions text",
        height=250
    )

if mode == "Enter URL":
    url = st.text_input("Enter Terms & Conditions URL")
    if url:
        try:
            with st.spinner("Extracting text from URL..."):
                input_text = extract_tc_text(url)[:6000]
        except Exception as e:
            st.error(str(e))
            input_text = ""


# ------------------ ANALYZE ------------------
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
