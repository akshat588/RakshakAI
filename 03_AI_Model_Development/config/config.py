"""
=========================================================
RakshakAI - Global Configuration
Project: RakshakAI
=========================================================
"""

from pathlib import Path

# =========================================================
# PROJECT
# =========================================================

PROJECT_NAME = "RakshakAI"

VERSION = "1.0.0"


# =========================================================
# RANDOM SEED
# =========================================================

RANDOM_STATE = 42

# =========================================================
# DATA SPLIT
# =========================================================

TEST_SIZE = 0.20

VALIDATION_SIZE = 0.10

# =========================================================
# NLP CONFIGURATION
# =========================================================

MAX_FEATURES = 10000

NGRAM_RANGE = (1, 2)

MIN_DF = 2

MAX_DF = 0.95

REMOVE_STOPWORDS = True

LOWERCASE = True

REMOVE_PUNCTUATION = True

REMOVE_NUMBERS = False

# =========================================================
# MODEL CONFIGURATION
# =========================================================

EMAIL_MODEL_NAME = "email_detector.pkl"

URL_MODEL_NAME = "url_detector.pkl"

SMS_MODEL_NAME = "sms_detector.pkl"

WHATSAPP_MODEL_NAME = "whatsapp_detector.pkl"

FAKE_JOB_MODEL_NAME = "fake_job_detector.pkl"

SOCIAL_MODEL_NAME = "social_detector.pkl"

QR_MODEL_NAME = "qr_detector.pth"

DEEPFAKE_MODEL_NAME = "deepfake_detector.pth"

VOICE_MODEL_NAME = "voice_detector.pth"

# =========================================================
# IMAGE CONFIGURATION
# =========================================================

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32

NUM_CLASSES = 2

EPOCHS = 15

LEARNING_RATE = 0.0001

# =========================================================
# DEVICE
# =========================================================

import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = "INFO"
