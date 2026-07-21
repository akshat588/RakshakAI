"""
RakshakAI v2
Performance Monitor
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Any, Callable


class PerformanceMonitor:
    """
    Measures execution time of functions.
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
    ):
        self.logger = logger or logging.getLogger("RakshakAI")

    def measure(self, name: str | None = None):
        """
        Decorator for measuring execution time.
        """

        def decorator(func: Callable):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                start_time = time.perf_counter()

                try:
                    return func(*args, **kwargs)

                finally:

                    elapsed = (time.perf_counter() - start_time) * 1000

                    function_name = name or func.__name__

                    self.logger.info(
                        "[Performance] %s executed in %.2f ms",
                        function_name,
                        elapsed,
                    )

            return wrapper

        return decorator

    def measure_block(
        self,
        name: str,
        start_time: float,
    ) -> None:
        """
        Log execution time for a manual block.
        """

        elapsed = (time.perf_counter() - start_time) * 1000

        self.logger.info(
            "[Performance] %s executed in %.2f ms",
            name,
            elapsed,
        )

    @staticmethod
    def start_timer() -> float:
        """
        Return a high-resolution timer value.
        """

        return time.perf_counter()
