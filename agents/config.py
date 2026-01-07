import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    
    # Job Search Settings
    MIN_MATCH_SCORE = float(os.getenv("MIN_MATCH_SCORE", "0.7"))
    JOB_FRESHNESS_DAYS = int(os.getenv("JOB_FRESHNESS_DAYS", "7"))
    
    # Personal Details
    FULL_NAME = os.getenv("FULL_NAME", "Your Name")
    EMAIL = os.getenv("EMAIL", "your.email@example.com")
    LOCATION = os.getenv("LOCATION", "Your City, Country")
    PHONE = os.getenv("PHONE", "+1234567890")
    
    # Resume Paths
    INDUSTRY_RESUME = "data/resumes/Industry.txt"
    RESEARCH_RESUME = "data/resumes/Research.txt"
    
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        if not cls.GOOGLE_SHEET_ID:
            raise ValueError("GOOGLE_SHEET_ID not found in environment")