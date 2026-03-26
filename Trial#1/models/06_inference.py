import torch
from pathlib import Path

from stutter_dataset import StutterDataset
from stutter_model import StutterCNN

# =============================
# PATHS
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "Data_downloading" / "dataset" / "final_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "model.pth"

# =============================
# LABELS
# =============================
LABELS = [
    "Prolongation",
    "Block",
    "SoundRep",
    "WordRep",
    "Interjection"
]

# =============================
# LOAD DATA
# =============================
dataset = StutterDataset(CSV_PATH)

# Pick sample
mel, label = dataset[0]

# =============================
# LOAD MODEL
# =============================
device = "cuda" if torch.cuda.is_available() else "cpu"
mel = mel.unsqueeze(0).to(device)

model = StutterCNN().to(device)

# Dummy forward pass to initialize lazy fc layers
with torch.no_grad():
    model(mel)

model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
model.eval()

# =============================
# PREDICTION
# =============================
with torch.no_grad():
    logits = model(mel)
    probs = torch.sigmoid(logits).cpu()

# =============================
# CLASS-WISE THRESHOLDS
# =============================
thresholds = torch.tensor([
    0.5,   # Prolongation
    0.65,  # Block (higher → reduce false positives)
    0.5,   # SoundRep
    0.5,   # WordRep
    0.5    # Interjection
])

pred = (probs > thresholds).int()

# =============================
# OUTPUT
# =============================
print("\nProbabilities:", probs)
print("Prediction:", pred)
print("Ground Truth:", label)

print("\nDetailed:")
for i, cls in enumerate(LABELS):
    print(
        f"{cls}: prob={probs[0][i]:.4f}  "
        f"pred={pred[0][i].item()}  "
        f"truth={int(label[i].item())}"
    )