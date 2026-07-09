from typing import Any


def calculate_result(
    prediction,
    probabilities,
    classes,
    safe_label,
    phishing_label,
):
    """
    Universal Threat Scoring Engine
    Works with string labels and integer labels.
    """

    # Convert numpy values
    if hasattr(prediction, "item"):
        prediction = prediction.item()

    classes = list(classes)

    # Find phishing probability index
    phishing_index = classes.index(phishing_label)

    # Threat Score
    threat_score = round(float(probabilities[phishing_index]) * 100, 2)

    # Model Confidence
    confidence = round(float(max(probabilities)) * 100, 2)

    # Risk Mapping
    if threat_score >= 85:
        risk = "CRITICAL"
    elif threat_score >= 65:
        risk = "HIGH"
    elif threat_score >= 50:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Result
    if prediction == safe_label:
        result = safe_label
    else:
        result = phishing_label

    return {
        "prediction": prediction,
        "result": result,
        "confidence": confidence,
        "risk_score": threat_score,
        "risk": risk,
    }
