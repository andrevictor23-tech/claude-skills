---
name: repository-wide-documentation-update
description: Workflow command scaffold for repository-wide-documentation-update in claude-skills.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /repository-wide-documentation-update

Use this workflow when working on **repository-wide-documentation-update** in `claude-skills`.

## Goal

Updates or adds top-level documentation files such as README, contributing guidelines, code of conduct, and security policy.

## Common Files

- `README.md`
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/*.yml`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or create documentation files at the repository root (README.md, CLAUDE.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md).
- Optionally add or update issue and pull request templates under .github/.
- Group and cross-link documentation as needed.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.