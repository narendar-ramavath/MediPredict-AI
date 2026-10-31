from pydantic import BaseModel
from typing import Optional


class AIRequest(BaseModel):
    glucose: float
    haemoglobin: float
    cholesterol: float


class AIResponse(BaseModel):
    remarks: Optional[str] = None
    status: str  # pending, completed, unavailable, failed
    provider: Optional[str] = None
    model: Optional[str] = None
