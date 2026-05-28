from fastapi import APIRouter

from models.requests import SummarizeRequest
from models.responses import SummarizeResponse
from services.summarizer_service import summarize_text


router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    summary = await summarize_text(request.text)

    return SummarizeResponse(summary=summary)