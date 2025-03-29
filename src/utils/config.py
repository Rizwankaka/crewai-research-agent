import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file if it exists"""
    load_dotenv()

def get_api_key(name, default=None):
    """Get API key from environment variables or session state"""
    return os.getenv(name, default)