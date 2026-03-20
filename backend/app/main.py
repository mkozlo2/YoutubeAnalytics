import app.models  # noqa: F401
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analytics_routes import router as analytics_router
from app.api.auth_routes import router as auth_router
from app.api.channel_routes import router as channel_router
from app.api.debug_routes import router as debug_router
from app.api.video_routes import router as video_router
from app.core.config import get_settings
from app.core.database import Base, engine

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(channel_router)
app.include_router(video_router)
app.include_router(analytics_router)
app.include_router(debug_router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}
