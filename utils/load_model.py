import json
from functools import partial

from pydantic import parse_obj_as
from transformers import pipeline
# from transformers.pipelines import Pipeline

import models.note_model as note_model
import utils.files as files

def prepare_data():
    # Generate prepared_data.json file with all the modified entries from raw_data.json
    
    # Read NEW entries
    raw_data: list[str]
    with open(files.RAW_FILE, mode='r', encoding='utf8') as raw_data_file:
        raw_data = json.load(raw_data_file)

    # Convert raw data to model class, a list of notes
    raw_notes = parse_obj_as(list[note_model.Note], raw_data)

    # Load old entries
    old_data: list[str]
    with open(files.PREPARED_DATA_FILE, mode='r', encoding='utf8') as old_data_file:
        old_data = json.load(old_data_file)

    old_notes = parse_obj_as(list[note_model.Note], old_data)

    # Modify each Note.description_index
    description_begin: int
    description_end: int
    iteration: int = 0

    for rn in raw_notes:
        if iteration == 0:
            if len(old_notes) == 0:
                description_begin = 0
            else:
                # +2 because we count the \n separator as a new character
                description_begin = old_notes[-1].description_index[1] + 2
        else:
            description_begin = description_end + 2 # +2 because we count the \n separator as a new character
        description_end = description_begin + len(rn.description) - 1
        rn.description_index = (description_begin, description_end)
        iteration = iteration + 1

    # Append new entries to old ones
    old_notes.extend(raw_notes)
    
    # Re-write prepared file
    with open(files.PREPARED_DATA_FILE, mode='w', encoding='utf8') as prepared_data_file:
        json_string = json.dumps([n.dict() for n in old_notes], indent=2, separators=(',', ': '))
        prepared_data_file.write(json_string)

    # Clear raw file 
    with open(files.RAW_FILE, mode='w', encoding='utf8') as raw_data_file:
        raw_data_file.write("[]")

def write_descriptions():
     # Load old entries
    json_notes: list[str]
    with open(files.PREPARED_DATA_FILE, mode='r', encoding='utf8') as json_file:
        json_notes = json.load(json_file)

    notes: list[note_model.Note] = parse_obj_as(list[note_model.Note], json_notes)
    
    # Get list of descriptions
    desctiptions: list[str] = [note.description for note in notes]
    desctiptions: str = '\n'.join(desctiptions)

    with open(files.TRANSFORMER_CONTEXT_FILE, mode='w', encoding='utf8') as context_file:
        context_file.write(desctiptions)

def prepare_model() -> partial:

    # Read context file
    context: str
    with open(files.TRANSFORMER_CONTEXT_FILE, mode='r', encoding='utf8') as context_file:
        context = context_file.read()

    # Create the pipeline
    qa_pipeline = pipeline('question-answering', model=files.MODEL_FOLDER)
    return partial(qa_pipeline, context=context)

# ---------------------------------------------------------------------------------------
# ---------------------------------------- TESTS ----------------------------------------
# ---------------------------------------------------------------------------------------

# Using the transformer
def test1():
    from transformers import pipeline

    qa_pipeline = pipeline('question-answering', model=files.MODEL_FOLDER) # The folder with all the files
    # context = """ 
    # Procedure for assembling the cover ring assembly
    # 1. Remove the small screw (1 position) from the pressure gauge.
    # 2. Place the cover ring on the pressure gauge.
    # 3. Using the small screw that is provided with the cover ring, install the overring. The installation torque is 0.3 to 0.5N.m.
    # """

    # questions = [
    #          "What type of screw should I use to set the limit indicator?",
    #          "What is the next step after setting the limit indicator?",
    #          "How do I replace the cover?",
    #          "In which direction do I have to turn the cover?",
    #          "How many millimeters do I turn the cover?",
    #          "What screwdriver width do I need?",
    #          "How do I decrease the press?",
    #          "What color is the case cover?",
    #          "What is the first step for assembling the cover ring?",
    #          "What is the second step for assembling the cover ring?",
    #          "What is the last step for assembling the cover ring?"
    #         ]

    # data = []
    # # headers = ["Question", "Score", "Predictions"]
    # for q in questions:
    #     prediction = qa_pipeline(question = q, context = context)
    #     #data.append([q, prediction['score'], prediction['answer'].lower()])
    #     data.append(prediction)
    
    # print(data)
    context = "Transformers is backed by the three most popular deep learning libraries — Jax, PyTorch and TensorFlow\n — with a seamless integration between them. It's straightforward to train your models with one before loading them for inference with the other."
    question = "Which deep learning libraries back Transformers?"
    prediction = qa_pipeline(question=question, context=context)
    print(prediction)

def test2():
    p = prepare_model()
    answer = p(question="first")
    print(answer)
