# OpenProspect

**Free, local-first business discovery and prospect research workspace.**

OpenProspect is an open-source application for finding businesses from public map data, recording company and contact information, researching public websites, organising campaigns and preparing AI-assisted outreach drafts. It is designed to work for any industry, business and country where the selected data source has coverage.

> **Status:** usable local prospecting/CRM alpha. It is not yet a full replacement for Sellbird: automated contact enrichment, email verification, mailbox sync, reply handling and outbound delivery are not implemented. Those capabilities are not simulated.

## What works today

| Capability | Current implementation |
| --- | --- |
| Local dashboard | FastAPI dashboard at `http://127.0.0.1:5555` |
| Company register | Add, view, store and export companies in SQLite |
| Business discovery | Free OpenStreetMap / Overpass + Nominatim, 10 km around a geocoded place |
| Website research | Fetches public homepage, extracts title, description, visible text, email and phone strings |
| Contacts | Manually record contacts, role, source URL and email status |
| Campaigns | Create and organise campaign records |
| Product training | `openprospect train <url>` reads the public site and saves an editable local company profile; Train screen available in the dashboard |\n| AI drafts | Ollama locally, Claude Code CLI, Codex CLI, or optional Anthropic / OpenAI-compatible endpoints |
| Outbox | Review, approve or reject drafts; approval never sends |
| Suppression list | Store opt-out addresses and block draft creation for exact suppressed email |
| Exports | Company and contact CSV |
| Activity | Local audit trail for key operations |
| MCP | Optional tools to search saved companies, save companies and call configured AI |

## Zero-budget operation

The default AI provider is **Ollama**, which can run a model locally without API charges. Install Ollama and download a model separately; model downloads require disk space and local compute. The free discovery source is OpenStreetMap. Neither source guarantees complete coverage or current business details.

OpenProspect itself has no subscription fee. Optional cloud AI providers may charge for usage. No paid provider is required for the local CRM, manual data entry, local profiling or exports.

## Windows quick start

Requirements: Windows 10/11, Python 3.11 or newer, Git (or download the ZIP).

```cmd
git clone https://github.com/linkto254-bot/openprospect.git
cd openprospect
run.bat
```

The launcher creates `.venv`, installs the project and opens the dashboard. You can also run manually:

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev,mcp]"
copy .env.example .env
openprospect dashboard
```

The dashboard binds to `127.0.0.1` by default and stores data in `%USERPROFILE%\.openprospect\openprospect.db`. Keep it local; do not expose the development server directly to the public internet. Stop it with `Ctrl+C`.

## AI setup

### Local and free with Ollama

1. Install Ollama from [ollama.com](https://ollama.com).
2. In another CMD window run `ollama pull llama3.2`.
3. In the OpenProspect folder copy `.env.example` to `.env` if you have not already.
4. Keep these values in `.env`:

```env
OPENPROSPECT_AI_PROVIDER=ollama
OPENPROSPECT_AI_MODEL=llama3.2
OPENPROSPECT_AI_BASE_URL=http://localhost:11434/v1
```

### Optional hosted providers

For an OpenAI-compatible provider set `OPENPROSPECT_AI_PROVIDER=openai-compatible`, the model, base URL and API key. For Anthropic set `OPENPROSPECT_AI_PROVIDER=anthropic`, `OPENPROSPECT_AI_MODEL` and `OPENPROSPECT_AI_API_KEY`. Provider usage may incur charges. Keep `.env` private and never commit keys.

## Use in compatible AI chats (MCP)

Install the optional MCP dependency (included by `run.bat`):

```cmd
.venv\Scripts\activate
python -m pip install -e ".[mcp]"
openprospect mcp
```

Configure an MCP-capable desktop/agent client to launch the command in this repository's virtual environment. Example stdio server entry (replace the Windows username and path):

```json
{
  "mcpServers": {
    "openprospect": {
      "command": "C:\\Users\\YOUR_USER\\openprospect\\.venv\\Scripts\\python.exe",
      "args": ["-m", "openprospect.mcp_server"],
      "cwd": "C:\\Users\\YOUR_USER\\openprospect"
    }
  }
}
```

Available MCP tools: `search_companies`, `save_company`, and `ask_configured_ai`. MCP clients must support local stdio MCP servers. A browser-only chat service cannot directly reach a process running on your PC without a separate secure bridge.

## Discovery and data quality

Open the **Discover** tab, enter a city/place and select a category. OpenProspect geocodes the place using Nominatim and searches OpenStreetMap within a 10 km radius using Overpass. Coverage depends on volunteer map data. Search results may be incomplete, outdated or missing websites and contact details. A website being present does not mean the business is a suitable prospect or has consented to marketing.

The **Company** page can fetch the public homepage and show text and possible contact strings. These are leads for human review, not verified facts. The app does not currently crawl entire websites or verify email deliverability.

## Safety and compliance

- No email or social message is sent by OpenProspect.
- Marking a draft approved is a local review state only.
- Publicly visible contact details are not automatically permission to send marketing.
- Check applicable privacy, direct-marketing and anti-spam laws in the sender's and recipient's jurisdictions.
- Record the source of personal data, honour objections and opt-outs, and use the suppression list.
- Do not use the development server on a public network without adding production authentication, HTTPS and security review.
- Do not put real prospect data, passwords or API keys in GitHub issues, commits or logs.

## Commands

```cmd
openprospect dashboard
openprospect status
openprospect companies
openprospect mcp
```

## Tests

```cmd
python -m pip install -e ".[dev,mcp]"
python -m pytest -q
```

GitHub Actions runs tests on Windows and Ubuntu with Python 3.11, 3.12 and 3.13.

## Roadmap / not yet implemented

- Decision-maker discovery and contact enrichment providers
- Email verification adapters and verified/risky/invalid classifications
- Gmail, Microsoft 365 and generic IMAP/SMTP integrations
- Inbox sync, reply classification and conversation management
- Scheduled campaigns, sending windows, rate limits and deliverability monitoring
- Advanced cohort builder, scoring and analytics
- Production authentication, encrypted secrets storage and multi-user deployment

These items are not available yet. Do not configure a live mailbox expecting sending or reply handling.

## License

OpenProspect is licensed under **GNU Affero General Public License v3.0 (AGPL-3.0)**. See [LICENSE](LICENSE). This is an independent project informed by publicly available concepts and documentation; any future code derived from another AGPL project must retain applicable copyright notices and comply with its license.

Upstream project referenced for feature comparison: https://github.com/ethanplusai/sellbird

## Contributing

Issues and pull requests are welcome. Never submit real personal data, API keys or credentials. Please include tests for code changes.
