from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from llm import nl_to_sql
from feedback import save_feedback, log_interaction, init_db
from models import Feedback, ImplicitLog
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
init_db()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str = Field(..., example="List all customers from New York")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-sql")
async def generate_sql(request: QueryRequest):
    try:
        sql_query = nl_to_sql(request.question)
        if sql_query is None:
            raise HTTPException(status_code=500, detail="Failed to generate SQL")
        log_interaction(ImplicitLog(question=request.question, generated_sql=sql_query))
        return {
            "natural_language": request.question,
            "generated_sql": sql_query
        }
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate SQL")

@app.post("/submit-feedback")
async def submit_feedback(fb: Feedback):
    try:
        save_feedback(fb)
        return {"message": "Feedback received!"}
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")
 #main.py