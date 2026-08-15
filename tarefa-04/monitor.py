
from __future__ import annotations

import argparse
import json
import logging
import os
import socket
import ssl
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
import yaml
from requests import RequestException, Response


class URLMonitor:

    def __init__(
        self,
        urls: list[str],
        max_retries: int = 3,
        timeout: int = 10,
        output_dir: str | Path = "./output",
    ) -> None:
        self.urls = urls
        self.max_retries = max_retries
        self.timeout = timeout
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(self.__class__.__name__)

    def check_url(self, url: str) -> dict[str, Any]:
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            started_at = time.perf_counter()

            try:
                self.logger.info("checking_url", extra={"url": url, "attempt": attempt})
                response = requests.get(url, timeout=self.timeout)
                response_time_ms = round((time.perf_counter() - started_at) * 1000, 2)

                result = self.build_success_result(url, response, response_time_ms, attempt)
                self.logger.info("url_checked", extra=result)
                return result

            except requests.Timeout as exc:
                last_error = self.build_error_result(url, "timeout", str(exc), attempt)
            except requests.exceptions.SSLError as exc:
                last_error = self.build_error_result(url, "ssl_error", str(exc), attempt)
            except requests.exceptions.ConnectionError as exc:
                error_type = self.classify_connection_error(exc)
                last_error = self.build_error_result(url, error_type, str(exc), attempt)
            except RequestException as exc:
                last_error = self.build_error_result(url, "request_error", str(exc), attempt)

            self.logger.warning("url_check_failed", extra=last_error)

            if attempt < self.max_retries:
                wait_seconds = 2 ** (attempt - 1)
                self.logger.info(
                    "waiting_before_retry",
                    extra={
                        "url": url,
                        "attempt": attempt,
                        "wait_seconds": wait_seconds,
                    },
                )
                time.sleep(wait_seconds)

        return last_error or self.build_error_result(
            url=url,
            error_type="unknown_error",
            message="Falha desconhecida ao verificar URL.",
            attempt=self.max_retries,
        )

    def build_success_result(
        self,
        url: str,
        response: Response,
        response_time_ms: float,
        attempt: int,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "status": "ok" if response.ok else "http_error",
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "attempts": attempt,
            "checked_at": datetime.now(UTC).isoformat(),
            "error_type": None,
            "error_message": None,
        }

    def build_error_result(
        self,
        url: str,
        error_type: str,
        message: str,
        attempt: int,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "status": "error",
            "status_code": None,
            "response_time_ms": None,
            "attempts": attempt,
            "checked_at": datetime.now(UTC).isoformat(),
            "error_type": error_type,
            "error_message": message,
        }

    def classify_connection_error(self, exc: requests.exceptions.ConnectionError) -> str:
        error_text = str(exc).lower()

        if isinstance(exc.__cause__, socket.gaierror) or "name resolution" in error_text:
            return "dns_error"

        if isinstance(exc.__cause__, ssl.SSLError):
            return "ssl_error"

        return "connection_error"

    def run(self) -> dict[str, Any]:
        results = [self.check_url(url) for url in self.urls]
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "summary": self.build_summary(results),
            "results": results,
        }

        self.save_results(report)
        return report

    def build_summary(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(results)
        successful = len([result for result in results if result["status"] == "ok"])

        return {
            "total_urls": total,
            "successful": successful,
            "failed": total - successful,
        }

    def save_results(self, report: dict[str, Any]) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"monitor_results_{timestamp}.json"

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2)

        return output_path


class JsonFormatter(logging.Formatter):

    RESERVED_FIELDS = set(
        logging.LogRecord(
            name="",
            level=0,
            pathname="",
            lineno=0,
            msg="",
            args=(),
            exc_info=None,
        ).__dict__
    )

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key not in self.RESERVED_FIELDS:
                payload[key] = value

        return json.dumps(payload, ensure_ascii=False)


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Arquivo de configuracao nao encontrado: {path}") from exc
    except yaml.YAMLError as exc:
        raise RuntimeError("Arquivo YAML invalido.") from exc

    if not isinstance(config, dict):
        raise RuntimeError("A configuracao precisa ser um objeto YAML.")

    return config


def configure_logging(log_level: str, log_file: str | Path) -> None:
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, log_level.upper(), logging.INFO)
    formatter = JsonFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console_handler, file_handler],
        force=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitora URLs com Docker.")
    parser.add_argument(
        "--config",
        default=os.getenv("CONFIG_PATH", "config.yaml"),
        help="Arquivo YAML de configuracao.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    configure_logging(
        log_level=config.get("log_level", "INFO"),
        log_file=config.get("log_file", "./logs/monitor.log"),
    )

    monitor = URLMonitor(
        urls=config["urls"],
        max_retries=config.get("max_retries", 3),
        timeout=config.get("timeout", 10),
        output_dir=config.get("output_dir", "./output"),
    )
    report = monitor.run()

    print("Monitoramento concluido.")
    print(f"Total de URLs: {report['summary']['total_urls']}")
    print(f"Sucesso: {report['summary']['successful']}")
    print(f"Falhas: {report['summary']['failed']}")


if __name__ == "__main__":
    main()
