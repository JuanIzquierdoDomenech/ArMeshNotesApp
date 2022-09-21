from pydantic import BaseModel

from .note_model import Transform

class Answer(BaseModel):
    score: float
    start: int
    end: int
    answer: str
    note_transform_info: Transform = None
    note_identifier: int = -1