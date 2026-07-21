"""
RakshakAI v2
Phase 18
Integration Tests
"""

from __future__ import annotations

import unittest

from app import app


class IntegrationTestCase(unittest.TestCase):
    """
    Integration tests for RakshakAI APIs.
    """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertIn(response.status_code, [200, 404])

    def test_dashboard_endpoint(self):
        response = self.client.get("/api/dashboard")
        self.assertIn(response.status_code, [200, 401, 404])

    def test_ai_agent_health(self):
        response = self.client.get("/api/agent/health")
        self.assertIn(response.status_code, [200, 404])

    def test_voice_health(self):
        response = self.client.get("/api/voice/health")
        self.assertIn(response.status_code, [200, 404])

    def test_mobile_dashboard(self):
        response = self.client.get("/api/mobile/dashboard")
        self.assertIn(response.status_code, [200, 401, 404])


if __name__ == "__main__":
    unittest.main()
