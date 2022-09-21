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

## To run the server
`uvicorn main:app --host 0.0.0.0 --port 80`

The local IP could be something like 192.168.2.X

## To download the model
Since the model was **too heavy** for git, execute `download_model.py`

This will generate a *model* directory, which was too heavy for git
