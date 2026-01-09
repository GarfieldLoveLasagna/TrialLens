
# TrialLens

## 🩺 Application Overview

**TrialLens** is a backend service designed to make clinical trial information more accessible to non-expert audiences.

It retrieves data from **ClinicalTrials.gov**, normalizes complex and inconsistent trial records into clean domain models, and uses **Mistral LLMs** to generate structured, plain-English summaries intended for patients and caregivers.

The application is **informational only** and does not provide medical advice.

## ✨ Features

### 🔍 Clinical trial search

-   Search trials by condition or disease
    
-   Filter by recruitment status (e.g. `RECRUITING`, `NOT_YET_RECRUITING`)
    
-   Configurable result limits with guardrails
    

### 📄 Trial detail retrieval

-   Fetch a normalized, structured representation of a trial by NCT ID
    
-   Clean handling of missing or inconsistent upstream fields
    

### 🧠 LLM-generated summaries

-   Plain-English explanation of what the study is about
    
-   Key facts and outcomes
    
-   Eligibility guidance (high-level, non-diagnostic)
    
-   Participation overview (what it involves, where, time commitment)
    
-   Built-in safety disclaimer enforced at the schema level
    

### 🧱 Production-minded design

-   Clear separation of API, services, domain models, and LLM logic
    
-   Centralized configuration using Pydantic `Settings`
    
-   Strict schema validation for all LLM outputs
    
-   Safe defaults and bounded query parameters

## 🏗️ System Overview

### Architecture

    app/
    ├── api/            # FastAPI routers (HTTP layer)
    │   ├── health.py
    │   └── trials.py
    │
    ├── services/       # External API integrations
    │   └── clinicaltrials.py
    │
    ├── domain/         # Core domain & response models (Pydantic)
    │   ├── trial.py
    │   └── summary.py
    │
    ├── llm/            # Prompting & LLM orchestration
    │   ├── prompts.py
    │   └── health.py
    │
    ├── core/           # Configuration & settings
    │   └── config.py
    │
    └── main.py         # Application entrypoint
Each layer has a **single responsibility**, making the system easy to extend and test.

### End-to-end flow

#### 1️⃣ Trial search (`GET /trials/search`)

    Client
     → FastAPI router
     → ClinicalTrials.gov API
     → Raw response
     → Normalization into domain models
     → JSON response

#### 2️⃣ Trial detail (`GET /trials/{nct_id}`)

    Client
     → Fetch single study
     → Normalize into Trial model
     → Structured JSON response

#### 3️⃣ LLM summary (`GET /trials/{nct_id}/summary`)

    Client
     → Fetch normalized trial
     → Build structured summary input
     → Generate constrained prompt
     → Mistral LLM
     → Validate output against TrialSummary schema
     → Return safe, structured JSON
**Key design principles:**

-   The LLM never sees raw upstream API data
    
-   Inputs are curated and minimal
    
-   Outputs are validated before returning to the client
    
-   Safety disclaimers are enforced by the data model not the prompt

## ⚙️ Installation

### Requirements

-   Python 3.10+
    
-   Virtual environment recommended
    

### Install dependencies

    pip install -r requirements.txt

## 🚀 Usage

### Environment configuration

Create a `.env` file:

    APP_NAME=TrialLens
    APP_ENV=local_dev
    APP_VERSION=1.0
    
    MISTRAL_API_KEY=your_api_key_here
    MISTRAL_MODEL=mistral-large-latest
    
    CLINICAL_TRIAL_BASE_URL=https://clinicaltrials.gov/api/v2/studies
    CLINICAL_TRIAL_GET_STUDY_URL=https://clinicaltrials.gov/study/

### Run the application

    uvicorn app.main:app --reload
### API documentation
Swagger UI:

    http://localhost:8000/docs
### Example endpoints

-   `GET /trials/search`
-   `GET /trials/{nct_id}`
-   `GET /trials/{nct_id}/summary`
-   `GET /health`
-   `GET /health/llm`

## 📜 License

This project is licensed under the **MIT License** (see license file)

## 🙏 Acknowledgements

-   **ClinicalTrials.gov** for providing open access to clinical trial data
    
-   **Mistral AI** for LLM APIs and documentation
    
-   **FastAPI** and **Pydantic** for enabling clean, type-safe API design

## ⚠️ Disclaimer

This application is for **informational purposes only**.  
It does not provide medical advice and should not be used to make healthcare decisions.  
Always consult qualified healthcare professionals and the official study team for trial participation and medical guidance.