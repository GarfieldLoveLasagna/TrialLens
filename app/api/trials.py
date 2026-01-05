from fastapi import APIRouter, Query
from app.services.clinicaltrials import search_trials

router = APIRouter(prefix="/trials", tags=["trials"])

@router.get("/search")
async def search(condition: str = Query(...)):
    return search_trials(condition)