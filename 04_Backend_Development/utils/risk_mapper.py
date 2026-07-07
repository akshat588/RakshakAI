def get_risk(prediction):

    label = str(prediction).lower()

    high_keywords = [
        "phishing",
        "spam",
        "scam",
        "fraud",
        "lottery",
        "fake",
        "malicious",
        "social engineering",
    ]

    return "HIGH" if any(word in label for word in high_keywords) else "LOW"
