from flask import Blueprint, request, jsonify
import pandas as pd

from core.model_loader import (
    load_model,
    load_preprocessor,
)

from utils.response_builder import build_response
from utils.history_manager import save_scan

from api.assistant_core.entity_extractor import extractor

upi_bp = Blueprint("upi", __name__)

model = load_model("upi_detector")
preprocessor = load_preprocessor("upi_preprocessor")


def analyze_upi_ai(text: str):

    data = extractor.build_upi_features(text)

    risk_score = 0

    risk_factors = []

    amount = float(data["Transaction_Amount"])

    hour = int(data["Transaction_Time"].split(":")[0])

    if amount >= 50000:

        risk_score += 35

        risk_factors.append("High Transaction Amount")

    elif amount >= 20000:

        risk_score += 20

        risk_factors.append("Medium Transaction Amount")

    elif amount >= 10000:

        risk_score += 10

    if hour >= 23 or hour <= 5:

        risk_score += 15

        risk_factors.append("Late Night Transaction")

    if data["Channel"] == "QR":

        risk_score += 10

        risk_factors.append("QR Payment")

    if data["Transaction_Type"] == "Debit":

        risk_score += 10

    merchant = data["Merchant_Name"].lower()

    if any(
        word in merchant
        for word in [
            "gift",
            "reward",
            "bonus",
            "lottery",
            "cash",
            "prize",
            "unknown",
        ]
    ):

        risk_score += 20

        risk_factors.append("Unknown Merchant")

    if data["Bank_Name"] in [
        "Unknown Bank",
        "Demo Bank",
    ]:

        risk_score += 10

        risk_factors.append("High Risk Bank")

    detection_flag = 1 if risk_score >= 70 else 0

    df = pd.DataFrame([{**data, "Risk_Score": risk_score, "Detection_Flag": detection_flag}])

    features = preprocessor.transform(df)

    prediction = int(model.predict(features)[0])

    return {
        "prediction": prediction,
        "result": "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction",
        "risk": "HIGH" if prediction == 1 else "LOW",
        "confidence": risk_score,
        "risk_score": risk_score,
        "status": "Threat Detected" if prediction == 1 else "Appears Safe",
        "evidence": risk_factors,
        "recommendations": ["Verify the recipient before making payment."],
        "timeline": ["UPI entity extraction completed.", "Structured AI model executed."],
        "iocs": [data["Merchant_Name"]],
    }


@upi_bp.route("/api/upi", methods=["POST"])
def analyze_upi():
    try:
        data = request.get_json()

        required_fields = [
            "Bank_Name",
            "Transaction_Amount",
            "Transaction_Date",
            "Transaction_Time",
            "Merchant_Name",
            "Location_City",
            "Location_State",
            "Transaction_Type",
            "Channel",
        ]

        missing = [field for field in required_fields if field not in data]

        if missing:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Missing fields: {', '.join(missing)}",
                    }
                ),
                400,
            )
        # ==================================================
        # RakshakAI AI Risk Engine
        # ==================================================

        risk_score = 0
        risk_factors = []

        amount = float(data["Transaction_Amount"])
        hour = int(data["Transaction_Time"].split(":")[0])

        # Transaction Amount
        if amount >= 50000:
            risk_score += 35
            risk_factors.append("High Transaction Amount")
        elif amount >= 20000:
            risk_score += 20
            risk_factors.append("Medium Transaction Amount")
        elif amount >= 10000:
            risk_score += 10

        # Late Night
        if hour >= 23 or hour <= 5:
            risk_score += 15
            risk_factors.append("Late Night Transaction")

        # Channel
        if data["Channel"] == "QR":
            risk_score += 10
            risk_factors.append("QR Payment")

        # Debit
        if data["Transaction_Type"] == "Debit":
            risk_score += 10

        merchant = data["Merchant_Name"].lower()

        keywords = [
            "unknown",
            "gift",
            "reward",
            "bonus",
            "lottery",
            "cash",
            "prize",
        ]

        if any(word in merchant for word in keywords):
            risk_score += 20
            risk_factors.append("Unknown Merchant")

        # High Risk Banks

        high_risk_banks = ["Unknown Bank", "Demo Bank"]

        if data["Bank_Name"] in high_risk_banks:
            risk_score += 10
            risk_factors.append("High Risk Bank")

        # Round Amount

        if amount % 10000 == 0:
            risk_score += 5
            risk_factors.append("Round Amount Pattern")

        risk_score = min(risk_score, 100)

        detection_flag = 1 if risk_score >= 70 else 0
        df = pd.DataFrame(
            [
                {
                    "Bank_Name": data["Bank_Name"],
                    "Transaction_Amount": data["Transaction_Amount"],
                    "Transaction_Date": data["Transaction_Date"],
                    "Transaction_Time": data["Transaction_Time"],
                    "Merchant_Name": data["Merchant_Name"],
                    "Location_City": data["Location_City"],
                    "Location_State": data["Location_State"],
                    "Transaction_Type": data["Transaction_Type"],
                    "Channel": data["Channel"],
                    "Risk_Score": risk_score,
                    "Detection_Flag": detection_flag,
                }
            ]
        )

        result = analyze_upi_ai(str(data))

        response = build_response(
            engine="UPI Fraud Detector",
            prediction=result["prediction"],
            result=result["result"],
            risk=result["risk"],
            confidence=result["confidence"],
            risk_score=result["risk_score"],
        )

        response.update(
            {
                "analyzer": "upi",
                "status": result["status"],
                "original_input": data,
                "evidence": result["evidence"],
                "recommendations": result["recommendations"],
                "timeline": result["timeline"],
                "iocs": result["iocs"],
            }
        )

        save_scan(response)

        return jsonify(response)

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
