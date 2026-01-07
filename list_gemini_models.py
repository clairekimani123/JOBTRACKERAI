import google.generativeai as genai
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# List available models
models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
