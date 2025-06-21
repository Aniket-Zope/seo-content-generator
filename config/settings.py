import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    PORT = int(os.getenv("PORT", 8000))
    
    # LLM Settings
    MODEL_NAME = "gpt-3.5-turbo"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # Content Settings
    DEFAULT_ARTICLE_LENGTH = 1500
    MAX_KEYWORDS_PER_ARTICLE = 5
    
settings = Settings()
