from pydantic import BaseModel

class Feedback(BaseModel):
    question: str
    sql: str
    rating: int
    comments: str = ""

class ImplicitLog(BaseModel):
    question: str
    generated_sql: str
#models.py