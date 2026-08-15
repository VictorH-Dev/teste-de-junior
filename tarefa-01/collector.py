from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
from requests import RequestException


class UserCollector:
    def __init__(
        self,
        api_url: str,
        city_filters: list[str] | None = None,
        output_dir: str | Path = ".",
        timeout: int = 10,
    ) -> None:
        self.api_url = api_url
        self.city_filters = city_filters or []
        self.output_dir = Path(output_dir)
        self.timeout = timeout

    def fetch_users(self) -> list[dict[str, Any]]:
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except RequestException as error:
            raise RuntimeError(f"Erro ao consultar a API: {error}") from error
        except ValueError as error:
            raise RuntimeError("A resposta da API nao veio em JSON.") from error

        if not isinstance(data, list):
            raise RuntimeError("A API retornou um formato inesperado.")

        return data

    def filter_by_city(self, users: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.city_filters:
            return users

        cities = [city.strip().lower() for city in self.city_filters]
        filtered_users = []

        for user in users:
            user_city = user.get("address", {}).get("city", "").strip().lower()
            if user_city in cities:
                filtered_users.append(user)

        return filtered_users

    def generate_stats(self, users: list[dict[str, Any]]) -> dict[str, Any]:
        companies = []

        for user in users:
            company = user.get("company", {}).get("name")
            if company and company not in companies:
                companies.append(company)

        return {
            "total_users": len(users),
            "companies": sorted(companies),
            "cities_checked": self.city_filters,
            "results_by_city": self.generate_city_summary(users),
        }

    def generate_city_summary(self, users: list[dict[str, Any]]) -> dict[str, Any]:
        summary: dict[str, Any] = {}

        for city in self.city_filters:
            summary[city] = {"total_users": 0, "companies": []}

        for user in users:
            user_city = user.get("address", {}).get("city", "")
            company = user.get("company", {}).get("name")

            for city in self.city_filters:
                if user_city.strip().lower() == city.strip().lower():
                    summary[city]["total_users"] += 1
                    if company:
                        summary[city]["companies"].append(company)

        for city in summary:
            summary[city]["companies"] = sorted(set(summary[city]["companies"]))

        return summary

    def save_results(self, users: list[dict[str, Any]], stats: dict[str, Any]) -> Path:
        """Salva o relatorio em JSON."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"users_{timestamp}.json"

        result = {
            "generated_at": datetime.now(UTC).isoformat(),
            "city_filters": self.city_filters,
            "stats": stats,
            "users": users,
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)

        return output_path


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coleta usuarios por cidade.")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--city", action="append")
    return parser.parse_args()


def get_city_filters(args: argparse.Namespace, config: dict[str, Any]) -> list[str]:
    if args.city:
        return args.city

    if "city_filters" in config:
        return config["city_filters"]

    city = config.get("city_filter")
    if city:
        return [city]

    return []


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    city_filters = get_city_filters(args, config)

    collector = UserCollector(
        api_url=config["api_url"],
        city_filters=city_filters,
        output_dir=config.get("output_dir", "."),
    )

    users = collector.fetch_users()
    filtered_users = collector.filter_by_city(users)
    stats = collector.generate_stats(filtered_users)
    output_path = collector.save_results(filtered_users, stats)

    print(f"Arquivo gerado: {output_path}")
    print(f"Total de usuarios encontrados: {stats['total_users']}")
    print(f"Cidades pesquisadas: {', '.join(city_filters)}")


if __name__ == "__main__":
    main()
