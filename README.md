# OpenProspect

**Free, local-first business discovery and prospect research workspace.**

OpenProspect is an open-source application for finding businesses from public map data, recording company and contact information, researching public websites, organising campaigns and preparing AI-assisted outreach drafts. It is designed to work for any industry, business and country where the selected data source has coverage.

> **Status:** local-first prospecting and outreach alpha. SMTP/IMAP, an optional WhatsApp Web sidecar, unified inbox storage, a profile-only automation loop and DNS checks are implemented in this branch. Live provider accounts, mailbox credentials, a paired WhatsApp device and production end-to-end tests are still required. This is not yet a turnkey or fully autonomous Sellbird replacement.

## What works today

| Capability | Current implementation |
| --- | --- |
| Local dashboard | FastAPI dashboard at `http://127.0.0.1:5555` |
| Company register | Add, view, store and export companies in SQLite |
| Business discovery | Free OpenStreetMap / Overpass + Nominatim, 10 km around a geocoded place |
| Website research | Reads the public homepage and up to two relevant same-site pages (robots.txt-aware), extracts public contact strings and records evidence-backed buying signals |
| Contacts | Manually record contacts, role, source URL and email status |
| Campaigns | Create and organise campaign records |
| Product training | `openprospect train <url>` reads the public site and saves an editable local company profile; Train screen available in the dashboard |
| Buying signals | Configurable deterministic checks for HTTPS, mobile viewport, schema, WhatsApp, booking/ordering, contact pages, stale copyright, load time and hiring pages |
| AI drafts | Ollama locally, Claude Code CLI, Codex CLI, or optional Anthropic / OpenAI-compatible endpoints |
| Outbox | Review, approve, reject and explicitly send approved email drafts after SMTP + verified-recipient checks |
| Suppression list | Store opt-out addresses and block draft creation for exact suppressed email |
| Imports / exports | Company and contact CSV import and export |
| Company deduplication | Normalized website domain and Kenyan phone formats |
| Email | SMTP STARTTLS delivery, verified-recipient gate, suppression check, unsubscribe headers and configurable daily cap |\n| Mailbox sync | IMAP SSL sync for unread messages; detects opt-out phrases and adds suppressions |\n| Conversations | Shared local inbox records for inbound email and WhatsApp events |\n| WhatsApp | Optional Node/Baileys sidecar with pairing-code request, explicit text send and inbound webhook |\n| Automation | Start/pause/run loop for public website profiling and buying-signal capture; never sends automatically |\n| Compliance | SPF, DMARC and MX DNS lookup plus a practical privacy checklist; DKIM requires a provider selector |\n| Activity | Local audit trail for key operations |
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

The dashboard binds to `127.0.0.1` by default, prints a private token link, and stores data in `%USERPROFILE%\.openprospect\`. Keep the link private and do not expose the development server directly to the public internet. Stop it with `Ctrl+C`.

## Train OpenProspect on your product

Run `openprospect train https://your-company.com` to read the homepage and up to two relevant same-site pages, subject to `robots.txt`. It saves `company-training.json` under your local OpenProspect data folder. Open the dashboard **Train** screen to edit the ICP, offer, banned phrases, sender signature, language and default CTA. Extraction is heuristic and must be reviewed; it does not invent missing pricing or proof.

## Buying signals

Open **Signals** to edit built-in signal weights or add custom keyword rules. Profile a company to store evidence-linked observations and an explainable 0–100 opportunity score. Signals are heuristic indicators, not verified claims; review the linked page before using them in outreach.

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

### Subscription CLI providers

Choose **Claude Code CLI** or **Codex CLI** in Settings to use a CLI you have already installed and signed in to. These options do not require an API key. Use **Test connection** to run a real provider check. Missing CLIs are shown as **Not connected**.

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

The **Company** page can fetch the public homepage and up to two relevant same-site pages, subject to robots.txt. It records configurable buying signals with evidence URLs and confidence. Public email and phone strings remain unverified; no email deliverability verification is implemented yet.

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
openprospect train https://your-company.com
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


