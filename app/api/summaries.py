from fastapi import APIRouter, HTTPException, Path
import json
import traceback
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
        traceback.print_exc()
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {type(e).__name__}")
