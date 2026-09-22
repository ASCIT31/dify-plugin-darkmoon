# Darkmoon Autonomous Pentest (Dify plugin)

[![Darkmoon](https://img.shields.io/badge/Darkmoon-autonomous%20pentest-4f46e5)](https://github.com/ASCIT31/Dark-Moon)
[![Star Dark-Moon on GitHub](https://img.shields.io/github/stars/ASCIT31/Dark-Moon?style=social)](https://github.com/ASCIT31/Dark-Moon)

A [Dify](https://dify.ai) tool plugin for **[Darkmoon](https://github.com/ASCIT31/Dark-Moon)**, the local, privacy first autonomous AI penetration testing engine. It lets a Dify agent or workflow **trigger a Darkmoon pentest against a target you are authorised to assess, pull back the findings, and review the fix pull requests Darkmoon prepares**, so security testing fits into your Dify apps like any other tool.

> Darkmoon runs and validates security tests. It does not, and this plugin does not, guarantee that a system is secure. Findings can include false positives and must be reviewed by a qualified human. Only run assessments against systems you own or have explicit written authorisation to test. This plugin never merges a pull request; every fix is left for a person to review and merge.

## Tools

| Tool | What it does |
| --- | --- |
| **Run Pentest** | Starts a campaign against a target. With *Wait for completion* on (default), it polls to a terminal event, resolves the campaign, and returns the findings and severity stats. Optional, credential gated remediation (Pro) prepares fix pull requests during the run. |
| **Get Findings** | Returns the vulnerabilities and aggregated stats for a campaign id. |
| **List Campaigns** | Returns the campaigns visible to the authenticated dashboard user. |
| **List Pull Requests** | Returns the fix pull requests Darkmoon prepared (read only), optionally scoped to a campaign and filtered by state. |

## Connection

The plugin talks to the **Darkmoon Dashboard API**, the FastAPI service shipped with Darkmoon (typically on port `8000`). Darkmoon is self hosted, so there is no public endpoint; you point the plugin at your own instance. Darkmoon issues a short lived JWT from `POST /api/v1/auth/login`, so the plugin logs in at run time using the stored credentials.

Configure the provider with:

- **Darkmoon Dashboard API base URL**, for example `http://darkmoon.internal:8000`
- **Dashboard username** and **Dashboard password**, a Darkmoon dashboard user

Credential validation performs a real login, so a wrong URL or bad credentials fail fast.

## Setup

1. Deploy Darkmoon (see the [Darkmoon repository](https://github.com/ASCIT31/Dark-Moon)) and confirm the Dashboard API is reachable from your Dify instance.
2. Install this plugin on your Dify instance (Community Edition or Cloud) from the Marketplace, or as a local plugin package.
3. Add the Darkmoon tool provider and fill in the base URL, username and password.
4. Add a Darkmoon tool to an agent or workflow and run it against an authorised target.

## Remediation and secrets (Pro)

Remediation is optional and is a paid Darkmoon **Pro** feature. The open source Darkmoon focuses on finding, proving and reporting findings locally; the remediation feature that prepares fix pull requests is Pro. When enabled it needs a **credential reference**, an opaque id of a credential stored in Darkmoon's encrypted vault (created in the dashboard), not a raw token. Raw source control secrets never travel through this plugin, and the remediation agent only ever prepares a pull request for human review; it never merges. This plugin can **read** the prepared pull requests through the API regardless of edition.

## Privacy

Darkmoon keeps assessment work on your own infrastructure and applies a privacy gateway so the language model works over placeholders rather than your real hosts, IPs and credentials. This plugin sends data only to the base URL you configure and stores nothing of its own. See [PRIVACY.md](./PRIVACY.md).

## Development

```bash
pip install -r requirements.txt   # runtime deps
python -m pytest -q               # unit tests for the API client (mock transport)
```

The API client (`darkmoon_client.py`) is dependency free and transport injected, so its logic is unit tested without a network. A full end to end run additionally requires a running Darkmoon instance pointed at an authorised target.

## Source

Source repository: https://github.com/ASCIT31/dify-plugin-darkmoon
Darkmoon: https://github.com/ASCIT31/Dark-Moon

## License

MIT, see [LICENSE](./LICENSE). Not affiliated with Dify; "Dify" is a trademark of its respective owner.
