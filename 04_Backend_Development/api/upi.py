from flask import Blueprint, request, jsonify
import pandas as pd
from utils.response_builder import build_response
from utils.risk_mapper import get_risk

from core.model_loader import (
    load_model,
    load_preprocessor,
)

upi_bp = Blueprint("upi", __name__)

model = load_model("upi_detector")
preprocessor = load_preprocessor("upi_preprocessor")


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
            "Risk_Score",
            "Detection_Flag",
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
                    "Risk_Score": data["Risk_Score"],
                    "Detection_Flag": data["Detection_Flag"],
                }
            ]
        )

        features = preprocessor.transform(df)

        prediction = int(model.predict(features)[0])

        return jsonify(
            build_response(
                engine="UPI Fraud Detector",
                prediction=prediction,
                result=(
                    "Fraudulent Transaction"
                    if prediction == 1
                    else "Legitimate Transaction"
                ),
                risk="HIGH" if prediction == 1 else "LOW",
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
