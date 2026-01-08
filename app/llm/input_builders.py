from typing import Any, Dict
from app.domain.trial import Trial


PAYLOAD_LOCATION_LIMIT = 10

def _iso(d):
    return d.isoformat() if d else None

def build_summary_input(trial: Trial) -> Dict[str, Any]:
    """
    Minimize and standardize the input the LLM sees.
    """
    # limit locations to prevent huge prompts
    locs = []
    if trial.locations:
        for loc in trial.locations[:int(PAYLOAD_LOCATION_LIMIT)]:
            locs.append(
                {
                    "facility": loc.facility,
                    "city": loc.city,
                    "state": loc.state,
                    "country": loc.country,
                    "status": getattr(loc, "status", None),
                }
            )

    return {
        "nct_id": trial.nct_id,
        "title": trial.official_title or trial.brief_title,
        "brief_title": trial.brief_title,
        "official_title": trial.official_title,
        "conditions": trial.conditions or [],
        "keywords": trial.keywords or [],
        "study_type": trial.study_type,
        "status": trial.status,
        "phase": trial.phase,
        "primary_purpose": trial.primary_purpose,
        "enrollment_count": trial.enrollment_count,
        "start_date": _iso(trial.start_date),
        "primary_completion_date": _iso(trial.primary_completion_date),
        "completion_date": _iso(trial.completion_date),
        "last_update_posted": _iso(trial.last_update_posted),
        "sex": trial.sex,
        "min_age": trial.min_age,
        "max_age": trial.max_age,
        "healthy_volunteers": trial.healthy_volunteers,
        "eligibility_criteria": trial.eligibility_criteria,
        "interventions": trial.interventions or [],
        "primary_outcomes": [o.model_dump() for o in (trial.primary_outcomes or [])][:10],
        "locations": locs,
        "contacts": [c.model_dump() for c in (trial.contacts or [])][:5],
        "lead_sponsor": trial.lead_sponsor,
        "collaborators": trial.collaborators or [],
        "source_url": trial.url,
    }
