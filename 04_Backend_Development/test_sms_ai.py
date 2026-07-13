from api.sms import analyze_sms_ai

sample = """
Dear Customer,

Your KYC has expired.

Click the link below immediately to avoid account suspension.

"""

print(analyze_sms_ai(sample))
