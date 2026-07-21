"""
RakshakAI v2
Production Configuration
"""

from __future__ import annotations

import os


class ProductionConfig:
    """
    Production configuration.
    """

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key",
    )

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True

    JSON_SORT_KEYS = False

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads",
    )

    REPORT_FOLDER = os.getenv(
        "REPORT_FOLDER",
        "reports",
    )

    MODEL_DIRECTORY = os.getenv(
        "MODEL_DIRECTORY",
        "models",
    )

    CACHE_ENABLED = True

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    THREAT_CACHE_TIMEOUT = 3600

    PROVIDER_CACHE_TIMEOUT = 1800

    DATABASE_POOL_SIZE = 10

    DATABASE_MAX_OVERFLOW = 20

    API_RATE_LIMIT = "100/minute"

    ENABLE_AUDIT_LOGS = True

    ENABLE_SECURITY_HEADERS = True

    ENABLE_COMPRESSION = True
