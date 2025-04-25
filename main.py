import os
import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from llm import nl_to_sql  # Assuming this is your NL to SQL model
from feedback import save_feedback, log_interaction, init_db
from models import Feedback, ImplicitLog

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
init_db()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the request model for generating SQL
class QueryRequest(BaseModel):
    question: str = Field(..., example="List all customers from New York")

# Define the homepage endpoint
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the SQL generation endpoint
@app.post("/generate-sql")
async def generate_sql(request: QueryRequest):
    try:
        # Generate SQL from natural language question
        sql_query = nl_to_sql(request.question)
        if sql_query is None:
            raise HTTPException(status_code=500, detail="Failed to generate SQL")
        
        # Log interaction
        log_interaction(ImplicitLog(question=request.question, generated_sql=sql_query))
        
        # Return the result
        return {
            "natural_language": request.question,
            "generated_sql": sql_query
        }
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate SQL")

# Define the feedback submission endpoint
@app.post("/submit-feedback")
async def submit_feedback(fb: Feedback):
    try:
        save_feedback(fb)
        return {"message": "Feedback received!"}
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")

# Main entry point for running the app with Uvicorn
if __name__ == "__main__":
    # Set port to environment variable or fallback to 10000
    port = int(os.getenv("PORT", 10000))
    # Run the Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=port)