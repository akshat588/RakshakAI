from api.assistant_core.router import UniversalRouter
from api.assistant_core.detector import InputType

tests = [
    InputType.EMAIL,
    InputType.URL,
    InputType.SMS,
    InputType.WHATSAPP,
    InputType.UPI,
    InputType.FAKE_JOB,
    InputType.SOCIAL_ENGINEERING,
    InputType.QR,
    InputType.DEEPFAKE,
    InputType.VOICE,
]

for item in tests:
    print(item, "->", UniversalRouter.get_route(item))
