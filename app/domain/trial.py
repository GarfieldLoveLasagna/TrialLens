from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class TrialLocation(BaseModel):
    facility: Optional[str]
    status: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

class TrialContact(BaseModel):
    name: Optional[str]
    role: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class TrialOutcome(BaseModel):
    measure: str
    time_frame: Optional[str]
    description: Optional[str]

class Trial(BaseModel):
    nct_id: str
    url: str
    brief_title: str
    official_title: Optional[str]
    conditions: List[str]
    keywords: Optional[List[str]] = None
    study_type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    primary_completion_date: Optional[date] = None
    completion_date: Optional[date] = None
    last_update_posted: Optional[date] = None
    phase: Optional[str] = None
    primary_purpose: Optional[str] = None
    enrollment_count: Optional[int] = None
    min_age: Optional[str] = None
    max_age: Optional[str] = None
    sex: Optional[str] = None
    healthy_volunteers: Optional[bool] = None
    eligibility_criteria: Optional[str] = None
    interventions: Optional[List[str]] = None
    primary_outcomes: Optional[List[TrialOutcome]] = None
    locations: Optional[List[TrialLocation]] = None
    contacts: Optional[List[TrialContact]] = None
    lead_sponsor: Optional[str] = None
    collaborators: Optional[List[str]] = None

class TrialCard(BaseModel):
    nct_id: str
    url: str
    brief_title: str
    conditions: List[str]
    status: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    lead_sponsor: Optional[str] = None
    last_update_posted: Optional[date] = None
    locations: Optional[List["TrialLocation"]] = None
    location_count: Optional[int] = None