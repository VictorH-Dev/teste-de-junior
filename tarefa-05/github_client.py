
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from auth_client import AuthenticatedClient, AuthenticationError


class GitHubClient(AuthenticatedClient):

    def get_user(self, username: str) -> dict[str, Any]:
        return self.get(f"/users/{username}")

    def list_repos(self, username: str, sort: str = "updated") -> list[dict[str, Any]]:
        return self.get(
            f"/users/{username}/repos",
            params={"sort": sort, "per_page": 100},
        )

    def get_rate_limit(self) -> dict[str, Any]:
        return self.get("/rate_limit")


def load_simple_yaml(path: str | Path) -> dict[str, Any]:
    config: dict[str, Any] = {}

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue

            key, value = clean_line.split(":", maxsplit=1)
            parsed_value: Any = value.strip()
            if parsed_value.isdigit():
                parsed_value = int(parsed_value)

            config[key.strip()] = parsed_value

    return config


def build_output(
    user: dict[str, Any],
    repos: list[dict[str, Any]],
    rate_limit: dict[str, Any],
) -> dict[str, Any]:
    return {
        "user": {
            "login": user.get("login"),
            "name": user.get("name"),
            "public_repos": user.get("public_repos"),
            "profile_url": user.get("html_url"),
        },
        "repositories": [
            {
                "name": repo.get("name"),
                "language": repo.get("language"),
                "updated_at": repo.get("updated_at"),
                "url": repo.get("html_url"),
            }
            for repo in repos[:5]
        ],
        "rate_limit": {
            "limit": rate_limit.get("rate", {}).get("limit"),
            "remaining": rate_limit.get("rate", {}).get("remaining"),
            "reset": rate_limit.get("rate", {}).get("reset"),
        },
    }


def demo_output() -> dict[str, Any]:
    return {
        "user": {
            "login": "octocat",
            "name": "The Octocat",
            "public_repos": 8,
            "profile_url": "https://github.com/octocat",
        },
        "repositories": [
            {
                "name": "Hello-World",
                "language": None,
                "updated_at": "2026-01-01T00:00:00Z",
                "url": "https://github.com/octocat/Hello-World",
            }
        ],
        "rate_limit": {
            "limit": 5000,
            "remaining": 4999,
            "reset": 1760000000,
        },
        "demo_mode": True,
    }


def save_output(output: dict[str, Any], output_path: str | Path = "output.json") -> None:
    with Path(output_path).open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cliente autenticado da GitHub API.")
    parser.add_argument("--config", default="config.yaml", help="Arquivo de configuracao.")
    parser.add_argument("--username", help="Usuario do GitHub para consulta.")
    parser.add_argument("--demo", action="store_true", help="Gera uma saida de exemplo sem token.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_simple_yaml(args.config)
    username = args.username or config.get("demo_username", "octocat")

    if args.demo:
        output = demo_output()
        save_output(output)
        print("Arquivo output.json gerado em modo demonstracao.")
        return

    try:
        client = GitHubClient(
            base_url=config.get("base_url", "https://api.github.com"),
            token_env_var=config.get("token_env_var", "API_TOKEN"),
            token_file=config.get("token_file", "~/.config/token.txt"),
            cache_ttl_seconds=int(config.get("cache_ttl_seconds", 300)),
        )
        user = client.get_user(username)
        repos = client.list_repos(username)
        rate_limit = client.get_rate_limit()
    except AuthenticationError as exc:
        print(exc)
        print("Dica: use modo demo com: python github_client.py --demo")
        return

    output = build_output(user, repos, rate_limit)
    save_output(output)

    print(f"Usuario: {output['user']['login']}")
    print(f"Repositorios listados: {len(output['repositories'])}")
    print(
        "Rate limit restante: "
        f"{output['rate_limit']['remaining']}/{output['rate_limit']['limit']}"
    )
    print("Arquivo output.json gerado.")


if __name__ == "__main__":
    main()
