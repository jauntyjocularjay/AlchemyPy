# LLM-Generated: thin HTTP client for the Alchemy import workflow.

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from ..errors.http import APIError, AuthenticationError, BadRequestError, NotFoundError, RateLimitError


@dataclass
class AlchemyHTTPClient:
    base_url: str = "https://example.com"
    api_key: str | None = None
    auth: str | None = None
    timeout: float = 30.0
    max_retries: int = 3
    retries: int | None = None
    session: Any | None = None
    headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self.base_url = self.base_url.rstrip("/")
        if self.retries is not None:
            self.max_retries = self.retries
        if self.auth is not None:
            self.api_key = self.auth
        if self.api_key:
            self.headers.setdefault("Authorization", f"Bearer {self.api_key}")
        self.headers.setdefault("Content-Type", "application/json")
        self.headers.setdefault("Accept", "application/json")

    @property
    def auth_headers(self) -> dict[str, str]:
        return dict(self.headers)

    def build_url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"

    def request(self, method: str, path: str, payload: Any | None = None, *, headers: dict[str, str] | None = None) -> Any:
        request_headers = dict(self.headers)
        if headers:
            request_headers.update(headers)

        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        url = self.build_url(path)
        req = urllib_request.Request(url, data=data, headers=request_headers, method=method.upper())

        for attempt in range(max(1, self.max_retries)):
            try:
                with urllib_request.urlopen(req, timeout=self.timeout) as response:
                    body = response.read().decode("utf-8")
                    if not body:
                        return {}
                    return json.loads(body)
            except urllib_error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code == 401:
                    raise AuthenticationError(f"Authentication failed for {url}") from exc
                if exc.code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(0.5 * (attempt + 1))
                        continue
                    raise RateLimitError(f"Rate limited by API while calling {url}", exc.code, body) from exc
                if exc.code == 404:
                    raise NotFoundError(f"Resource not found at {url}", exc.code, body) from exc
                if exc.code in {400, 422}:
                    raise BadRequestError(f"Bad request to {url}", exc.code, body) from exc
                raise APIError(f"API request failed for {url}", exc.code, body) from exc
            except urllib_error.URLError as exc:
                if attempt < self.max_retries - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise APIError(f"Request to {url} failed: {exc.reason}") from exc

        raise APIError(f"Request to {url} did not complete successfully")

    def get(self, path: str, *, headers: dict[str, str] | None = None) -> Any:
        return self.request("GET", path, headers=headers)

    def post_json(self, path: str, payload: Any, *, headers: dict[str, str] | None = None) -> Any:
        return self.request("POST", path, payload=payload, headers=headers)
