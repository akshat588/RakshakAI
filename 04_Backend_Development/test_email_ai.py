from api.email import analyze_email_ai

sample = """
Dear Customer,

Your account has been suspended.

Click below immediately.

https://fake-bank-login.com

"""

print(analyze_email_ai(sample))
