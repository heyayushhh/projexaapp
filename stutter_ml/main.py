from model_loader import load_model
from audio_utils import load_audio
from inference import run_inference
from postprocess import post_process
from audio_utils import split_audio

# 1. load model
classifier = load_model()

# 2. load audio
audio, sr = load_audio("sample.wav")

# 3. split audio
chunks, timestamps = split_audio(audio, sr)

# 4. run model
raw_results = run_inference(classifier, chunks, timestamps)

# 5. clean results
final_results = post_process(raw_results)

# 6. print
for r in final_results:
    print(r)