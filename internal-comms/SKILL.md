---
name: internal-comms
description: A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).
license: Complete terms in LICENSE.txt
---

## When to Use This Skill

Use this skill whenever asked to write internal company communications, including:
- 3P updates (Progress, Plans, Problems)
- Company newsletters
- FAQ responses
- Status reports
- Leadership updates
- Project updates
- Incident reports

## Supported Formats

Each format has a dedicated guideline file in `examples/` with detailed instructions on structure, tone, and what tools/sources to pull from:

| Format | Guideline file | Use for |
|--------|----------------|---------|
| 3P update | `examples/3p-updates.md` | Weekly Progress/Plans/Problems team updates for leadership; succinct (30-60 sec read) |
| Company newsletter | `examples/company-newsletter.md` | Company-wide weekly/monthly recap (~20-25 bullets) sent via Slack/email |
| FAQ answers | `examples/faq-answers.md` | Summarizing and answering recurring company-wide questions |
| General comms | `examples/general-comms.md` | Anything that doesn't fit the above (status reports, incident reports, project updates, leadership updates, ad hoc announcements) |

## How to Use This Skill

1. **Identify the communication type** from the request. If it's ambiguous or doesn't clearly match a supported format, ask for clarification before proceeding.
2. **Load the matching guideline file** from the table above and follow its specific instructions for formatting, tone, and content gathering.
3. **Pull from available tools** when the guideline file mentions them (e.g., Slack, email, calendar, shared documents) — each file lists which sources are most useful for that format.
4. **Draft the communication** following the loaded guideline's structure and tone requirements.

If the communication type doesn't match any existing guideline, use `examples/general-comms.md` as the default and ask the user for the missing context (audience, purpose, tone, formatting requirements).

## Keywords
3P updates, company newsletter, company comms, weekly update, faqs, common questions, status report, incident report, leadership update, project update, internal comms
