
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LEGITIMATE_KEYWORDS = {
    "google",
    "cloudflare",
}

SUSPICIOUS_KEYWORDS = {
    "tor",
    "scanner",
    "hosting",
    "datacenter",
    "linode",
    "akamai",
}

SUSPICIOUS_IPS = {
    "185.220.101.45",
    "45.33.32.156",
}


def classify_ip(record: dict[str, Any]) -> str:
    ip = str(record.get("ip", ""))
    isp = str(record.get("isp") or "").lower()
    organization = str(record.get("organization") or "").lower()
    asn = str(record.get("asn") or "").lower()
    text = " ".join([isp, organization, asn])

    if ip in SUSPICIOUS_IPS:
        return "Potencialmente suspeito"

    if any(keyword in text for keyword in LEGITIMATE_KEYWORDS):
        return "Conhecido legítimo"

    if any(keyword in text for keyword in SUSPICIOUS_KEYWORDS):
        return "Potencialmente suspeito"

    return "Desconhecido"


class IPReportProcessor:

    def __init__(
        self,
        input_path: str | Path = "./output/enriched_ips.json",
        output_path: str | Path = "./output/final_report.json",
    ) -> None:
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def load_data(self) -> list[dict[str, Any]]:
        with self.input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        results = data.get("results", [])
        if not isinstance(results, list):
            raise RuntimeError("Arquivo de entrada precisa conter a lista 'results'.")

        return results

    def build_report(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        enriched_records = []

        for record in records:
            classification = classify_ip(record)
            enriched_records.append({**record, "classification": classification})

        summary = {
            "total_ips": len(enriched_records),
            "legitimate": len(
                [
                    item
                    for item in enriched_records
                    if item["classification"] == "Conhecido legítimo"
                ]
            ),
            "suspicious": len(
                [
                    item
                    for item in enriched_records
                    if item["classification"] == "Potencialmente suspeito"
                ]
            ),
            "unknown": len(
                [
                    item
                    for item in enriched_records
                    if item["classification"] == "Desconhecido"
                ]
            ),
        }

        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "summary": summary,
            "results": enriched_records,
        }

    def save_report(self, report: dict[str, Any]) -> Path:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2)

        return self.output_path

    def run(self) -> Path:
        records = self.load_data()
        report = self.build_report(records)
        return self.save_report(report)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Processa IPs enriquecidos.")
    parser.add_argument("--input", default="./output/enriched_ips.json")
    parser.add_argument("--output", default="./output/final_report.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processor = IPReportProcessor(input_path=args.input, output_path=args.output)
    output_path = processor.run()
    print(f"Relatório final gerado: {output_path}")


if __name__ == "__main__":
    main()
