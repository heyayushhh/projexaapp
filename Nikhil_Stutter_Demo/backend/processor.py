import os
import json
from audio_model import AudioStutterDetector
from visual_model import VisualStutterDetector

audio_detector = AudioStutterDetector()
visual_detector = VisualStutterDetector()


def process_session(session_path):
    audio_path = os.path.join(session_path, "audio.wav")
    video_path = os.path.join(session_path, "video.webm")
    output_path = os.path.join(session_path, "results.json")

    print("Processing audio...")
    audio_results = audio_detector.predict(audio_path)

    print("Processing video...")
    visual_results = visual_detector.detect(video_path)

    combined = audio_results + visual_results
    combined.sort(key=lambda x: x["start"])

    # 🔥 SUMMARY
    total = len(combined)

    type_count = {}
    visual_count = 0

    for e in combined:
        t = e["type"]
        type_count[t] = type_count.get(t, 0) + 1

        if t == "head_jerk":
            visual_count += 1

    most_common = max(type_count, key=type_count.get) if type_count else "None"

    # 🔥 INSIGHTS
    insights = []

    if "block" in type_count:
        insights.append("You tend to pause or block during speech.")

    if "sound_rep" in type_count or "word_rep" in type_count:
        insights.append("Repetition patterns detected in your speech.")

    if visual_count > 0:
        insights.append("Facial tension or head movement detected during stuttering.")

    if total > 5:
        insights.append("High frequency of stuttering observed.")

    summary = {
        "total_events": total,
        "most_common": most_common,
        "visual_events": visual_count
    }

    final_output = {
        "events": combined,
        "summary": summary,
        "insights": insights
    }

    with open(output_path, "w") as f:
        json.dump(final_output, f, indent=4)

    return final_output