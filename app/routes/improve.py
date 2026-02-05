from fastapi import APIRouter, Request, Depends
from app.schemas.request import ImproveRequest
from app.schemas.response import ImproveResponse
from app.services.evaluator import evaluator
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/improve", response_model=ImproveResponse)
@limiter.limit("1/minute")
async def improve_text(request: Request, payload: ImproveRequest):
    """
    Improve text based on specific focus areas using AI.
    """
    return await evaluator.improve(payload)
