import librosa

# Load audio file
def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=16000, mono=True)
    return audio, sr


# Split audio into chunks (STEP 5)
def split_audio(audio, sr, chunk_duration=1.5, stride=0.5):
    chunk_size = int(chunk_duration * sr)
    stride_size = int(stride * sr)

    chunks = []
    timestamps = []

    for i in range(0, len(audio) - chunk_size, stride_size):
        chunk = audio[i:i + chunk_size]

        start = i / sr
        end = (i + chunk_size) / sr

        chunks.append(chunk)
        timestamps.append((start, end))

    return chunks, timestamps