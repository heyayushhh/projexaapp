from transformers import pipeline

def load_model():
    classifier = pipeline(
        "audio-classification",
        model="HareemFatima/distilhubert-finetuned-stutterdetection"
    )
    return classifier