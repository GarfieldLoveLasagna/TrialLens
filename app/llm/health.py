import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")
model = "mistral-large-latest"

def check_mistral_health() -> str:
    try:
        client = Mistral(api_key=api_key)
        
        chat_response = client.chat.complete(
            model=model,
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