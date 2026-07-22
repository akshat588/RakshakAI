"""
Twilio WhatsApp webhook integration
- Endpoint: POST /api/twilio
- Accepts Twilio webhook form-data for incoming WhatsApp messages/media
- Downloads media using Twilio Account SID/Auth Token
- Detects QR codes, runs existing analyze_payload from api.qr, and replies with TwiML

Environment variables expected:
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN

Optional:
- TWILIO_VALIDATE_SIGNATURE=true|false (default: true)
- TWILIO_WEBHOOK_URL=https://<public-host>/api/twilio
"""

from flask import Blueprint, request, Response
import os
import requests
import io
import hmac
import hashlib
import base64
from PIL import Image
import numpy as np
import cv2

# Reuse QR analyzer logic
try:
    from api.qr import analyze_payload as analyze_qr_payload
except Exception:
    analyze_qr_payload = None


twilio_bp = Blueprint("twilio", __name__)


def decode_qr_from_bytes(img_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(image)
        if points is None or not data:
            return None
        return data
    except Exception:
        return None


def _build_signature(url: str, params: dict, auth_token: str) -> str:
    validation_str = url
    for key in sorted(params.keys()):
        values = params[key]
        for value in values:
            validation_str += key + value
    digest = hmac.new(auth_token.encode("utf-8"), validation_str.encode("utf-8"), hashlib.sha1).digest()
    return base64.b64encode(digest).decode("utf-8")


def _is_valid_twilio_signature(auth_token: str, twilio_sig: str) -> bool:
    params = request.form.to_dict(flat=False)

    candidate_urls = []

    # Highest priority: exact public webhook URL configured in Twilio Console.
    configured_public_url = os.getenv("TWILIO_WEBHOOK_URL", "").strip()
    if configured_public_url:
        candidate_urls.append(configured_public_url)

    # Next priority: proxy forwarded URL (common with ngrok/reverse proxy).
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
    forwarded_host = request.headers.get("X-Forwarded-Host", "")
    if forwarded_proto and forwarded_host:
        candidate_urls.append(f"{forwarded_proto}://{forwarded_host}{request.path}")

    # Fallback local URL seen by Flask.
    candidate_urls.append(request.url)

    # De-duplicate while preserving order.
    seen = set()
    normalized_urls = []
    for url in candidate_urls:
        if url and (url not in seen):
            normalized_urls.append(url)
            seen.add(url)

    for url in normalized_urls:
        computed_sig = _build_signature(url, params, auth_token)
        if hmac.compare_digest(computed_sig, twilio_sig):
            return True

    return False


@twilio_bp.route("/api/twilio", methods=["POST"])
def twilio_webhook():
    """Handle incoming Twilio webhook for WhatsApp messages and media."""
    try:
        # Validate Twilio signature when enabled
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        validate_signature = os.getenv("TWILIO_VALIDATE_SIGNATURE", "true").strip().lower() == "true"
        twilio_sig = request.headers.get("X-Twilio-Signature", "")

        if validate_signature and auth_token and twilio_sig:
            if not _is_valid_twilio_signature(auth_token, twilio_sig):
                twiml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>Invalid Twilio signature.</Message></Response>"
                return Response(twiml, mimetype="text/xml"), 403

        # Twilio sends form-encoded data
        num_media = int(request.form.get("NumMedia", 0))
        body = request.form.get("Body", "").strip()

        # Text-only flow
        if num_media == 0:
            reply = "Thanks - send an image of the QR code and I will analyze it."
            if body:
                reply = f"Received text. To analyze QR images, please send the QR image.\nYou said: {body[:400]}"
            twiml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{reply}</Message></Response>"
            return Response(twiml, mimetype="text/xml")

        # Process first media only
        media_url = request.form.get("MediaUrl0")
        if not media_url:
            twiml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>No media URL found.</Message></Response>"
            return Response(twiml, mimetype="text/xml")

        # Download media from Twilio using Basic Auth
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            twiml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>Server misconfigured: missing Twilio credentials.</Message></Response>"
            return Response(twiml, mimetype="text/xml"), 500

        resp = requests.get(media_url, auth=(account_sid, auth_token), timeout=20)
        if resp.status_code != 200:
            twiml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>Unable to download media (status {resp.status_code}).</Message></Response>"
            return Response(twiml, mimetype="text/xml"), 502

        decoded = decode_qr_from_bytes(resp.content)
        if not decoded:
            twiml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>No QR code detected in the image. Please send a clear picture of the QR code.</Message></Response>"
            return Response(twiml, mimetype="text/xml")

        if analyze_qr_payload is None:
            reply = f"Decoded QR: {decoded}\n(RakshakAI analysis not available)"
            twiml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{reply}</Message></Response>"
            return Response(twiml, mimetype="text/xml")

        result = analyze_qr_payload(decoded)

        lines = [
            "RakshakAI QR Analysis",
            f"Prediction: {result.get('prediction', 'Unknown')}",
            f"Risk: {result.get('risk', '-')}",
        ]

        if "risk_score" in result:
            lines.append(f"Threat Score: {result.get('risk_score')}%")
        if "confidence" in result:
            lines.append(f"Confidence: {result.get('confidence')}%")

        decoded_preview = result.get("decoded_content") or decoded
        if len(decoded_preview) > 400:
            decoded_preview = decoded_preview[:400] + "..."
        lines.append(f"Decoded: {decoded_preview}")

        flags = result.get("flags") or []
        if flags:
            lines.append("Indicators: " + ", ".join(flags[:6]))

        recs = result.get("recommendation") or []
        if recs:
            lines.append("Recommendations: " + "; ".join(recs[:3]))

        reply_text = "\n".join(lines)
        twiml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{reply_text}</Message></Response>"
        return Response(twiml, mimetype="text/xml")

    except Exception as e:
        twiml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>Internal server error: {str(e)}</Message></Response>"
        return Response(twiml, mimetype="text/xml"), 500


