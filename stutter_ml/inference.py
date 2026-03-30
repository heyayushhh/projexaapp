def run_inference(classifier, chunks, timestamps):
    results = []

    for chunk, (start, end) in zip(chunks, timestamps):
        prediction = classifier(chunk)

        label = prediction[0]["label"]
        score = prediction[0]["score"]

        results.append({
            "start": start,
            "end": end,
            "label": label,
            "confidence": score
        })

    return results