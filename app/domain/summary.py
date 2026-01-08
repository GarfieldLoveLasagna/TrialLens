from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional

class EligibilityHighlights(BaseModel):
    """
    High-level, plain-English eligibility bullets.
    Must reflect the record NO MEDICAL ADVICE
    """
    likely_eligible_if: List[str] = Field(default_factory=list, description="Inclusion-like bullet points.")
    likely_not_eligible_if: List[str] = Field(default_factory=list, description="Exclusion-like bullet points.")
    unknown_or_unclear: List[str] = Field(default_factory=list, description="Eligibility aspects not specified or unclear.")

class ParticipationInfo(BaseModel):
    """
    Practical participation notes when supported by the source.
    """
    what_it_involves: List[str] = Field(default_factory=list, description="Visits, procedures, surveys, medication, etc.")
    time_commitment: Optional[str] = Field(default=None, description="E.g., 'weekly visits for ~8 weeks' if stated; else None.")
    location_notes: Optional[str] = Field(default=None, description="E.g., 'single site in Zhengzhou, China' if derived from locations; else None.")
    costs_and_compensation: Optional[str] = Field(
        default=None,
        description="If stated in the record; otherwise None. Do not guess."
    )

class TrialSummary(BaseModel):
    """
    Patient-friendly summary of a clinical trial record (informational only).
    """
    nct_id: str = Field(..., description="ClinicalTrials.gov NCT identifier.")
    source_url: str = Field(..., description="ClinicalTrials.gov study URL.")
    generated_at: datetime = Field(default=datetime.now(timezone.utc), description="UTC timestamp when this summary was generated.")

    plain_english_summary: str = Field(
        ...,
        description="2–6 sentence patient-friendly overview of the trial."
    )

    key_facts: List[str] = Field(
        default_factory=list,
        description="Short bullet facts (phase, status, population, intervention type, etc.)."
    )

    eligibility: EligibilityHighlights = Field(
        default_factory=EligibilityHighlights,
        description="Simplified eligibility bullets derived from the record."
    )

    participation: ParticipationInfo = Field(
        default_factory=ParticipationInfo,
        description="Practical participation notes (only if supported by the record)."
    )

    questions_to_ask_your_doctor: List[str] = Field(
        default_factory=list,
        description="Suggested questions for a clinician or trial contact."
    )

    safety_disclaimer: str = Field(
        default=(
            "Informational only. This summary is based on publicly available ClinicalTrials.gov data and may be incomplete "
            "or outdated. It is not medical advice. Always discuss trial eligibility, risks, and benefits with a qualified "
            "healthcare professional and the study team."
        ),
        description="Fixed disclaimer shown with every summary."
    )

    limitations: List[str] = Field(
        default_factory=list,
        description="Explicit notes about missing/uncertain info (e.g., 'Results not posted', 'Locations missing')."
    )