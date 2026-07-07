"""
===============================================================================
RakshakAI Backend Configuration
===============================================================================
"""

from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# AI Model Directory
MODEL_ROOT = PROJECT_ROOT / "03_AI_Model_Development" / "saved_models"

NLP_MODEL_DIR = MODEL_ROOT / "nlp"
VISION_MODEL_DIR = MODEL_ROOT / "vision"
AUDIO_MODEL_DIR = MODEL_ROOT / "audio"

HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
