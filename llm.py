import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def nl_to_sql(nl_query: str) -> str:
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
