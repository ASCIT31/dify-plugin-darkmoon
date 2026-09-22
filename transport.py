"""
requests-based transport for the Darkmoon Dashboard API client.

Kept in its own module (and out of ``darkmoon_client``) so the client stays
dependency-free and unit-testable without ``requests`` installed. The transport
never raises on a non-2xx status: it returns the real status and parsed body so
the client can surface the API's own ``detail`` rather than a local secret.
"""
from __future__ import annotations

from typing import Any, Dict

import requests

from darkmoon_client import DarkmoonClient, HttpResponse

DEFAULT_TIMEOUT = 60


def requests_transport(opts: Dict[str, Any]) -> HttpResponse:
    method = str(opts.get("method", "GET")).upper()
    url = opts["url"]
    headers = opts.get("headers") or {}
    body = opts.get("body")
    try:
        resp = requests.request(
            method,
            url,
            headers=headers,
            json=body if body is not None else None,
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.exceptions.RequestException as exc:
        # Surface a transport failure as a 0 status with a safe detail. The
        # message is the library's own (no credentials are placed in it).
        return HttpResponse(status_code=0, body={"detail": f"Request to Darkmoon failed: {exc}"})
    try:
        parsed: Any = resp.json()
    except ValueError:
        parsed = resp.text
    return HttpResponse(status_code=resp.status_code, body=parsed)


def logged_in_client(credentials: Dict[str, Any]) -> DarkmoonClient:
    """Build a DarkmoonClient from stored credentials and authenticate it."""
    base_url = str(credentials.get("base_url", "")).strip()
    username = str(credentials.get("username", "")).strip()
    password = str(credentials.get("password", ""))
    client = DarkmoonClient(base_url, requests_transport)
    client.login(username, password)
    return client

