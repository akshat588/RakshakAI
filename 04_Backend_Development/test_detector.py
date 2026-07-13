from api.assistant_core.detector import UniversalInputDetector

samples = [
    "https://google.com",
    "support@gmail.com",
    "akshat@ybl",
    "Urgent! Verify your OTP immediately.",
    "Hiring Python Developer. Salary 12 LPA.",
    "Forwarded many times",
    "Congratulations! You won ₹10 lakh.",
]

for sample in samples:
    print(sample)
    print("->", UniversalInputDetector.detect(sample))
    print("-" * 50)
