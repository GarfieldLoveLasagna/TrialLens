from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    app_name: str
    app_env: str
    app_version: str

    # LLM
    mistral_api_key: str
    mistral_model: str

    # External APIs
    clinical_trial_base_url: str
    clinical_trial_get_study_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()