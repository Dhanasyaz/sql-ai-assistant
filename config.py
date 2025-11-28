import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables by their KEY names
EURI_API_KEY = os.getenv("EURI_API_KEY")
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
MODEL_NAME = "gpt-4.1-nano"
DATABASE_URI = os.getenv("DATABASE_URI")

# Clean up the DATABASE_URI - remove quotes and extra whitespace if present
if DATABASE_URI:
    DATABASE_URI = DATABASE_URI.strip().strip("'\"")
    print(f"DATABASE_URI: {DATABASE_URI[:50]}...")  # Print first 50 chars for debugging

# Raise error if DATABASE_URI is not set
if not DATABASE_URI:
    raise ValueError(
        "DATABASE_URI not found! Please check:\n"
        "1. .env file exists in the same directory as app.py\n"
        "2. .env file contains: DATABASE_URI=your_connection_string\n"
        "3. No extra spaces or quotes around the value"
    )