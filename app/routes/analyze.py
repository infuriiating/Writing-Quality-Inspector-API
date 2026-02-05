from fastapi import APIRouter, Request, Depends
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.services.evaluator import evaluator
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit("3/minute")
async def analyze_text(request: Request, payload: AnalyzeRequest):
    """
    Analyze text quality using strict rubrics.
    """
    return await evaluator.analyze(payload)
