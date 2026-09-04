from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import ApiResponse, EventRead
from app.services.events import list_events as query_events

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=ApiResponse[list[EventRead]])
def list_events(
    request: Request,
    category: str | None = Query(default=None),
    region: str | None = Query(default=None),
    keyword: str | None = Query(default=None, min_length=1, max_length=200),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=10000),
    db: Session = Depends(get_db),  # noqa: B008
) -> ApiResponse[list[EventRead]]:
    rows = query_events(
        db, category=category, region=region, keyword=keyword, limit=limit, offset=offset
    )
    return ApiResponse(
        data=[EventRead.model_validate(row) for row in rows],
        request_id=request.state.request_id,
    )
