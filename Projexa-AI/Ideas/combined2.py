import cv2
import mediapipe as mp
import numpy as np
from collections import deque, Counter
import threading
import sounddevice as sd
import torch
import torch.nn.functional as F
from transformers import AutoProcessor, AutoModelForAudioClassification

# ============================================================
# CONFIGURATION
# ============================================================

# General fallback threshold
AUDIO_CONFIDENCE_THRESH = 0.60

# Label-specific stricter thresholds
LABEL_THRESHOLDS = {
    "SoundRep": 0.76,
    "WordRep": 0.68,
    "Interjection": 0.70,
    "Prolongation": 0.68,
    "NoStutteredWords": 0.60
}

# Face / speaking
SPEAKING_MOUTH_THRESH = 0.055
SPEAKING_VAR_THRESH   = 0.0025

# Head jerk
HEAD_JERK_ACCEL_THRESH = 0.018
HEAD_JERK_MIN_FRAMES   = 2
EMA_ALPHA = 0.35

# Tremor
TREMOR_WINDOW = 12
TREMOR_STD_THRESH = 0.0018
TREMOR_ZERO_CROSS_THRESH = 5
HEAD_STABLE_THRESH = 0.010

# Block
BLOCK_STATIC_THRESH = 0.0015
BLOCK_MIN_FRAMES    = 12

# Fusion
FUSION_MIN_SIGNALS = 2

# ============================================================
# LOAD AUDIO MODEL
# ============================================================

model_name = "Huma10/Whisper_Stuttered_Speech"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)
model.eval()

latest_audio_label = "Listening..."
latest_audio_confidence = 0.0
audio_lock = threading.Lock()

# NEW: smoothing history
audio_label_history = deque(maxlen=5)

display_audio_label = "Listening..."
display_audio_hold = 0
DISPLAY_HOLD_FRAMES = 20
# ============================================================
# AUDIO THREAD
# ============================================================

def get_threshold_for_label(label):
    return LABEL_THRESHOLDS.get(label, AUDIO_CONFIDENCE_THRESH)

def smooth_audio_label(history):
    """
    Balanced smoothing:
    - If a stutter label appears at least 2 times recently, keep it
    - Otherwise fallback to latest meaningful label
    """
    if len(history) == 0:
        return "Listening..."

    counts = Counter(history)

    # Prefer real stutter labels if they appear at least twice
    for label in ["SoundRep", "WordRep", "Prolongation", "Interjection"]:
        if counts[label] >= 2:
            return label

    # Otherwise use most recent non-normal label if present
    for label in reversed(history):
        if label not in ("NoStutteredWords", "No Speech", "Listening..."):
            return label

    return "NoStutteredWords"
    """
    Majority vote smoothing.
    If labels are inconsistent, return NoStutteredWords.
    """
    if len(history) < 3:
        return history[-1] if history else "Listening..."   

    counts = Counter(history)
    top_label, top_count = counts.most_common(1)[0]

    # Require consistency
    if top_count >= 3:
        return top_label
    return "NoStutteredWords"

