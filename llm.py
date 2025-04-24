import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import GenerativeModel  # Required for latest versions

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Correct logger name

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
try:
    model = GenerativeModel(model_name="gemini-1.5-flash")
except Exception as e:
    logger.error(f"Failed to initialize GenerativeModel: {e}")
    model = None

def nl_to_sql(nl_query: str) -> str:
    """
    Converts a natural language query to SQL using Gemini 1.5 Flash.
    Returns SQL string or None on failure.
    """
    if not model:
        logger.error("Gemini model is not initialized.")
        return None

    prompt = f"""
You are an expert at converting natural language to SQL.
Only return a valid SQL query for SQLite.
Do not include explanations or comments. Just return the SQL.

Natural Language: "{nl_query}"
SQL:
""".strip()

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        return None