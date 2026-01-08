from __future__ import annotations

import requests
#using request as clintrials is fingerprinting httpx
from datetime import date
from typing import Any, Dict, List, Optional
from app.domain.trial import Trial, TrialCard, TrialLocation, TrialContact, TrialOutcome
from app.core.config import settings


def search_trials_raw(condition: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search trials from ClinicalTrials.gov by condition
    """
    params = {"query.cond": condition, "pageSize": limit}
    resp = requests.get(settings.clinical_trial_base_url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def search_trials(condition: str, limit: int = 5) -> List[Trial]:
    """
    Search and normalize trials by condition
    """
    raw = search_trials_raw(condition, limit)
    studies = raw.get("studies", []) or []
    return [map_study_to_trial(s) for s in studies if isinstance(s, dict)]

def search_trial_cards(condition: str, limit: int = 5, max_locations: int = 5) -> List[TrialCard]:
    """
    Search, normalize and summarize trials by condition
    """
    trials = search_trials(condition, limit) 
    return [to_trial_card(t, max_locations=max_locations) for t in trials]

def get_trial_raw(nct_id: str) -> Dict[str, Any]:
    """
    Fetch a single study from ClinicalTrials.gov by NCTID
    """
    url = settings.clinical_trial_base_url + "/" + nct_id
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def get_trial(nct_id: str) -> Trial:
    """
    Fetch and normalize a single trial by NCTID
    """
    raw = get_trial_raw(nct_id)
    return map_study_to_trial(raw)

def _get(d: Dict[str, Any], *path: str, default=None):
    cur: Any = d
    for key in path:
        if not isinstance(cur, dict):
            return default
        if key not in cur:
            return default
        cur = cur[key]
    return cur

def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_date_struct(study: Dict[str, Any], *path: str) -> Optional[date]:
    """
    Many CT.gov date fields are like:
      {"startDateStruct": {"date": "2024-01-10", "type": "ACTUAL"}}
    """
    d = _get(study, *path, default=None)
    if isinstance(d, dict):
        return _parse_date(d.get("date"))
    if isinstance(d, str):
        return _parse_date(d)
    return None


def map_study_to_trial(study: Dict[str, Any]) -> Trial:
    """
    Convert a ClinicalTrials.gov study payload into a Trial domain model.
    """
    proto = study.get("protocolSection", {}) or {}
    ident = proto.get("identificationModule", {}) or {}
    status_mod = proto.get("statusModule", {}) or {}
    cond_mod = proto.get("conditionsModule", {}) or {}
    design_mod = proto.get("designModule", {}) or {}
    elig_mod = proto.get("eligibilityModule", {}) or {}
    arms_mod = proto.get("armsInterventionsModule", {}) or {}
    out_mod = proto.get("outcomesModule", {}) or {}
    contacts_mod = proto.get("contactsLocationsModule", {}) or {}
    sponsor_mod = proto.get("sponsorCollaboratorsModule", {}) or {}
    nct_id = ident.get("nctId")
    if not nct_id:
        raise ValueError("Missing nctId in study.identificationModule")

    brief_title = ident.get("briefTitle") or ""
    official_title = ident.get("officialTitle")
    conditions = cond_mod.get("conditions") or []
    if not isinstance(conditions, list):
        conditions = []
    keywords = cond_mod.get("keywords")
    study_type = design_mod.get("studyType")
    overall_status = status_mod.get("overallStatus")
    start_date = _parse_date_struct(proto, "statusModule", "startDateStruct")
    primary_completion_date = _parse_date_struct(proto, "statusModule", "primaryCompletionDateStruct")
    completion_date = _parse_date_struct(proto, "statusModule", "completionDateStruct")
    last_update_posted = _parse_date_struct(proto, "statusModule", "lastUpdateSubmitDate")
    phases = design_mod.get("phases")
    phase = None
    if isinstance(phases, list) and phases:
        phase = phases[0]
    if phase == "NA":
        phase = None
    primary_purpose = design_mod.get("primaryPurpose")
    enrollment_count = None
    enrollment = design_mod.get("enrollmentInfo")
    if isinstance(enrollment, dict):
        cnt = enrollment.get("count")
        if isinstance(cnt, int):
            enrollment_count = cnt
        elif isinstance(cnt, str) and cnt.isdigit():
            enrollment_count = int(cnt)
    min_age = elig_mod.get("minimumAge")
    max_age = elig_mod.get("maximumAge")
    sex = elig_mod.get("sex")
    eligibility_criteria = elig_mod.get("eligibilityCriteria")
    healthy_volunteers = None
    hv = elig_mod.get("healthyVolunteers")
    if isinstance(hv, bool):
        healthy_volunteers = hv
    elif isinstance(hv, str):
        hv_upper = hv.upper()
        if "ACCEPT" in hv_upper or hv_upper in {"YES", "Y", "TRUE"}:
            healthy_volunteers = True
        elif hv_upper in {"NO", "N", "FALSE"}:
            healthy_volunteers = False
    interventions_list: Optional[List[str]] = None
    interventions = arms_mod.get("interventions")
    if isinstance(interventions, list) and interventions:
        names: List[str] = []
        for it in interventions:
            if isinstance(it, dict):
                name = it.get("name")
                itype = it.get("type")
                if name and itype:
                    names.append(f"{name} ({itype})")
                elif name:
                    names.append(name)
        interventions_list = names or None
    primary_outcomes: Optional[List[TrialOutcome]] = None
    po = out_mod.get("primaryOutcomes")
    if isinstance(po, list) and po:
        out_objs: List[TrialOutcome] = []
        for o in po:
            if not isinstance(o, dict):
                continue
            measure = o.get("measure")
            if not measure:
                continue
            out_objs.append(
                TrialOutcome(
                    measure=measure,
                    time_frame=o.get("timeFrame"),
                    description=o.get("description"),
                )
            )
        primary_outcomes = out_objs or None
    locations: Optional[List[TrialLocation]] = None
    locs = contacts_mod.get("locations")
    if isinstance(locs, list) and locs:
        loc_objs: List[TrialLocation] = []
        for loc in locs:
            if not isinstance(loc, dict):
                continue
            facility = None
            fac = loc.get("facility")
            if isinstance(fac, dict):
                facility = fac.get("name")
            elif isinstance(fac, str):
                facility = fac

            loc_objs.append(
                TrialLocation(
                    facility=facility,
                    city=loc.get("city"),
                    state=loc.get("state"),
                    country=loc.get("country"),
                    status=loc.get("status")
                )
            )
        locations = loc_objs or None
    contacts: Optional[List[TrialContact]] = None
    central = contacts_mod.get("centralContacts")
    if isinstance(central, list) and central:
        c_objs: List[TrialContact] = []
        for c in central:
            if not isinstance(c, dict):
                continue
            c_objs.append(
                TrialContact(
                    name=c.get("name"),
                    role=c.get("role") or "Central Contact",
                    phone=c.get("phone"),
                    email=c.get("email"),
                )
            )
        contacts = c_objs or None
    lead_sponsor = None
    ls = sponsor_mod.get("leadSponsor")
    if isinstance(ls, dict):
        lead_sponsor = ls.get("name")
    collaborators: Optional[List[str]] = None
    collab = sponsor_mod.get("collaborators")
    if isinstance(collab, list) and collab:
        names = [c.get("name") for c in collab if isinstance(c, dict) and c.get("name")]
        collaborators = names or None
    return Trial(
        nct_id=nct_id,
        url = settings.clinical_trial_get_study_url + "/" + nct_id,
        brief_title=brief_title,
        official_title=official_title,
        conditions=conditions,
        keywords=keywords,
        study_type=study_type,
        status=overall_status,
        start_date=start_date,
        primary_completion_date=primary_completion_date,
        completion_date=completion_date,
        last_update_posted=last_update_posted,
        phase=phase,
        primary_purpose=primary_purpose,
        enrollment_count=enrollment_count,
        min_age=min_age,
        max_age=max_age,
        sex=sex,
        healthy_volunteers=healthy_volunteers,
        eligibility_criteria=eligibility_criteria,
        interventions=interventions_list,
        primary_outcomes=primary_outcomes,
        locations=locations,
        contacts=contacts,
        lead_sponsor=lead_sponsor,
        collaborators=collaborators,
    )

def to_trial_card(trial: Trial, max_locations: int = 5) -> TrialCard:
    locs = trial.locations or []
    loc_preview = locs[:max_locations] if locs else None
    return TrialCard(
        nct_id=trial.nct_id,
        brief_title=trial.brief_title,
        conditions=trial.conditions,
        status=trial.status,
        phase=trial.phase,
        study_type=trial.study_type,
        lead_sponsor=trial.lead_sponsor,
        last_update_posted=trial.last_update_posted,
        locations=loc_preview,
        location_count=len(locs) if trial.locations is not None else None,
        url=trial.url,
    )
