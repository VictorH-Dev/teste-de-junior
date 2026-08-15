
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
import yaml
from requests import RequestException


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(log_level: str, logs_dir: str | Path) -> None:
    logs_path = Path(logs_dir)
    logs_path.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, log_level.upper(), logging.INFO)
    formatter = JsonFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logs_path / "pipeline.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[console_handler, file_handler], force=True)


def load_config(config_path: str | Path) -> dict[str, Any]:
    with Path(config_path).open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise RuntimeError("O config.yaml precisa conter um objeto YAML.")

    return config


class IPCollector:

    API_URL = "http://ip-api.com/json/{ip}"
    FIELDS = "status,message,query,country,regionName,city,lat,lon,isp,org,as"

    def __init__(
        self,
        ips: list[str],
        output_dir: str | Path = "./output",
        max_retries: int = 3,
        timeout: int = 10,
    ) -> None:
        self.ips = ips
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def enrich_ip(self, ip: str) -> dict[str, Any]:
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Consultando IP {ip}, tentativa {attempt}")
                response = requests.get(
                    self.API_URL.format(ip=ip),
                    params={"fields": self.FIELDS},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()

                if data.get("status") != "success":
                    message = data.get("message", "erro desconhecido")
                    raise RuntimeError(f"Falha ao consultar {ip}: {message}")

                return {
                    "ip": data.get("query"),
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "isp": data.get("isp"),
                    "organization": data.get("org"),
                    "asn": data.get("as"),
                    "status": "enriched",
                    "error": None,
                }

            except (RequestException, RuntimeError, ValueError) as exc:
                last_error = str(exc)
                self.logger.warning(f"Falha ao consultar {ip}: {last_error}")

                if attempt < self.max_retries:
                    time.sleep(2 ** (attempt - 1))

        return {
            "ip": ip,
            "country": None,
            "region": None,
            "city": None,
            "latitude": None,
            "longitude": None,
            "isp": None,
            "organization": None,
            "asn": None,
            "status": "error",
            "error": last_error,
        }

    def run(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        results = [self.enrich_ip(ip) for ip in self.ips]

        payload = {
            "generated_at": datetime.now(UTC).isoformat(),
            "source": "ip-api.com",
            "results": results,
        }

        output_path = self.output_dir / "enriched_ips.json"
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coleta enriquecimento de IPs.")
    parser.add_argument("--config", default="config.yaml", help="Arquivo YAML.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    configure_logging(config.get("log_level", "INFO"), config.get("logs_dir", "./logs"))

    collector = IPCollector(
        ips=config["ips"],
        output_dir=config.get("output_dir", "./output"),
        max_retries=config.get("max_retries", 3),
        timeout=config.get("timeout", 10),
    )
    output_path = collector.run()
    print(f"Coleta concluída: {output_path}")


if __name__ == "__main__":
    main()
