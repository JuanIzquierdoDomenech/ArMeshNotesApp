import json
from functools import partial

from pydantic import parse_obj_as
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

import utils.load_model as lm
import utils.files as files
from models.note_model import Note
from models.question_model import Question
from models.answer_model import Answer

app = FastAPI()
_model_data = {
    'model': '', 
    'notes': ''
    }

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
    # Creates new file with prepared data for transformers, and clears raw_data.json
    # and retreives the notes from the system
    _model_data['notes'] = lm.prepare_data()    

    # Writes all descriptions in a new file (using \n) for transformer context
    lm.write_descriptions()
    
    # Retrieve model, partially applied (has the "context", but needs the "question")
    _model_data['model'] = lm.prepare_model()   

    return "Model ready!"


@app.post("/ask/")
async def ask_question(question: Question) -> Answer:
    # answer = qa_model(question=question.question)
    answer_dict: dict = _model_data['model'](question=question.question)
    answer: Answer = parse_obj_as(Answer, answer_dict)

    # Look for the Note relative to this element of interest, using the index of the response and the index of every note
    # Answer has 'start' and 'end' properties
    all_notes: list[Note] = _model_data['notes']
    the_note: Note = next(
        filter(
            lambda note: answer.start >= note.description_index[0] and answer.end-1 <= note.description_index[1], all_notes),
            None)

    # Add missing info to respnse (the transform and the identifier)
    answer.note_transform_info = the_note.info
    answer.note_identifier = the_note.identifier

    return answer