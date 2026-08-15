#!/usr/bin/env bash
set -euo pipefail

echo "Inicializando repositorio..."
git init
git checkout -b main

git config user.name "Victor"
git config user.email "victor@example.com"

echo "Criando healthcheck inicial..."
cat > healthcheck.py <<'PY'
"""Health check HTTP simples."""

from __future__ import annotations

import requests


def health_check(url: str) -> dict[str, object]:
    """Executa uma verificacao HTTP simples."""
    response = requests.get(url, timeout=10)
    return {"status": "ok", "code": response.status_code}
PY

git add healthcheck.py
git commit -m "chore: add initial healthcheck script"

echo "Criando branch feat/health-check-endpoint..."
git checkout -b feat/health-check-endpoint

echo "Adicionando classe HealthChecker..."
cat > healthcheck.py <<'PY'
"""Health checker HTTP com logging estruturado."""

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
    """Executa health checks HTTP e retorna status padronizado."""

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def check(self, url: str) -> dict[str, Any]:
        """Verifica uma URL e retorna status com tempo de resposta ou erro."""
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
PY

git add healthcheck.py
git commit -m "feat: add HTTP health check endpoint

Add HealthChecker class that performs HTTP GET requests
and returns status with response time measurement.

Closes #1"

echo "Fazendo merge para main..."
git checkout main
git merge feat/health-check-endpoint

echo "Gerando CHANGELOG..."
cat > CHANGELOG.md <<'MD'
# Changelog

## 1.0.0 - 2026-08-13

### Added

- Added `HealthChecker` class for HTTP health checks.
- Added structured logging for successful and failed checks.
- Added response time measurement for successful requests.
MD

git add CHANGELOG.md
git commit -m "docs: add changelog for health check feature"

echo "Workflow concluido!"
git log --oneline --graph --all
