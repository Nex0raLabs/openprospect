# OpenProspect

**Free, open-source business discovery and outreach software.**

OpenProspect is a community-oriented alternative to commercial prospecting platforms. It is designed to help businesses of any size discover relevant companies, research their public websites, organise prospects, prepare personalised outreach and manage replies — with human approval kept in control.

> Project status: early development. This repository is not yet a feature-complete Sellbird replacement.

## Goals

- Work for any business, industry or country through configurable ideal-customer profiles.
- Local-first by default, with SQLite as the zero-cost starting database.
- Free discovery options where available, with provider costs clearly disclosed before use.
- Website profiling and transparent prospect-fit signals.
- Company, contact and campaign management.
- Draft personalised outreach; require explicit human approval before sending.
- Email inbox integration and reply tracking through supported providers.
- No mandatory paid AI provider, data provider, email verifier or hosted service.
- Clear setup, privacy, compliance and self-hosting documentation.

## Zero-budget principles

OpenProspect software is free and open source. Optional third-party services may impose their own limits, fees, terms or API requirements. The project will not describe a paid service as free, silently incur usage charges, or send messages without an explicit approval workflow.

The initial development target is a local installation using open-source dependencies and SQLite. Users remain responsible for complying with applicable privacy, marketing, anti-spam and email-provider rules in their jurisdiction.

## Planned modules

| Module | Purpose |
| --- | --- |
| Today | Pipeline overview and tasks requiring attention |
| Company profile | Business identity, offer, industries and target geography |
| Discovery | Find businesses through pluggable data sources |
| Companies | Company register and website presence |
| Contacts | Contact records and source tracking |
| Signals | Review and configure prospect-fit signals |
| Campaigns | Build and organise outreach campaigns |
| Drafts / Outbox | Review, edit and approve messages |
| Inboxes | Connect supported mailboxes and track replies |
| Activity | Auditable history of important actions |
| Settings | Providers, privacy, sending limits and compliance controls |

## Development principles

1. **Approval first:** no automatic outbound messages by default.
2. **Transparent costs:** show provider requirements and estimated costs before a provider is used.
3. **Privacy by design:** collect only necessary business/contact data, record sources, and support suppression and deletion.
4. **Portable:** local database and documented export formats.
5. **Extensible:** provider adapters rather than hard-coded vendor dependencies.
6. **Honest status:** features marked planned are not represented as implemented.

## License and attribution

OpenProspect is distributed under the GNU Affero General Public License v3.0 (AGPL-3.0). This project is being developed as an independent, community-maintained alternative and is informed by the public Sellbird project. Where code is copied or modified from Sellbird, its copyright notices and AGPL-3.0 obligations must be preserved. See [LICENSE](LICENSE).

- Upstream reference: https://github.com/ethanplusai/sellbird
- License: AGPL-3.0

## Contributing

Issues and pull requests are welcome. Please do not submit credentials, private customer data, scraped personal data, or API keys. Security issues should be reported privately to the repository maintainers.

## Roadmap

- [ ] Minimal local dashboard and setup flow
- [ ] SQLite data model and company register
- [ ] Free/local business discovery adapters
- [ ] Website profiling and evidence-backed signals
- [ ] Contact research and email verification adapters
- [ ] Draft generation with human approval
- [ ] Mailbox integrations and reply tracking
- [ ] Campaign analytics, exports and documentation
