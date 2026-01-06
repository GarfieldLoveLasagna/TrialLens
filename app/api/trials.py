from fastapi import APIRouter, Query, HTTPException, Path
from app.services.clinicaltrials import search_trial_cards, get_trial
from app.domain.trial import Trial
import requests


router = APIRouter(prefix="/trials", tags=["trials"])

@router.get("/search")
async def search(condition: str = Query(...)):
    return search_trial_cards(condition)

@router.get("/{nct_id}", response_model=Trial)
def get_by_id(
    nct_id: str = Path(..., pattern=r"^NCT\d{8}$", description="ClinicalTrials.gov NCT identifier")
):
    try:
        return get_trial(nct_id)
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", 502)
        if status == 404:
            raise HTTPException(status_code=404, detail="Trial not found")
        raise HTTPException(status_code=502, detail="ClinicalTrials.gov request failed")
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="ClinicalTrials.gov request failed")