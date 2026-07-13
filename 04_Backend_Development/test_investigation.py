from api.assistant_core.investigation import InvestigationEngine

sample = {
    "prediction": 1,
    "result": "Phishing Email",
    "risk": "HIGH",
    "confidence": 98.3,
    "risk_score": 94,
}

report = InvestigationEngine.build(
    analyzer="Email Detector", engine_result=sample, original_input="Click here immediately"
)

print(report)
