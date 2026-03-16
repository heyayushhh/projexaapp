import torch
import librosa
import numpy as np
from transformers import AutoProcessor, AutoModelForAudioClassification

model_name = "Huma10/Whisper_Stuttered_Speech"

print("Loading model...")

processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(
    model_name,
    use_safetensors=False
)

audio_path = "audio_stutter.wav"

audio, sr = librosa.load(audio_path, sr=16000)

# chunk length in seconds
chunk_length = 3
samples_per_chunk = chunk_length * sr

num_chunks = int(np.ceil(len(audio) / samples_per_chunk))

print("\nAnalyzing audio...\n")

for i in range(num_chunks):

    start_sample = i * samples_per_chunk
    end_sample = start_sample + samples_per_chunk

    chunk = audio[start_sample:end_sample]

    inputs = processor(
        chunk,
        sampling_rate=16000,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=30 * 16000
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_id = torch.argmax(logits).item()

    label = model.config.id2label[predicted_class_id]

    start_time = i * chunk_length
    end_time = start_time + chunk_length

    print(f"{start_time}s - {end_time}s : {label}")