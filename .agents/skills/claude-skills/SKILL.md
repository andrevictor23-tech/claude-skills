```markdown
# claude-skills Development Patterns

> Auto-generated skill from repository analysis

## Overview
This repository demonstrates best practices for developing modular TypeScript "skills" for Claude Code. It emphasizes clear documentation, consistent coding conventions, and standardized workflows for adding and maintaining both code and documentation. The patterns here are designed to ensure readability, maintainability, and ease of collaboration across contributors.

## Coding Conventions

- **Language:** TypeScript (no framework detected)
- **File Naming:** Use PascalCase for all file names.
  - Example: `SkillHandler.ts`, `UserProfile.ts`
- **Import Style:** Use relative imports.
  - Example:
    ```typescript
    import { UserProfile } from './UserProfile';
    ```
- **Export Style:** Use named exports.
  - Example:
    ```typescript
    export function processSkill(input: string): string { ... }
    export const SKILL_VERSION = '1.0.0';
    ```
- **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/) with prefixes like `docs` and `fix`.
  - Example: `docs: update usage example in README`

## Workflows

### add-or-update-skill-readme
**Trigger:** When creating a new skill or updating documentation for an existing skill  
**Command:** `/add-skill-readme`

1. Create or update `README.md` inside the skill's directory.
2. Follow the standardized template:
    - What the skill does
    - When to use it
    - Prompt examples
    - Deliverables
    - Folder structure
    - Requirements
    - Compliance notes
3. If reorganizing, update the existing `README.md` to match the new pattern.

**Example folder structure:**
```
/MySkill/
  README.md
  MySkill.ts
  MySkill.test.ts
```

**Example README section:**
```markdown
## What it does
Describes the skill's purpose.

## When to use
Scenarios where this skill is applicable.

## Prompt examples
- "Summarize this document."
- "Extract key points from the following text."
```

---

### repository-wide-documentation-update
**Trigger:** When improving or standardizing repository-wide documentation  
**Command:** `/update-docs`

1. Edit or create documentation files at the repository root:
    - `README.md`
    - `CLAUDE.md`
    - `CONTRIBUTING.md`
    - `CODE_OF_CONDUCT.md`
    - `SECURITY.md`
2. Optionally, add or update issue and pull request templates under `.github/`.
3. Group and cross-link documentation as needed to maintain consistency.

**Example:**
- To add a new contributing guideline, create or update `CONTRIBUTING.md` at the root.
- To standardize issue templates, edit files under `.github/ISSUE_TEMPLATE/`.

---

## Testing Patterns

- **Test File Pattern:** Test files are named with the pattern `*.test.*` (e.g., `MySkill.test.ts`).
- **Testing Framework:** Not explicitly detected; use your preferred TypeScript-compatible test runner (e.g., Jest, Mocha).
- **Test Example:**
    ```typescript
    import { processSkill } from './MySkill';

    describe('processSkill', () => {
      it('should process input correctly', () => {
        expect(processSkill('input')).toBe('expected output');
      });
    });
    ```

## Commands

| Command           | Purpose                                                        |
|-------------------|----------------------------------------------------------------|
| /add-skill-readme | Add or update a skill's README following the standard template |
| /update-docs      | Update or add repository-wide documentation files              |
```
