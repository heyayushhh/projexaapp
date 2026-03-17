import pandas as pd
import librosa
from pathlib import Path
from tqdm import tqdm

# ===================== CONFIG =====================
BASE_DIR = Path(__file__).resolve().parent

NORMALIZED_ROOT = BASE_DIR / "normalized_audio"
LABELS_CSV = BASE_DIR / "dataset" / "SEP-28k_labels.csv"
OUTPUT_CSV = BASE_DIR / "train_dataset.csv"

SAMPLE_RATE = 16000

# ===================== LABEL MAP =====================
LABEL_COLUMNS = {
    "Prolongation": 1,
    "Block": 2,
    "SoundRep": 3,
    "WordRep": 4,
    "DifficultToUnderstand": 5,
    "Interjection": 6   # ✅ ADDED
}

LABEL_NAMES = {
    0: "fluent",
    1: "prolongation",
    2: "block",
    3: "sound_rep",
    4: "word_rep",
    5: "difficult",
    6: "interjection"   # ✅ ADDED
}

# ===================== HELPERS =====================
def safe_name(s):
    return str(s).strip().replace(" ", "").replace("/", "_").replace("\\", "_")

# ===================== LOAD LABELS =====================
df_labels = pd.read_csv(LABELS_CSV)

# Validate column exists
if "Interjection" not in df_labels.columns:
    raise ValueError("❌ 'Interjection' column not found in labels CSV")

label_lookup = {}

for _, row in df_labels.iterrows():
    show = safe_name(row["Show"])
    ep = str(int(float(row["EpId"])))
    clip = str(int(float(row["ClipId"])))

    key = f"{show}_{ep}_{clip}"

    # Default = fluent
    assigned_label = 0

    for col, val in LABEL_COLUMNS.items():
        if row[col] > 0:
            assigned_label = val
            break  # first detected stutter

    label_lookup[key] = assigned_label

print(f"✅ Loaded {len(label_lookup)} label mappings")

# ===================== BUILD DATASET =====================
rows = []

for label_folder in ["clean_audio", "stutter_clips"]:
    base_dir = NORMALIZED_ROOT / label_folder

    if not base_dir.exists():
        print(f"⚠️ Skipping {base_dir}")
        continue

    print(f"\n🔹 Processing {label_folder}")

    for show_dir in base_dir.iterdir():
        for ep_dir in show_dir.iterdir():

            wav_files = list(ep_dir.glob("*.wav"))

            for wav_path in tqdm(wav_files, leave=False):
                try:
                    filename = wav_path.stem

                    if filename not in label_lookup:
                        continue

                    label = label_lookup[filename]

                    y, sr = librosa.load(wav_path, sr=SAMPLE_RATE)
                    duration = len(y) / sr

                    if duration < 0.2:
                        continue

                    rows.append({
                        "path": wav_path.as_posix(),
                        "label": label,
                        "label_name": LABEL_NAMES[label],
                        "duration": round(duration, 3)
                    })

                except Exception as e:
                    print(f"❌ {wav_path} | {e}")

# ===================== SAVE =====================
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ Dataset created: {OUTPUT_CSV}")
print(f"Total samples: {len(df)}")

print("\n📊 Class distribution:")
print(df["label_name"].value_counts())