from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from darkmoon_client import DarkmoonClient, DarkmoonError
from transport import requests_transport


class DarkmoonProvider(ToolProvider):
    """Validate the connection to a self-hosted Darkmoon Dashboard API.

    Validation performs a real login against ``POST /api/v1/auth/login`` so a
    wrong base URL or bad credentials fail fast. Only the API's own error detail
    is surfaced - the password and JWT are never placed in an error message.
    """

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        base_url = str(credentials.get("base_url", "")).strip()
        username = str(credentials.get("username", "")).strip()
        password = str(credentials.get("password", ""))

        if not base_url:
            raise ToolProviderCredentialValidationError(
                "Darkmoon base URL is required (e.g. http://darkmoon.internal:8000)."
            )
        if not username or not password:
            raise ToolProviderCredentialValidationError(
                "A Darkmoon dashboard username and password are required."
            )

        client = DarkmoonClient(base_url, requests_transport)
        try:
            client.login(username, password)
        except DarkmoonError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
