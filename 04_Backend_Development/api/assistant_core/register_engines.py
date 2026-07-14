"""
==========================================================
RakshakAI v2
Universal Engine Registration
==========================================================
"""

from api.assistant_core.orchestrator import orchestrator

from api.email import analyze_email_ai
from api.url import analyze_url_ai
from api.sms import analyze_sms_ai
from api.whatsapp import analyze_whatsapp_ai
from api.upi import analyze_upi_ai
from api.fake_job import analyze_fake_job_ai
from api.social_engineering import analyze_social_engineering_ai

# Optional analyzers
try:
    from api.qr import analyze_qr_ai
except Exception:
    analyze_qr_ai = None

try:
    from api.deepfake import analyze_deepfake_ai
except Exception:
    analyze_deepfake_ai = None

try:
    from api.voice import analyze_voice_ai
except Exception:
    analyze_voice_ai = None

    # ==========================================================
# Register Core Engines
# ==========================================================

orchestrator.register("email", analyze_email_ai)

orchestrator.register("url", analyze_url_ai)

orchestrator.register("sms", analyze_sms_ai)

orchestrator.register("whatsapp", analyze_whatsapp_ai)
orchestrator.register("upi", analyze_upi_ai)

orchestrator.register("fake_job", analyze_fake_job_ai)

orchestrator.register("social_engineering", analyze_social_engineering_ai)

# ==========================================================
# Register Optional Engines
# ==========================================================

if analyze_qr_ai is not None:

    orchestrator.register("qr", analyze_qr_ai)

if analyze_deepfake_ai is not None:

    orchestrator.register("deepfake", analyze_deepfake_ai)

if analyze_voice_ai is not None:

    orchestrator.register("voice", analyze_voice_ai)

    # ==========================================================
# Verification Helpers
# ==========================================================


def registered_engines():
    """
    Returns the list of currently
    registered analyzer engines.
    """

    return orchestrator.available_engines()


def engine_count():
    """
    Returns the number of
    registered analyzer engines.
    """

    return len(orchestrator.available_engines())

    # ==========================================================


# Health Check
# ==========================================================


def health():
    """
    Returns the registration health
    of the Universal Investigation Engine.
    """

    return {
        "status": "healthy",
        "registered_engines": registered_engines(),
        "engine_count": engine_count(),
        "orchestrator_ready": engine_count() > 0,
    }


# ==========================================================
# Debug Information
# ==========================================================


def debug():
    """
    Returns orchestrator debug information.
    """

    return orchestrator.debug()


# ==========================================================
# Initialization
# ==========================================================


def initialize():
    """
    Initializes the Universal Investigation Engine.
    Safe to call multiple times.
    """

    info = health()

    print("=" * 60)
    print(" RakshakAI v2 - Universal Investigation Engine")
    print("=" * 60)
    print(f"Registered Engines : {info['engine_count']}")

    for engine in info["registered_engines"]:

        print(f"  ✓ {engine}")

    print("=" * 60)

    return info


# ==========================================================
# Auto Initialization
# ==========================================================

ENGINE_INFO = initialize()

# ==========================================================
# Validation
# ==========================================================


def validate():
    """
    Validates that all required engines
    are registered correctly.
    """

    required = ["email", "url", "sms", "whatsapp", "upi", "fake_job", "social_engineering"]

    available = set(registered_engines())

    missing = [engine for engine in required if engine not in available]

    return {"valid": len(missing) == 0, "missing": missing, "registered": registered_engines()}


# ==========================================================
# Startup Validation
# ==========================================================

VALIDATION_RESULT = validate()

if VALIDATION_RESULT["valid"]:

    print("✓ Universal Engine Registration Successful")

else:

    print("⚠ Missing Engines:")

    for engine in VALIDATION_RESULT["missing"]:

        print(f"   - {engine}")

        # ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "orchestrator",
    "initialize",
    "health",
    "debug",
    "validate",
    "registered_engines",
    "engine_count",
]

# ==========================================================
# End of File
# ==========================================================
