# This file downloads the transformer model to use locally

from transformers import pipeline, AutoModel, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering


def download_model():

    transformer_type = "question-answering"

    # https://arxiv.org/abs/2111.05754
    tokenizer = AutoTokenizer.from_pretrained(
        "Intel/bert-large-uncased-squadv1.1-sparse-80-1x4-block-pruneofa"
    )

    model = AutoModelForQuestionAnswering.from_pretrained(
        "Intel/bert-large-uncased-squadv1.1-sparse-80-1x4-block-pruneofa"
    )

    qa_pipeline = pipeline(task=transformer_type, model=model, tokenizer=tokenizer)
    qa_pipeline.save_pretrained("the_model")


if __name__ == "__main__":
    download_model()
