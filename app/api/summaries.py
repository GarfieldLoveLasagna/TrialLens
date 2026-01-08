import json
from fastapi import APIRouter, HTTPException, Path

from app.domain.summary import TrialSummary
from app.services.summaries import summarize_trial

router = APIRouter(prefix="/trials", tags=["summaries"])

@router.get("/{nct_id}/summary", response_model=TrialSummary)
def get_trial_summary(
    nct_id: str = Path(..., pattern=r"^NCT\d{8}$", description="ClinicalTrials.gov NCT identifier")
):
    try:
        return summarize_trial(nct_id)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="LLM returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {type(e).__name__}")