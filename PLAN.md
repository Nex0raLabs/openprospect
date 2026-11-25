# OpenProspect implementation plan

> Independent implementation. Sellbird is used only as a feature reference; no Sellbird code, prompts, or assets are copied. OpenProspect remains AGPL-3.0.

## Initial audit (2026-11-25)

- [x] Read the current README and packaging metadata.
- [x] Read Sellbird's public README and the requested pipeline, approval/sending, and dashboard guides for feature-level comparison only.
- [x] Complete a recursive source-tree and module/test audit before implementation.
- [ ] Record baseline test results and identify existing API, CLI, database, frontend, and security boundaries.

### What exists (confirmed from README and packaging)

- FastAPI local dashboard on loopback, CLI entry point, Python 3.11+ package.
- SQLite-backed company/contact/campaign/outbox/activity workflows.
- Free OpenStreetMap Overpass + Nominatim discovery.
- Basic public homepage research and extraction of visible text, email and phone strings.
- Manual contacts, campaign records, CSV company/contact export.
- Ollama and optional Anthropic/OpenAI-compatible AI drafting.
- Approval/reject state for drafts (approval does not send).
- Exact-email suppression list.
- Optional MCP server with search/save/AI tools.
- pytest and GitHub Actions are described in the README; must verify implementation and coverage.
- Existing README explicitly discloses missing enrichment, verification, mailbox sync, reply handling and outbound delivery.

### Confirmed gaps from the requested target

- Product training workflow and editable product/ICP/offer/voice configuration.
- Provider adapters for Claude Code CLI and Codex CLI; provider connection checks and settings UI.
- Configurable buying signals, full multi-page site profiling, scoring and provenance.
- Decision-maker/contact enrichment, E.164 normalization, email-pattern learning and verification classifications.
- Editable Markdown playbooks, per-contact multi-step sequences, WhatsApp copy and deterministic pre-send lint.
- Real Gmail/Microsoft 365/SMTP sending, approval/autopilot controls, throttling, office hours, warmup, unsubscribe headers/endpoints and suppression enforcement.
- IMAP sync, thread matching, bounce/auto-reply/reply classification and unified conversations.
- WhatsApp sidecar pairing/sending/receiving and optional official Cloud API mode.
- Autonomous run loop, scheduler, activity trail, pause controls and usage accounting.
- Full dashboard navigation, analytics, onboarding, search, saved filters, bulk actions, kanban, PWA and CSV import/export.
- Compliance/DNS checks, Docker, changelog, comprehensive tests and end-to-end CI.

## Delivery checklist

### Foundation and security
- [x] Audit every tracked source, test, docs and workflow file.\n- [ ] Capture baseline test results (not executable through the GitHub repository connector; awaiting CI/local runner).
- [ ] Keep secrets, database files, mailbox credentials and WhatsApp sessions out of Git; harden .gitignore.
- [ ] Add encrypted local secret/session storage and private token dashboard authentication.
- [ ] Preserve loopback-only binding, host validation and CSRF/origin protections.
- [ ] Add migration-safe SQLAlchemy/SQLite data model and backup/export path.
- [ ] Keep all optional integrations explicitly Not connected until credentials and live checks succeed.

### 1. Training
- [ ] `openprospect train <url>` fetches a site and extracts product, buyers, pricing, proof, voice and objections.
- [ ] Persist editable local training configuration.
- [ ] Train screen edits ICP, offer, banned phrases, signature, language and CTA.
- [ ] Pluggable Ollama, Claude Code CLI, Codex CLI and user-supplied OpenAI-compatible providers.
- [ ] Settings provider selection and real Test connection action.

### 2. Discovery
- [ ] Free Overpass/Nominatim discovery by category and city, including Nairobi, Mombasa and Kisumu.
- [ ] CSV import and manual company creation.
- [ ] Dedupe by normalized domain and phone.
- [ ] Store source URL, company identity, category, address, website, phone, published email and socials.
- [ ] robots.txt compliance, bounded concurrency, caching and per-host rate limits.

### 3. Signals and profiling
- [ ] Fetch homepage, contact and about pages without LLM calls.
- [ ] Detect no website, stale site, mobile issues, missing booking/ordering, SSL, performance, WhatsApp and hiring signals.
- [ ] User-editable signal definitions and evidence.
- [ ] Explainable company score with observation history and confidence.

### 4. Enrichment
- [ ] Extract public decision makers and contacts only from company-owned pages/public listings.
- [ ] Extract email, phone, WhatsApp, tel links, schema.org and contact forms.
- [ ] Normalize Kenyan numbers to E.164 with tests.

### 5. Email verification
- [ ] Syntax, disposable domain, MX and role-account checks.
- [ ] Catch-all detection and optional bounded SMTP RCPT probe where network policy permits.
- [ ] Honest verified/risky/guess/invalid labels.
- [ ] Learn domain email patterns and label generated addresses as guesses.
- [ ] Sending gate accepts deliverable addresses only.

