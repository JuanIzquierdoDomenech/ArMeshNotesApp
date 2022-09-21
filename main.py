import json
from functools import partial

from pydantic import parse_obj_as
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

import utils.load_model as lm
from models.note_model import Note
from models.question_model import Question
from models.answer_model import Answer
import utils.files as files

app = FastAPI()
_model = {'model': ''}

@app.get("/")
def read_root(response_class=HTMLResponse) -> HTMLResponse:
    html_content = """
    <html>
        <head>
            <title>ARMeshNotesApp</title>
        </head>
        <body>
            <h1>Welcome to ARMeshNotesApp!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/note/")
async def create_note(note: Note) -> Note:    
    # Load old entries
    raw_data: list[str]
    with open(files.RAW_FILE, mode='r') as raw_data_file:
        raw_data = json.load(raw_data_file)
    raw_notes = parse_obj_as(list[Note], raw_data)

    # Add new note
    raw_notes.append(note)

    # re-write the same file
    with open(files.RAW_FILE, mode='w') as raw_data_file:
        json_string = json.dumps([n.dict() for n in raw_notes], indent=2, separators=(',', ': '))
        raw_data_file.write(json_string)

    return note


@app.get("/train/", response_class=PlainTextResponse)
async def train_model() -> PlainTextResponse:
    lm.prepare_data()                       # Creates new file with prepared data for transformers, and clears raw_data.json
    lm.write_descriptions()                 # Writes all descriptions in a new file (using \n )
    
    _model['model'] = lm.prepare_model()    # Retrieve partially applied model (has the "context", but needs the "question")
    return "Model ready!"


@app.post("/ask/")
async def ask_question(question: Question) -> Answer:
    # answer = qa_model(question=question.question)
    answer: dict = _model['model'](question=question.question)
    result = parse_obj_as(Answer, answer)
    return result