from fastapi import FastAPI
from src.utils.generate_outputs import generate_output
from src.core.url_extractor import extract_tc_text
from src.api.schemas import TextRequest, URLRequest

app = FastAPI(title="T&C Summarizer API")

@app.post("/analyze-text")
def analyze_text(req: TextRequest):
    return generate_output(req.text)

@app.post("/analyze-url")
def analyze_url(req: URLRequest):
    text = extract_tc_text(req.url)[:6000]
    return generate_output(text)