def audio_worker():
    global latest_audio_label, latest_audio_confidence

    sr = 16000
    buffer = []

    def callback(indata, frames, time, status):
        buffer.append(indata.copy())

    with sd.InputStream(samplerate=sr, channels=1, callback=callback):
        while True:
            if len(buffer) > 10:   # ~1 sec audio
                audio = np.concatenate(buffer, axis=0).flatten()
                buffer.clear()

                # Silence / weak speech filter
                rms = np.sqrt(np.mean(audio ** 2))
                if rms < 0.01:
                    with audio_lock:
                        latest_audio_label = "No Speech"
                        latest_audio_confidence = 0.0
                    continue

                inputs = processor(
                    audio,
                    sampling_rate=16000,
                    return_tensors="pt",
                    padding="max_length",
                    truncation=True,
                    max_length=30 * 16000,
                )

                with torch.no_grad():
                    outputs = model(**inputs)

                probs = F.softmax(outputs.logits, dim=-1)
                conf, pred = torch.max(probs, dim=-1)

                conf_val = conf.item()
                raw_label = model.config.id2label[pred.item()]

                # Label-specific stricter threshold
                needed_thresh = get_threshold_for_label(raw_label)

                if conf_val < needed_thresh:
                    raw_label = "NoStutteredWords"

                # Add to smoothing history
                global display_audio_label, display_audio_hold

                audio_label_history.append(raw_label)
                smoothed_label = smooth_audio_label(audio_label_history)

                # Hold detected stutter label for a short duration
                if smoothed_label not in ("NoStutteredWords", "No Speech", "Listening..."):
                    display_audio_label = smoothed_label
                    display_audio_hold = DISPLAY_HOLD_FRAMES
                else:
                    if display_audio_hold > 0:
                        display_audio_hold -= 1
                    else:
                        display_audio_label = smoothed_label

                with audio_lock:
                    latest_audio_label = display_audio_label
                    latest_audio_confidence = conf_val

threading.Thread(target=audio_worker, daemon=True).start()

# ============================================================
# VIDEO SETUP
# ============================================================

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

# Histories
mouth_hist = deque(maxlen=20)
head_accel_hist = deque(maxlen=6)

# Tremor histories
upper_lip_y_hist = deque(maxlen=TREMOR_WINDOW)
lower_lip_y_hist = deque(maxlen=TREMOR_WINDOW)

prev_nose = None
prev_velocity = 0.0
ema_nose = None

jerk_frames = 0
block_counter = 0

# ============================================================
# HELPERS
# ============================================================

def px(lm, idx, w, h):
    return np.array([lm[idx].x * w, lm[idx].y * h], dtype=np.float32)

def ema_update(prev, new, alpha):
    return alpha * new + (1 - alpha) * prev if prev is not None else new.copy()

