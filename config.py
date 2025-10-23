# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_NAME = "Travel & Entertainment Bot"
    BOT_EMOJI = "🌍"
    TAGLINE = "Your AI guide for travel plans and local events"
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
    
    @classmethod
    def validate_keys(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("Gemini API key is missing from environment variables")
        if not cls.TICKETMASTER_API_KEY:
            raise ValueError("Ticketmaster API key is missing from environment variables")
        
