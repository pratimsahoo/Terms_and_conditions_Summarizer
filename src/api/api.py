from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.ai_engine.inference import run_inference
from src.core.url_extractor import extract_tc_text

app = FastAPI(
    title="Terms & Conditions Risk Analyzer API",
    description="Analyze T&C text or URL and return summary and risk score",
    version="1.0.0"
)

# ----------------------------
# Request Schemas
# ----------------------------

class TextRequest(BaseModel):
    text: str


class URLRequest(BaseModel):
    url: str


# ----------------------------
# API Endpoints
# ----------------------------

@app.post("/analyze/text")
def analyze_text(req: TextRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    return run_inference(req.text)


@app.post("/analyze/url")
def analyze_url(req: URLRequest):
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    try:
        text = extract_tc_text(req.url)
        text = text[:6000]  # safety limit
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return run_inference(text)
