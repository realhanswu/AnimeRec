from pydantic import BaseModel, Field
from typing import List, Optional

class UserContext(BaseModel):
    user_id: str
    device: str = "mobile"

class RecRequest(BaseModel):
    context: UserContext
    k: int = Field(default=10, ge=1, le=100)

class RecItem(BaseModel):
    item_id: str
    score: float
    rank: int

class RecResponse(BaseModel):
    items: List[RecItem]
    latency_ms: float
