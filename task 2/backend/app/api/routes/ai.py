from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.ai import AIRequest, AIResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/api/ai/analyze", response_model=AIResponse)
async def analyze_ai(request: AIRequest, db: Session = Depends(get_db)):
    ai_service = AIService()
    return await ai_service.analyze(request)
