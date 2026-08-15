
from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests import RequestException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class HealthChecker:

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def check(self, url: str) -> dict[str, Any]:
        started_at = time.perf_counter()

        try:
            response = requests.get(url, timeout=self.timeout)
            response_time_ms = round((time.perf_counter() - started_at) * 1000, 2)

            if response.ok:
                result = {
                    "status": "ok",
                    "response_time_ms": response_time_ms,
                }
            else:
                result = {
                    "status": "error",
                    "code": response.status_code,
                }

            self.logger.info("health_check_finished", extra={"url": url, **result})
            return result

        except RequestException as exc:
            self.logger.error(
                "health_check_failed",
                extra={"url": url, "error": str(exc)},
            )
            return {"status": "error", "code": None}


if __name__ == "__main__":
    checker = HealthChecker()
    print(checker.check("https://jsonplaceholder.typicode.com"))
