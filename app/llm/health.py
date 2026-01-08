from app.core.config import settings
from mistralai import Mistral

def check_mistral_health() -> str:
    try:
        client = Mistral(api_key=settings.mistral_api_key)
        
        chat_response = client.chat.complete(
            model=settings.mistral_model,
            messages=[
                {
                    "role": "user",
                    "content": "What is the best French cheese?",
                },
            ]
        )
        return chat_response
    except Exception as e:
        raise Exception(f"Mistral health check failed: {str(e)}")