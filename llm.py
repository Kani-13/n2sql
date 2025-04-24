import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configure the Gemini API key
genai.configure(api_key=os.getenv("AIzaSyDZC7iXbrVi62o7EAQIXbCa0R6C8gnT2-A"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def nl_to_sql(nl_query: str) -> str:
    prompt = f""" 
    You are an expert at converting natural language to SQL. Only return valid SQL for SQLite. 
    Do not explain anything, just give SQL. 

    Natural Language: "{nl_query}"
    SQL:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        return None #llm.py