def draw_label(frame, text, y, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale, th = 0.72, 2
    (tw, tht), baseline = cv2.getTextSize(text, font, scale, th)
    pad = 6
    cv2.rectangle(
        frame,
        (20, y - tht - pad),
        (20 + tw + 2 * pad, y + baseline + pad),
        (30, 30, 30),
        cv2.FILLED
    )
    cv2.putText(frame, text, (20 + pad, y), font, scale, color, th, cv2.LINE_AA)

def is_speaking(mouth_hist):
    if len(mouth_hist) < 8:
        return False
    mean_open = np.mean(mouth_hist)
    var_open = np.std(np.diff(mouth_hist)) if len(mouth_hist) > 2 else 0
    return (mean_open > SPEAKING_MOUTH_THRESH) and (var_open > SPEAKING_VAR_THRESH)

def compute_repetition(mouth_hist):
    if len(mouth_hist) < 8:
        return False
    diffs = np.diff(mouth_hist)
    signs = np.sign(diffs)
    zero_crossings = np.sum(signs[:-1] != signs[1:])
    return zero_crossings >= 5

def compute_lip_tremor(upper_hist, lower_hist, head_stable=True):
    if len(upper_hist) < TREMOR_WINDOW or not head_stable:
        return False, 0.0

    upper = np.array(upper_hist, dtype=np.float32)
    lower = np.array(lower_hist, dtype=np.float32)

    signal = lower - upper

    smooth = np.convolve(signal, np.ones(5) / 5, mode='same')
    residual = signal - smooth

    amp = np.std(residual)

    signs = np.sign(np.diff(residual))
    zero_crossings = np.sum(signs[:-1] != signs[1:])

    tremor = (amp > TREMOR_STD_THRESH) and (zero_crossings >= TREMOR_ZERO_CROSS_THRESH)
    return tremor, amp

# ============================================================
# MAIN LOOP
# ============================================================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    flag_jerk = False
    flag_tremor = False
    flag_block = False
    flag_repetition = False
    speaking_flag = False

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark

        # Key points
        nose = px(lm, 1, w, h)
        upper = px(lm, 13, w, h)
        lower = px(lm, 14, w, h)
        left = px(lm, 61, w, h)
        right = px(lm, 291, w, h)

        # Face normalization points
        left_cheek = px(lm, 234, w, h)
        right_cheek = px(lm, 454, w, h)

        face_width = np.linalg.norm(left_cheek - right_cheek) + 1e-6

        # Normalized mouth opening
        mouth_open = np.linalg.norm(upper - lower) / face_width
        mouth_hist.append(mouth_open)

        # Tremor signals
        upper_lip_y_hist.append(upper[1] / face_width)
        lower_lip_y_hist.append(lower[1] / face_width)

        # Speaking gate
        speaking_flag = is_speaking(mouth_hist)

        # ---------------- HEAD JERK ----------------
        ema_nose = ema_update(ema_nose, nose, EMA_ALPHA)

        head_stable = True
        if prev_nose is not None:
            velocity = np.linalg.norm(ema_nose - prev_nose) / face_width
            accel = abs(velocity - prev_velocity)

            head_accel_hist.append(accel)

            if np.median(head_accel_hist) > HEAD_JERK_ACCEL_THRESH:
                jerk_frames += 1
            else:
                jerk_frames = max(0, jerk_frames - 1)

            flag_jerk = jerk_frames >= HEAD_JERK_MIN_FRAMES
            prev_velocity = velocity

            if accel > HEAD_STABLE_THRESH:
                head_stable = False

        prev_nose = ema_nose.copy()

        # ---------------- REPETITION ----------------
        if speaking_flag:
            flag_repetition = compute_repetition(mouth_hist)

        # ---------------- LIP TREMOR ----------------
        if speaking_flag and not flag_repetition:
            flag_tremor, tremor_score = compute_lip_tremor(
                upper_lip_y_hist,
                lower_lip_y_hist,
                head_stable=head_stable
            )

        # ---------------- BLOCK ----------------
        if speaking_flag and len(mouth_hist) >= 2:
            delta = abs(mouth_hist[-1] - mouth_hist[-2])

            if mouth_open > SPEAKING_MOUTH_THRESH and delta < BLOCK_STATIC_THRESH:
                block_counter += 1
            else:
                block_counter = max(0, block_counter - 1)

            flag_block = block_counter >= BLOCK_MIN_FRAMES
        else:
            block_counter = max(0, block_counter - 1)

        for pt in [nose, upper, lower, left, right]:
            cv2.circle(frame, tuple(pt.astype(int)), 3, (180, 220, 0), -1)

    # ============================================================
    # AUDIO
    # ============================================================

    with audio_lock:
        a_label = latest_audio_label
        a_conf = latest_audio_confidence

    flag_audio = a_label not in ("NoStutteredWords", "No Speech", "Listening...")

    # ============================================================
    # FUSION
    # ============================================================

    active_signals = sum([flag_jerk, flag_tremor, flag_block, flag_audio, flag_repetition])
    stutter_detected = active_signals >= FUSION_MIN_SIGNALS

    # ============================================================
    # CLEAN UI
    # ============================================================

    y = 45
    draw_label(frame, "VocaCare Live Detection", y, (255, 255, 255)); y += 45

    if flag_jerk:
        draw_label(frame, "Head Jerk Detected", y, (0, 80, 255))
        y += 40

    if flag_tremor:
        draw_label(frame, "Lip Tremor Detected", y, (255, 0, 0))
        y += 40

    if flag_audio:
        draw_label(frame, f"Audio: {a_label}", y, (0, 255, 100))
        y += 40

    if stutter_detected:
        cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 200), 4)
        draw_label(frame, "Stutter Detected", y, (0, 50, 255))

    cv2.imshow("VocaCare — Multimodal Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key in (ord('q'), 27):
        break

cap.release()
cv2.destroyAllWindows()