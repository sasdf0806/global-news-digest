from fastapi import FastAPI

from app.api.routes import events, health
from app.core.config import get_settings
from app.middleware import RequestIdMiddleware

settings = get_settings()
app = FastAPI(title="Global News Digest API", version="0.1.0")
app.add_middleware(RequestIdMiddleware)
app.include_router(health.router, prefix="/api")
app.include_router(events.router, prefix="/api")


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {"name": settings.app_name, "environment": settings.app_env}