## Email sending and inbox sync

Email is optional and remains disconnected until configured. Add these variables to your private `.env` file:

```env
OPENPROSPECT_SMTP_HOST=smtp.example.com
OPENPROSPECT_SMTP_PORT=587
OPENPROSPECT_SMTP_USER=your-mailbox
OPENPROSPECT_SMTP_PASSWORD=your-app-password
OPENPROSPECT_FROM_EMAIL=you@example.com
OPENPROSPECT_DAILY_SEND_LIMIT=25
OPENPROSPECT_PUBLIC_BASE_URL=https://your-public-host
OPENPROSPECT_IMAP_HOST=imap.example.com
OPENPROSPECT_IMAP_PORT=993
OPENPROSPECT_IMAP_USER=your-mailbox
OPENPROSPECT_IMAP_PASSWORD=your-app-password
```

Restart OpenProspect, verify the recipient in Contacts, create and review a draft, approve it, then use **Send approved email now**. Delivery is refused unless SMTP is configured, the address is marked verified by the app, it is not suppressed, and a public HTTPS unsubscribe base URL is set. The daily cap defaults to 25 and can be lowered or raised up to 100. Use a dedicated mailbox and follow your provider's sending limits. IMAP sync is manual from Inbox and imports unread messages. Test with a mailbox you control before real outreach.

The current unsubscribe handler records the address in the local suppression list. For a deployment behind a reverse proxy, expose the HTTPS unsubscribe route securely; the dashboard itself is designed for loopback-only use and must not be exposed directly.

## WhatsApp sidecar (optional, unofficial)

The sidecar is separate from the Python app and uses the Baileys WhatsApp Web protocol. WhatsApp may restrict unofficial clients; the official Cloud API is the recommended production integration and is not implemented here.

```cmd
cd whatsapp-sidecar
copy .env.example .env
npm install
```

Set `WA_SIDECAR_TOKEN` to the same long random secret in the sidecar environment and the Python app's `.env`. Set `OPENPROSPECT_INBOUND_URL=http://127.0.0.1:5555/api/whatsapp/inbound` in the sidecar environment. Start the Python dashboard, then start the sidecar with `npm start`. Open **WhatsApp**, request a pairing code using your number in international format without a plus sign, and enter the code in WhatsApp → Linked devices → Link a device → Link with phone number. Send messages only to business-published numbers where you have an appropriate lawful basis and follow WhatsApp policies. Pairing and delivery must be tested on a device you control.

## Autonomous controls

The Controls page can start, pause or manually run a local background cycle. The current loop only profiles saved public websites and stores buying signals. It does not discover endlessly, generate campaigns, or send email/WhatsApp automatically. Human approval remains required for outbound communication.

## DNS and privacy readiness

Open **Compliance** to check SPF, DMARC and MX records for a domain. DKIM cannot be conclusively checked without knowing the sending provider's selector. The privacy checklist is operational guidance, not legal advice or a certification of compliance. Review the Kenya Data Protection Act, ODPC guidance, applicable direct-marketing rules and provider terms before using personal data for outreach.

## Known limitations

- No live SMTP/IMAP mailbox or WhatsApp device has been connected and verified in this development session.
- IMAP currently imports unread plain-text message content and groups records by sender; complex MIME, provider-specific threading, attachments and full reply classification are not complete.
- The Baileys bridge is an optional unofficial integration. Official WhatsApp Cloud API templates, webhook verification and message-status callbacks are not implemented.
- The automation loop only profiles existing companies; discovery, enrichment, writing, sending and reply handling are not chained into a fully autonomous pipeline.
- SPF/DMARC/MX lookups are DNS presence checks, not deliverability guarantees. DKIM selector discovery and alignment analysis remain future work.
- No production deployment, public HTTPS unsubscribe test, end-to-end mailbox test or WhatsApp pairing test has been performed.
