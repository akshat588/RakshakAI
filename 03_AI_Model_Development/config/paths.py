"""
===============================================================================
RakshakAI Path Configuration
===============================================================================
"""

from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# -----------------------------------------------------------------------------
# Dataset Paths
# -----------------------------------------------------------------------------

DATASET_ROOT = PROJECT_ROOT / "02_Dataset_Design_Collection" / "raw_data"

EMAIL_DATASET = DATASET_ROOT / "email"
URL_DATASET = DATASET_ROOT / "url"
SMS_DATASET = DATASET_ROOT / "sms"
WHATSAPP_DATASET = DATASET_ROOT / "whatsapp"
FAKE_JOB_DATASET = DATASET_ROOT / "fake_job"
SOCIAL_DATASET = DATASET_ROOT / "social_engineering"
UPI_DATASET = DATASET_ROOT / "upi"
QR_DATASET = DATASET_ROOT / "qr"
DEEPFAKE_DATASET = DATASET_ROOT / "deepfake"
VOICE_DATASET = DATASET_ROOT / "voice_scam"

# -----------------------------------------------------------------------------
# AI Module Root
# -----------------------------------------------------------------------------

AI_ROOT = PROJECT_ROOT / "03_AI_Model_Development"

MODEL_DIR = AI_ROOT / "saved_models"

NLP_MODELS = MODEL_DIR / "nlp"
VISION_MODELS = MODEL_DIR / "vision"
AUDIO_MODELS = MODEL_DIR / "audio"

LOG_DIR = AI_ROOT / "logs"

TRAINING_LOGS = LOG_DIR / "training_logs"
EVALUATION_LOGS = LOG_DIR / "evaluation_logs"
