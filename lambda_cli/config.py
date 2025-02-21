import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = "https://cloud.lambdalabs.com/api/v1"
API_KEY = os.getenv("LAMBDA_API_KEY")

# Config directory setup
CONFIG_DIR = Path.home() / ".lambda-cli"
CONFIG_DIR.mkdir(exist_ok=True)

def get_api_key():
    """Get API key from environment or prompt user to enter it"""
    if API_KEY:
        return API_KEY
    
    raise ValueError(
        "API key not found. Please set LAMBDA_API_KEY environment variable "
        "or create a .env file with LAMBDA_API_KEY=your-api-key"
    )

def get_headers():
    """Get default headers for API requests"""
    return {
        "Content-Type": "application/json"
    }

def get_auth():
    """Get authentication tuple for requests"""
    return (get_api_key(), "") 