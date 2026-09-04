from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApiResponse[T](BaseModel):
    success: bool = True
    data: T
    error: None = None
    request_id: str


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    fact_summary: str | None
    impact_analysis: str | None
    category: str | None
    region: str | None
    importance_score: float
    last_updated_at: datetime
