import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import threading
import sounddevice as sd
import torch
import torch.nn.functional as F
from transformers import AutoProcessor, AutoModelForAudioClassification

# ---------------- LOAD AUDIO MODEL ----------------

model_name = "Huma10/Whisper_Stuttered_Speech"

processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)

latest_audio_label = "Listening..."

# ---------------- AUDIO THREAD ----------------

def audio_worker():
    global latest_audio_label

    sr = 16000
    buffer = []

    def callback(indata, frames, time, status):
        buffer.append(indata.copy())

    stream = sd.InputStream(samplerate=sr, channels=1, callback=callback)

    with stream:
        while True:
            if len(buffer) > 10:  # ~1 sec audio
                audio = np.concatenate(buffer, axis=0).flatten()
                buffer.clear()

                if np.mean(np.abs(audio)) < 0.01:
                    latest_audio_label = "No Speech"
                    continue

                inputs = processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=30 * 16000
                )

                with torch.no_grad():
                    outputs = model(**inputs)

                probs = F.softmax(outputs.logits, dim=-1)
                confidence, pred_id = torch.max(probs, dim=-1)

                if confidence.item() < 0.6:
                    latest_audio_label = "NoStutteredWords"
                else:
                    latest_audio_label = model.config.id2label[pred_id.item()]


# ---------------- START AUDIO THREAD ----------------

threading.Thread(target=audio_worker, daemon=True).start()


# ---------------- VIDEO SETUP ----------------

mp_face = mp.solutions.face_mesh

face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

prev_nose = None
lip_history = deque(maxlen=10)

freeze_counter = 0

# ---------------- VIDEO LOOP ----------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0]

        nose = face.landmark[1]
        upper_lip = face.landmark[13]
        lower_lip = face.landmark[14]
        left_lip = face.landmark[61]
        right_lip = face.landmark[291]

        nose_xy = np.array([nose.x*w, nose.y*h])
        upper_xy = np.array([upper_lip.x*w, upper_lip.y*h])
        lower_xy = np.array([lower_lip.x*w, lower_lip.y*h])
        left_xy = np.array([left_lip.x*w, left_lip.y*h])
        right_xy = np.array([right_lip.x*w, right_lip.y*h])

        # Head movement
        if prev_nose is not None:
            movement = np.linalg.norm(nose_xy - prev_nose)
            if movement > 25:
                cv2.putText(frame, "HEAD JERK", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        prev_nose = nose_xy

        # Mouth open
        mouth_open = np.linalg.norm(upper_xy - lower_xy)
        cv2.putText(frame, f"Mouth: {int(mouth_open)}", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        # Lip tremor
        lip_width = np.linalg.norm(left_xy - right_xy)
        lip_history.append(lip_width)

        if len(lip_history) > 5:
            if np.std(lip_history) > 3:
                cv2.putText(frame, "LIP TREMOR", (30,150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        # Freeze detection
        if mouth_open > 10 and len(lip_history) > 2:
            change = abs(lip_history[-1] - lip_history[-2])
            if change < 0.5:
                freeze_counter += 1
            else:
                freeze_counter = 0

            if freeze_counter > 15:
                cv2.putText(frame, "BLOCK DETECTED", (30,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    # ---------------- AUDIO OUTPUT ON SCREEN ----------------

    cv2.putText(frame, f"Audio: {latest_audio_label}", (30, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, "Press Q to exit", (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow("VocaCare - Multimodal Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()