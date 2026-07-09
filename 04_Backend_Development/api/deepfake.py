from flask import Blueprint, request, jsonify

import os
import uuid

import torch
import torch.nn as nn
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
from PIL import Image

from torchvision import transforms
from torchvision.models import (
    resnet18,
)

deepfake_bp = Blueprint("deepfake", __name__)

# ==========================================================
# Load Model
# ==========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "03_AI_Model_Development",
    "saved_models",
    "vision",
    "deepfake_detector.pth",
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = resnet18(weights=None)

model.fc = nn.Linear(
    model.fc.in_features,
    2,
)

from core.model_loader import load_torch_model

model = load_torch_model(
    MODEL_PATH,
    model,
)

model.to(DEVICE)

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)

# ==========================================================
# API
# ==========================================================


@deepfake_bp.route("/api/deepfake", methods=["POST"])
def analyze_deepfake():

    try:

        if "image" not in request.files:

            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Image not uploaded",
                    }
                ),
                400,
            )

        file = request.files["image"]

        file.stream.seek(0)

        image = Image.open(file.stream).convert("RGB")

        image = transform(image).unsqueeze(0)

        image = image.to(DEVICE)

        with torch.no_grad():

            outputs = model(image)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )

        confidence, prediction = torch.max(
            probabilities,
            1,
        )

        prediction = int(prediction.item())

        confidence = round(
            confidence.item() * 100,
            2,
        )

        risk_score = confidence

        if prediction == 0:

            result = "Deepfake Image"

            risk = "HIGH"

            explanation = [
                "AI-generated facial patterns detected.",
                "Deep learning model classified the image as manipulated.",
            ]

            recommendation = [
                "Do not trust this image without verification.",
                "Cross-check with the original source.",
            ]

        else:

            result = "Authentic Image"

            risk = "LOW"

            explanation = [
                "No significant manipulation detected.",
            ]

            recommendation = [
                "Image appears authentic.",
            ]

        response = {
            "success": True,
            "engine": "Deepfake Detector",
            "prediction": result,
            "risk": risk,
            "confidence": confidence,
            "risk_score": risk_score,
            "scan_id": "RK-DF-" + uuid.uuid4().hex[:8].upper(),
            "explanation": explanation,
            "recommendation": recommendation,
        }

        save_scan(response)

        return jsonify(response)

    except Exception as e:

        import traceback

        traceback.print_exc()

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                }
            ),
            500,
        )
