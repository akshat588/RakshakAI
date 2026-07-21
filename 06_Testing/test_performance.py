"""
RakshakAI v2
Phase 18
Performance Tests
"""

from __future__ import annotations

import time
import unittest

from app import app


class PerformanceTestCase(unittest.TestCase):
    """
    Basic performance validation tests.
    """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_homepage_response_time(self):
        start = time.perf_counter()

        response = self.client.get("/")

        elapsed = time.perf_counter() - start

        self.assertIn(response.status_code, [200, 302])
        self.assertLess(elapsed, 5.0)

    def test_health_response_time(self):
        start = time.perf_counter()

        response = self.client.get("/health")

        elapsed = time.perf_counter() - start

        self.assertIn(response.status_code, [200, 404])
        self.assertLess(elapsed, 5.0)

    def test_dashboard_response_time(self):
        start = time.perf_counter()

        response = self.client.get("/api/dashboard")

        elapsed = time.perf_counter() - start

        self.assertIn(response.status_code, [200, 401, 404])
        self.assertLess(elapsed, 5.0)


if __name__ == "__main__":
    unittest.main()
