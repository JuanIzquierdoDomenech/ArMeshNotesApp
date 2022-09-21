from pydantic import BaseModel

class Answer(BaseModel):
    score: float
    start: int
    end: int
    answer: str