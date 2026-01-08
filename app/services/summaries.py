import json
import os
from dotenv import load_dotenv
from mistralai import Mistral

from app.domain.summary import TrialSummary
from app.services.clinicaltrials import get_trial
from app.llm.input_builders import build_summary_input
from app.llm.prompts import build_summary_prompt

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")
model = "mistral-large-latest"

def summarize_trial(nct_id: str) -> TrialSummary:
    trial = get_trial(nct_id)
    payload = build_summary_input(trial)
    prompt = build_summary_prompt(payload)

    client = Mistral(api_key=api_key)

    resp = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        #Low temperature for deterministic, factual responses and prevent hallucinations
        temperature=0.2,
    )

    text = resp.choices[0].message.content

    data = json.loads(text)

    return TrialSummary.model_validate(data)
