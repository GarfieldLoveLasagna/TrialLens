from fastapi import FastAPI

from app.api.trials import router as trials_router
from app.api.health import router as health_router

app = FastAPI(title="TrialLens", version="0.1.0")

app.include_router(health_router)
app.include_router(trials_router)
