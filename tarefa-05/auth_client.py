from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from requests import Response


class APIClientError(RuntimeError):
    pass


class AuthenticationError(APIClientError):
    pass


class RateLimitError(APIClientError):
    pass


class AuthenticatedClient:
    def __init__(
        self,
        base_url: str,
        token_env_var: str = "API_TOKEN",
        token_file: str | Path = "~/.config/token.txt",
        cache_ttl_seconds: int = 300,
        timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.token_env_var = token_env_var
        self.token_file = Path(token_file).expanduser()
        self.cache_ttl_seconds = cache_ttl_seconds
        self.timeout = timeout
        self.cache: dict[str, tuple[float, Any]] = {}
        self.session = requests.Session()

        token = self.load_token()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "teste-tecnico-github-client",
            }
        )

    def load_token(self) -> str:
        env_token = os.getenv(self.token_env_var)
        if env_token:
            return env_token.strip()

        if self.token_file.exists():
            token = self.token_file.read_text(encoding="utf-8").strip()
            if token:
                return token

        raise AuthenticationError(
            "Token nao encontrado. Configure API_TOKEN ou ~/.config/token.txt."
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = self.build_url(path)
        cache_key = self.build_cache_key("GET", url, params)
        cached = self.get_from_cache(cache_key)

        if cached is not None:
            return cached

        response = self.session.get(url, params=params, timeout=self.timeout)
        data = self.handle_response(response)
        self.save_to_cache(cache_key, data)
        return data

    def post(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = self.build_url(path)
        response = self.session.post(url, json=payload or {}, timeout=self.timeout)
        return self.handle_response(response)

    def build_url(self, path: str) -> str:
        return urljoin(self.base_url, path.lstrip("/"))

    def build_cache_key(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None,
    ) -> str:
        params_text = json.dumps(params or {}, sort_keys=True)
        return f"{method}:{url}:{params_text}"

    def get_from_cache(self, cache_key: str) -> Any | None:
        cached = self.cache.get(cache_key)
        if not cached:
            return None

        created_at, data = cached
        is_valid = time.time() - created_at <= self.cache_ttl_seconds

        if is_valid:
            return data

        del self.cache[cache_key]
        return None

    def save_to_cache(self, cache_key: str, data: Any) -> None:
        self.cache[cache_key] = (time.time(), data)

    def handle_response(self, response: Response) -> Any:
        if response.status_code == 401:
            raise AuthenticationError("Token invalido ou ausente.")

        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                reset = response.headers.get("X-RateLimit-Reset", "desconhecido")
                raise RateLimitError(f"Rate limit excedido. Reset em: {reset}")

            raise APIClientError(f"Acesso negado: {response.text}")

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            message = f"Erro HTTP {response.status_code}: {response.text}"
            raise APIClientError(message) from error

        if response.content:
            return response.json()

        return None
