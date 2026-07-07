"""
===============================================================================
RakshakAI Backend
Main Flask Application
===============================================================================
"""

from flask import Flask
from flask_cors import CORS

import config

# ==========================
# Import Blueprints
# ==========================

from api.email import email_bp
from api.url import url_bp
from api.sms import sms_bp
from api.whatsapp import whatsapp_bp
from api.upi import upi_bp
from api.fake_job import fake_job_bp
from api.social_engineering import social_bp

# ==========================
# Flask App
# ==========================

app = Flask(__name__)

CORS(app)

# ==========================
# Register Blueprints
# ==========================

app.register_blueprint(email_bp)
app.register_blueprint(url_bp)
app.register_blueprint(sms_bp)
app.register_blueprint(whatsapp_bp)
app.register_blueprint(upi_bp)
app.register_blueprint(fake_job_bp)
app.register_blueprint(social_bp)

# ==========================
# Home Route
# ==========================


@app.route("/")
def home():
    return {
        "project": "RakshakAI",
        "version": "1.0",
        "status": "Running",
        "backend": "Active",
    }


# ==========================
# Health Check
# ==========================


@app.route("/health")
def health():
    return {"status": "healthy", "server": "running"}


# ==========================
# Run Server
# ==========================

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
