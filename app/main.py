from fastapi import FastAPI

from app.core.config import settings
from app.api.trials import router as trials_router
from app.api.health import router as health_router
from app.api.summaries import router as summaries_router

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(health_router)
app.include_router(trials_router)
app.include_router(summaries_router)