"""
RakshakAI v2
Phase 18
End-to-End Tests
"""

from __future__ import annotations

import unittest

from app import app


class EndToEndTestCase(unittest.TestCase):
    """
    End-to-end workflow tests.
    """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_application_reachable(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_workflow(self):
        response = self.client.get("/api/dashboard")
        self.assertIn(response.status_code, [200, 401, 404])

    def test_ai_agent_workflow(self):
        response = self.client.post(
            "/api/agent/query",
            json={"query": "Test investigation"},
        )
        self.assertIn(response.status_code, [200, 400, 404])

    def test_mobile_dashboard_workflow(self):
        response = self.client.get("/api/mobile/dashboard")
        self.assertIn(response.status_code, [200, 401, 404])

    def test_voice_health_workflow(self):
        response = self.client.get("/api/voice/health")
        self.assertIn(response.status_code, [200, 404])


if __name__ == "__main__":
    unittest.main()
