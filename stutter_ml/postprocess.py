def post_process(results, threshold=0.6):
    # filter low confidence
    filtered = [r for r in results if r["confidence"] > threshold]

    # merge nearby segments
    merged = []
    for r in filtered:
        if not merged:
            merged.append(r)
            continue

        last = merged[-1]

        if r["start"] - last["end"] < 0.5:
            last["end"] = r["end"]
        else:
            merged.append(r)

    return merged