from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from darkmoon_client import DarkmoonError
from transport import logged_in_client


class GetFindingsTool(Tool):
    """Return the vulnerabilities and aggregated stats for a Darkmoon campaign."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        campaign_id = str(tool_parameters.get("campaign_id", "")).strip()
        if not campaign_id:
            raise Exception("A campaign id is required.")
        try:
            client = logged_in_client(self.runtime.credentials)
            findings = client.get_findings(campaign_id)
        except DarkmoonError as exc:
            raise Exception(str(exc))
        yield self.create_json_message(
            {
                "campaign_id": campaign_id,
                "total": findings["total"],
                "stats": findings["stats"],
                "findings": findings["data"],
            }
        )
        yield self.create_text_message(
            f"Campaign {campaign_id} has {findings['total']} finding(s). "
            "Findings can include false positives and must be reviewed by a qualified human."
        )
