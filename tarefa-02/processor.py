
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


class MetricsProcessor:


    CPU_LIMIT = 80
    MEMORY_LIMIT = 90

    def __init__(
        self,
        input_path: str | Path = "input.json",
        json_output_path: str | Path = "output.json",
        csv_output_path: str | Path = "output.csv",
    ) -> None:
        self.input_path = Path(input_path)
        self.json_output_path = Path(json_output_path)
        self.csv_output_path = Path(csv_output_path)

    def load_data(self) -> list[dict[str, Any]]:


        try:
            with self.input_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise RuntimeError(f"Arquivo nao encontrado: {self.input_path}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("O arquivo de entrada nao contem um JSON valido.") from exc

        servers = data.get("servers")
        if not isinstance(servers, list):
            raise RuntimeError("O JSON precisa conter uma lista chamada 'servers'.")

        return servers

    def parse_metrics(self, raw_metrics: str) -> dict[str, int]:


        metrics: dict[str, int] = {}

        for item in raw_metrics.split("|"):
            try:
                key, value = item.split(":", maxsplit=1)
                metrics[key.strip()] = int(value)
            except ValueError as exc:
                raise RuntimeError(f"Metrica em formato invalido: {item}") from exc

        required_keys = {"cpu", "mem", "disk"}
        missing_keys = required_keys - metrics.keys()
        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            raise RuntimeError(f"Metricas obrigatorias ausentes: {missing}")

        return metrics

    def identify_issues(self, metrics: dict[str, int]) -> list[str]:


        issues = []

        if metrics["cpu"] > self.CPU_LIMIT:
            issues.append("CPU acima de 80%")

        if metrics["mem"] > self.MEMORY_LIMIT:
            issues.append("Memoria acima de 90%")

        return issues

    def process_servers(
        self,
        servers: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

      

        processed_servers = []

        for server in servers:
            metrics = self.parse_metrics(server["metrics"])
            issues = self.identify_issues(metrics)

            processed_servers.append(
                {
                    "id": server["id"],
                    "name": server["name"],
                    "timestamp": server["timestamp"],
                    "metrics": {
                        "cpu": metrics["cpu"],
                        "memory": metrics["mem"],
                        "disk": metrics["disk"],
                    },
                    "has_problem": bool(issues),
                    "issues": issues,
                }
            )

        return processed_servers

    def calculate_averages(
        self,
        processed_servers: list[dict[str, Any]],
    ) -> dict[str, float]:
        
        if not processed_servers:
            return {"cpu": 0.0, "memory": 0.0, "disk": 0.0}

        total = len(processed_servers)
        cpu_average = sum(item["metrics"]["cpu"] for item in processed_servers) / total
        memory_average = sum(item["metrics"]["memory"] for item in processed_servers) / total
        disk_average = sum(item["metrics"]["disk"] for item in processed_servers) / total

        return {
            "cpu": round(cpu_average, 2),
            "memory": round(memory_average, 2),
            "disk": round(disk_average, 2),
        }

    def build_report(
        self,
        processed_servers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        
        problem_servers = [
            server for server in processed_servers if server["has_problem"]
        ]

        return {
            "summary": {
                "total_servers": len(processed_servers),
                "servers_with_problems": len(problem_servers),
                "averages": self.calculate_averages(processed_servers),
            },
            "servers": processed_servers,
        }

    def export_json(self, report: dict[str, Any]) -> None:
       
        with self.json_output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2)

    def export_csv(self, processed_servers: list[dict[str, Any]]) -> None:
        
        fieldnames = [
            "id",
            "name",
            "timestamp",
            "cpu",
            "memory",
            "disk",
            "has_problem",
            "issues",
        ]

        with self.csv_output_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for server in processed_servers:
                writer.writerow(
                    {
                        "id": server["id"],
                        "name": server["name"],
                        "timestamp": server["timestamp"],
                        "cpu": server["metrics"]["cpu"],
                        "memory": server["metrics"]["memory"],
                        "disk": server["metrics"]["disk"],
                        "has_problem": server["has_problem"],
                        "issues": "; ".join(server["issues"]),
                    }
                )

    def run(self) -> dict[str, Any]:
       
        servers = self.load_data()
        processed_servers = self.process_servers(servers)
        report = self.build_report(processed_servers)

        self.export_json(report)
        self.export_csv(processed_servers)

        return report


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Processa metricas de servidores.")
    parser.add_argument("--input", default="input.json", help="Arquivo JSON de entrada.")
    parser.add_argument("--json-output", default="output.json", help="Saida em JSON.")
    parser.add_argument("--csv-output", default="output.csv", help="Saida em CSV.")
    return parser.parse_args()


def main() -> None:
  
    args = parse_args()
    processor = MetricsProcessor(
        input_path=args.input,
        json_output_path=args.json_output,
        csv_output_path=args.csv_output,
    )
    report = processor.run()

    print("Processamento concluido.")
    print(f"Total de servidores: {report['summary']['total_servers']}")
    print(f"Servidores com problemas: {report['summary']['servers_with_problems']}")
    print(f"Arquivo JSON: {processor.json_output_path}")
    print(f"Arquivo CSV: {processor.csv_output_path}")


if __name__ == "__main__":
    main()
