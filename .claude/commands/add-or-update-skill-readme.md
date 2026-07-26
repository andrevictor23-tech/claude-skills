---
name: add-or-update-skill-readme
description: Workflow command scaffold for add-or-update-skill-readme in claude-skills.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-or-update-skill-readme

Use this workflow when working on **add-or-update-skill-readme** in `claude-skills`.

## Goal

Adds or updates a README guide for a skill, following a standardized structure with usage, examples, requirements, and compliance notes.

## Common Files

- `*/README.md`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create or update README.md inside the skill's directory.
- Follow the standardized template: what it does, when to use, prompt examples, deliverables, folder structure, requirements, and compliance notes.
- If reorganizing, update existing README.md to match the new pattern.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.