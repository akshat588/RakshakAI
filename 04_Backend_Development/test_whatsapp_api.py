from api.whatsapp import analyze_whatsapp_ai

samples = [
    "Congratulations! You won ₹10 lakh. Click here immediately.",
    "URGENT! Your bank account will be blocked. Verify now: https://fakebank.com",
    "Hi, are we meeting at 6 PM today?",
    "Forward this message to 20 people to avoid account suspension.",
]

for sample in samples:

    print("=" * 80)

    print(sample)

    print()

    result = analyze_whatsapp_ai(sample)

    print(f"Prediction : {result['prediction']}")
    print(f"Result     : {result['result']}")
    print(f"Risk       : {result['risk']}")
    print(f"Confidence : {result['confidence']}")
    print(f"Status     : {result['status']}")

    print("\nEvidence:")
    for item in result["evidence"]:
        print(f"  • {item}")

    print("\nRecommendations:")
    for item in result["recommendations"]:
        print(f"  • {item}")

    print("\nTimeline:")
    for item in result["timeline"]:
        print(f"  • {item}")

    print("\nIOCs:")
    for item in result["iocs"]:
        print(f"  • {item}")