### 6. Writing
- [ ] Generate personalized email sequences from evidence and trained product context.
- [ ] Editable Markdown templates and playbooks/skills folder.
- [ ] Deterministic lint rejects merge tags, banned phrases, overlong copy, excess links and unverified recipients.
- [ ] Generate concise WhatsApp variants.

### 7. Email sending
- [ ] Real Gmail OAuth/app-password, Microsoft 365 and generic SMTP adapters.
- [ ] Approval-first Outbox; explicit Autopilot opt-in.
- [ ] Per-mailbox daily limits, warmup ramp, recipient-local office hours and jitter.
- [ ] Global pause/kill switch.
- [ ] Mandatory sender footer, List-Unsubscribe and List-Unsubscribe-Post headers, unsubscribe endpoint.
- [ ] Persistent suppression list enforced in all channels and stages.
- [ ] Track sent, bounced, replied and unsubscribed outcomes.

### 8. Mailbox sync and replies
- [ ] IMAP sync per mailbox and thread matching.
- [ ] Detect bounce, auto-reply and out-of-office.
- [ ] Classify interested, objection, question, not now, wrong person and stop.
- [ ] Immediately suppress opt-outs and stop sequences on replies.
- [ ] Draft non-opt-out responses into approval Outbox.

### 9. WhatsApp
- [ ] Node/Baileys sidecar with phone-number pairing code (no QR-only workflow).
- [ ] Encrypted persistent session and live connection status.
- [ ] Text send/receive, delivery/read state and unified inbox integration.
- [ ] Official WhatsApp Cloud API mode with template support and honest connection state.
- [ ] Only business-published contact numbers eligible for outreach.
- [ ] Per-message approval by default; low daily cap and gradual ramp.
- [ ] Random 45–180 second delay, variation checks, mandatory STOP line and instant STOP suppression.
- [ ] Failure-spike circuit breaker and visible unofficial-client ban warning.

### 10. Conversations
- [ ] Unified email/WhatsApp inbox grouped by contact.
- [ ] AI reply drafts, notes and deal statuses.
- [ ] Needs-you queue and sequence stop/resume controls.

### 11. Autonomous loop
- [ ] `openprospect run` and dashboard Start/Pause.
- [ ] Budget-aware/throttled stage selection across discovery, profile, enrich, verify, write, send, sync and replies.
- [ ] Every operation recorded in Activity with outcome and provenance.

### 12. Dashboard
- [ ] Today, Your company/Train, Outbox, Inboxes, Conversations, Signals, Discover, Companies, Contacts, Campaigns, Activity, Usage, Controls, Settings and Help.
- [ ] Consistent responsive design, light/dark mode, transitions, loading/empty states.
- [ ] Keyboard shortcuts, Ctrl/Cmd-K command palette and global search.
- [ ] Saved filters, bulk actions and drag/drop pipeline kanban.
- [ ] Funnel, daily sends, reply/bounce rates, campaign performance and deliverability charts.
- [ ] First-run onboarding with live checks.
- [ ] Installable PWA and phone-friendly layout.
- [ ] CSV import/export for all supported records.

### 13. Compliance and deliverability
- [ ] Kenya Data Protection Act 2019/ODPC lawful-basis and opt-out checklist.
- [ ] Real DNS SPF/DKIM/DMARC lookups with pass/fail evidence.
- [ ] Warmup and responsible sending guidance.

### 14. Quality and release
- [ ] Tests for every pipeline stage and security-sensitive behavior.
- [ ] CI workflow on supported Python versions and platforms.
- [ ] Docker option.
- [ ] Clean README with honest 5-minute quick start and accurate capability status.
- [ ] CHANGELOG maintained.
- [ ] Small logical commits on this feature branch; phase PRs only after real tests pass.
- [ ] Real SMTP test to a user-controlled mailbox and real WhatsApp pairing/test only after user supplies credentials and completes pairing.
- [ ] Do not claim end-to-end completion until each applicable item is implemented and tested.


## Audit notes

The recursive tree currently contains only the README, license, packaging/launcher files, one CI workflow, eight Python package modules, and one test module. There is no frontend build system, migrations folder, Docker configuration, changelog, playbook directory, or docs folder in OpenProspect's current tree.

Key implementation risks found during source review:
- Dashboard routes currently have no private-token authentication or CSRF/origin protection.
- Website profiling currently fetches only the homepage and does not enforce robots.txt or robustly constrain redirects/private-network destinations.
- Discovery uses Nominatim and Overpass directly with no explicit pacing/cache/retry policy and dedupes only by name/location at the route layer.
- AI providers are environment-variable based; there is no connection test UI or CLI provider adapter.
- Existing "approved" drafts are only local state and are not sent; README correctly discloses this.
- The database is direct SQLite with ad-hoc table creation, not SQLAlchemy migrations.
- Existing tests cover basic database/dashboard/API/suppression behavior only. No test execution environment is exposed by the GitHub file connector; CI must supply the executable verification.
