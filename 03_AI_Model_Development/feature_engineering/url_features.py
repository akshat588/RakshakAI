"""
===============================================================================
RakshakAI - URL Feature Engineering
===============================================================================
"""

import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "bank",
    "paypal",
    "signin",
    "confirm",
    "password",
]


SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "ow.ly",
    "is.gd",
]


def extract_url_features(url: str):

    url = str(url).lower()

    parsed = urlparse(url)

    features = {
        "url_length": len(url),
        "num_digits": sum(c.isdigit() for c in url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "num_at": url.count("@"),
        "num_question": url.count("?"),
        "https": int(url.startswith("https")),
        "http": int(url.startswith("http")),
        "ip_address": int(
            bool(
                re.search(
                    r"(?:\d{1,3}\.){3}\d{1,3}",
                    url,
                )
            )
        ),
        "shortener": int(any(short in url for short in SHORTENERS)),
        "suspicious_words": sum(word in url for word in SUSPICIOUS_WORDS),
    }

    return features
