from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from darkmoon_client import DarkmoonClient, DarkmoonError
from transport import logged_in_client


class ListPullRequestsTool(Tool):
    """Return the fix pull requests Darkmoon prepared (read-only).

    Pull requests are prepared by the paid Pro remediation feature and are left
    for a human to review and merge. This tool only reads them; it never merges.
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        campaign_id = str(tool_parameters.get("campaign_id", "")).strip() or None
        state = str(tool_parameters.get("state", "")).strip()
        try:
            client = logged_in_client(self.runtime.credentials)
            prs = client.list_pull_requests(campaign_id)
        except DarkmoonError as exc:
            raise Exception(str(exc))
        if state:
            prs = DarkmoonClient.filter_pull_requests(prs, state=[state])
        yield self.create_json_message({"total": len(prs), "pull_requests": prs})
        yield self.create_text_message(
            f"Found {len(prs)} fix pull request(s). These are prepared for human review and are "
            "never merged automatically."
        )
