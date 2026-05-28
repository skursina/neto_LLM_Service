from fastapi import FastAPI, HTTPException, status
from models.requests import SummarizeRequest
from models.responses import SummarizeResponse
from services.summarizer_service import summarize_text
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

app = FastAPI(title="LLM Summarizer API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    try:
        result = await summarize_text(request.text)
        return SummarizeResponse(summary=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Суммаризация недоступна: {str(e)}"
        )