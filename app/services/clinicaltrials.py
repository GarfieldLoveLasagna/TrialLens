import requests

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def search_trials(condition: str, limit: int = 5):
    params = {"query.cond": condition, "pageSize": limit}
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()
