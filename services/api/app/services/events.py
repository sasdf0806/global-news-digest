from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from app.models import Event


def build_event_query(
    *, category: str | None = None, region: str | None = None, keyword: str | None = None
) -> Select[tuple[Event]]:
    """Build the event listing query independently from HTTP concerns."""
    query = select(Event).where(Event.status == "published")
    if category:
        query = query.where(Event.category == category)
    if region:
        query = query.where(Event.region == region)
    if keyword:
        pattern = f"%{keyword}%"
        query = query.where(or_(Event.title.ilike(pattern), Event.fact_summary.ilike(pattern)))
    return query.order_by(Event.importance_score.desc(), Event.last_updated_at.desc())


def list_events(
    db: Session,
    *,
    category: str | None = None,
    region: str | None = None,
    keyword: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Event]:
    """Return published events using deterministic ranking and pagination."""
    query = (
        build_event_query(category=category, region=region, keyword=keyword)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(query))
