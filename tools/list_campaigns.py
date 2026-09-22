from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from darkmoon_client import DarkmoonError
from transport import logged_in_client


class ListCampaignsTool(Tool):
    """Return the campaigns visible to the authenticated dashboard user."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            client = logged_in_client(self.runtime.credentials)
            campaigns = client.list_campaigns()
        except DarkmoonError as exc:
            raise Exception(str(exc))
        yield self.create_json_message({"total": len(campaigns), "campaigns": campaigns})
        yield self.create_text_message(f"Found {len(campaigns)} Darkmoon campaign(s).")
