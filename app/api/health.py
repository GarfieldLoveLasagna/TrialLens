from fastapi import APIRouter
from app.llm.health import check_mistral_health
router = APIRouter(prefix="", tags=["health"])

@router.get("/health")
async def health():
    """App status health check"""
    return {"status": "ok"}

@router.get("/health/llm")
async def llm_health():
    """LLM health check"""
    return {"mistralResponse": check_mistral_health().model_dump()}