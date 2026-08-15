
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from models import (
    Alert,
    AlertResult,
    ConfidenceLevel,
    Indicator,
    IndicatorType,
    KnownIOC,
    Priority,
    Report,
    ReportSummary,
    Severity,
)


def calculate_risk_score(
    indicators: list[Indicator],
    confidence: ConfidenceLevel,
) -> int:
    score = 0

    for indicator in indicators:
        if indicator.type == IndicatorType.HASH and indicator.severity == Severity.CRITICAL:
            score += 40
        elif indicator.type == IndicatorType.IP and indicator.severity == Severity.SUSPICIOUS:
            score += 30
        elif indicator.type == IndicatorType.DOMAIN and indicator.severity == Severity.CRITICAL:
            score += 20

    if confidence == ConfidenceLevel.HIGH:
        score += 10
    elif confidence == ConfidenceLevel.MEDIUM:
        score += 5

    return score


def classify_priority(score: int) -> Priority:
    if score >= 80:
        return Priority.CRITICAL

    if score >= 50:
        return Priority.HIGH

    if score >= 20:
        return Priority.MEDIUM

    return Priority.LOW


class AlertProcessor:

    def __init__(
        self,
        alerts_path: str | Path = "alerts.json",
        iocs_path: str | Path = "known_iocs.csv",
        json_output_path: str | Path = "output.json",
        csv_output_path: str | Path = "output.csv",
    ) -> None:
        self.alerts_path = Path(alerts_path)
        self.iocs_path = Path(iocs_path)
        self.json_output_path = Path(json_output_path)
        self.csv_output_path = Path(csv_output_path)

    def load_alerts(self) -> list[Alert]:
        with self.alerts_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        raw_alerts = data.get("alerts", [])
        if not isinstance(raw_alerts, list):
            raise RuntimeError("O arquivo alerts.json precisa conter uma lista 'alerts'.")

        return [Alert.model_validate(alert) for alert in raw_alerts]

    def load_known_iocs(self) -> dict[tuple[IndicatorType, str], KnownIOC]:
        known_iocs: dict[tuple[IndicatorType, str], KnownIOC] = {}

        with self.iocs_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                ioc = KnownIOC.model_validate(row)
                key = (ioc.type, ioc.value.lower())
                known_iocs[key] = ioc

        return known_iocs

    def extract_indicators(self, alert: Alert) -> list[Indicator]:
        return [
            Indicator(type=IndicatorType.HASH, value=alert.sha256),
            Indicator(type=IndicatorType.IP, value=alert.source_ip),
            Indicator(type=IndicatorType.DOMAIN, value=alert.domain),
        ]

    def enrich_indicators(
        self,
        indicators: list[Indicator],
        known_iocs: dict[tuple[IndicatorType, str], KnownIOC],
    ) -> list[Indicator]:
        enriched = []

        for indicator in indicators:
            key = (indicator.type, indicator.value.lower())
            known_ioc = known_iocs.get(key)

            if not known_ioc:
                enriched.append(indicator)
                continue

            enriched.append(
                indicator.model_copy(
                    update={
                        "matched": True,
                        "severity": known_ioc.severity,
                        "reason": known_ioc.reason,
                    }
                )
            )

        return enriched

    def process_alert(
        self,
        alert: Alert,
        known_iocs: dict[tuple[IndicatorType, str], KnownIOC],
    ) -> AlertResult:
        indicators = self.extract_indicators(alert)
        enriched_indicators = self.enrich_indicators(indicators, known_iocs)
        risk_score = calculate_risk_score(enriched_indicators, alert.confidence)
        priority = classify_priority(risk_score)

        return AlertResult(
            alert_id=alert.id,
            alert_name=alert.name,
            confidence=alert.confidence,
            indicators=enriched_indicators,
            risk_score=risk_score,
            priority=priority,
        )

    def build_report(self, results: list[AlertResult]) -> Report:
        all_indicators = [
            indicator
            for result in results
            for indicator in result.indicators
        ]
        critical_indicators = len(
            [
                indicator
                for indicator in all_indicators
                if indicator.severity == Severity.CRITICAL
            ]
        )
        clean_indicators = len(
            [
                indicator
                for indicator in all_indicators
                if not indicator.matched
            ]
        )

        return Report(
            summary=ReportSummary(
                total_alerts=len(results),
                critical_indicators=critical_indicators,
                clean_indicators=clean_indicators,
            ),
            alerts=results,
        )

    def export_json(self, report: Report) -> None:
        with self.json_output_path.open("w", encoding="utf-8") as file:
            file.write(report.model_dump_json(indent=2))

    def export_csv(self, report: Report) -> None:
        fieldnames = [
            "alert_id",
            "alert_name",
            "confidence",
            "risk_score",
            "priority",
            "matched_indicators",
            "clean_indicators",
        ]

        with self.csv_output_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for alert in report.alerts:
                matched = len([indicator for indicator in alert.indicators if indicator.matched])
                clean = len([indicator for indicator in alert.indicators if not indicator.matched])

                writer.writerow(
                    {
                        "alert_id": alert.alert_id,
                        "alert_name": alert.alert_name,
                        "confidence": alert.confidence.value,
                        "risk_score": alert.risk_score,
                        "priority": alert.priority.value,
                        "matched_indicators": matched,
                        "clean_indicators": clean,
                    }
                )

    def run(self) -> Report:
        alerts = self.load_alerts()
        known_iocs = self.load_known_iocs()
        results = [self.process_alert(alert, known_iocs) for alert in alerts]
        report = self.build_report(results)

        self.export_json(report)
        self.export_csv(report)

        return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classifica alertas de seguranca.")
    parser.add_argument("--alerts", default="alerts.json", help="Arquivo JSON de alertas.")
    parser.add_argument("--iocs", default="known_iocs.csv", help="Base CSV de IOCs.")
    parser.add_argument("--json-output", default="output.json", help="Relatorio JSON.")
    parser.add_argument("--csv-output", default="output.csv", help="Relatorio CSV.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processor = AlertProcessor(
        alerts_path=args.alerts,
        iocs_path=args.iocs,
        json_output_path=args.json_output,
        csv_output_path=args.csv_output,
    )
    report = processor.run()

    print("Processamento de alertas concluido.")
    print(f"Total de alertas: {report.summary.total_alerts}")
    print(f"Indicadores criticos: {report.summary.critical_indicators}")
    print(f"Indicadores limpos: {report.summary.clean_indicators}")
    print(f"Arquivo JSON: {processor.json_output_path}")
    print(f"Arquivo CSV: {processor.csv_output_path}")


if __name__ == "__main__":
    main()
