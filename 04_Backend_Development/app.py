"""
===============================================================================
RakshakAI Backend
Main Flask Application
===============================================================================
"""

from flask import Flask, render_template
from flask_cors import CORS
from api.qr import qr_bp
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
from api.qr import qr_bp
from api.twilio import twilio_bp
from api.deepfake import deepfake_bp
from api.history import history_bp

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
app.register_blueprint(twilio_bp)
app.register_blueprint(upi_bp)
app.register_blueprint(fake_job_bp)
app.register_blueprint(social_bp)
app.register_blueprint(qr_bp)
app.register_blueprint(deepfake_bp)
app.register_blueprint(history_bp)

# ==========================
# Home Route
# ==========================


@app.route("/")
def home():
    return render_template("pages/dashboard.html")


# ==========================
# Health Check
# ==========================


@app.route("/health")
def health():
    return {"status": "healthy", "server": "running"}


# ==========================
# Frontend Pages
# ==========================


@app.route("/email")
def email_page():
    return render_template("analyzers/email.html")


@app.route("/url")
def url_page():
    return render_template("analyzers/url.html")


@app.route("/sms")
def sms_page():
    return render_template("analyzers/sms.html")


@app.route("/whatsapp")
def whatsapp_page():
    return render_template("analyzers/whatsapp.html")


@app.route("/fake-job")
def fake_job_page():
    return render_template("analyzers/fake_job.html")


@app.route("/social-engineering")
def social_engineering_page():
    return render_template("analyzers/social_engineering.html")


@app.route("/upi")
def upi_page():
    return render_template("analyzers/upi.html")


@app.route("/qr")
def qr_page():
    return render_template("analyzers/qr.html")


@app.route("/qr/result")
def qr_result_page():
    return render_template("analyzers/qr_result.html")


@app.route("/deepfake")
def deepfake_page():
    return render_template("analyzers/deepfake.html")


@app.route("/deepfake-result")
def deepfake_result_page():
    return render_template("analyzers/deepfake_result.html")


@app.route("/scan-history")
def scan_history_page():
    return render_template("analyzers/scan_history.html")


# ==========================
# Run Server
# ==========================

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
