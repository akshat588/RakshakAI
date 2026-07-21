"""
RakshakAI v2
Phase 18
Security Tests
"""

from __future__ import annotations

import unittest

from app import app


class SecurityTestCase(unittest.TestCase):
    """
    Basic security validation tests.
    """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_security_headers(self):
        response = self.client.get("/")

        self.assertIn(response.status_code, [200, 302])

        headers = response.headers

        expected_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy",
        ]

        for header in expected_headers:
            self.assertTrue(header in headers or response.status_code == 302)

    def test_invalid_route(self):
        response = self.client.get("/this-route-does-not-exist")
        self.assertIn(response.status_code, [404])

    def test_invalid_method(self):
        response = self.client.put("/")
        self.assertIn(response.status_code, [405, 404])

    def test_large_invalid_request(self):
        response = self.client.post(
            "/api/agent/query",
            json={"query": "A" * 100000},
        )

        self.assertIn(
            response.status_code,
            [200, 400, 404, 413],
        )


if __name__ == "__main__":
    unittest.main()
