# AR Mesh Notes App Server
This repository contains the files for the server side of the AR Mesh Notes App

## Requirements
This server uses PyEnv y VirtualEnv, so make sure you create a virtual environment and install the requirements in `requirements.txt`

*Python Version: 3.9.13*

## Requests

| Request     | Description |
| ----------: | :---------- |
| GET /       | Basic HTML template
| POST /note/ | This request takes adds the new AR note (see model description below) into the system, and returns the inserted Note |
| GET /train/ | This request starts the process to obtain a transformer, ready for making QA requests, and returns a PlainTextResponse |
| POST /ask/  | This request takes a Question and returns an Answer (see models below) |
| POST /notes_in_rectangle/ | Takes an AreaSelection and returns the notes within it, with a certain tolerance depending on the plane |


This is the structure of the models, using Pydantic:

### Note model

```python
class Vec3(BaseModel):
    x: float
    y: float
    z: float


class Transform(BaseModel):
    position: Vec3
    rotation: Vec3
    scale: Vec3


class Note(BaseModel):
    identifier: str
    description: str
    info: Transform
    description_index: tuple[int, int] = (
        -1,
        -1,
    )

class NotesList(BaseModel):
    notes: list[Note] = None
```

### Question model

```python
class Question(BaseModel):
    question: str
```

### Answer model

```python
class Answer(BaseModel):
    score: float
    start: int
    end: int
    answer: str
    note_transform_info: Transform = None
    note_identifier: int = -1
```

### AreaSelection model

```python
class AreaSelection(BaseModel):
    begin: Vec3
    end: Vec3
    tolerance: float
    normalDir: str


class NormalDir(Enum):
    NONE = 0
    POSITIVE_X = 1
    POSITIVE_Y = 2
    POSITIVE_Z = 3
    NEGATIVE_X = 4
    NEGATIVE_Y = 5
    NEGATIVE_Z = 6
```

## To run the server
`uvicorn main:app --host 0.0.0.0 --port 80` or just `python main.py`

The local IP could be something like 192.168.2.X

## To download the model
Since the model was **too heavy** for git, execute `download_model.py` BEFORE ANYTHING ELSE

This will generate a *transformer_qa_model* directory
