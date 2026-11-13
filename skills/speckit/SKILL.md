---
name: speckit
description: GitHub Spec Kit (Spec-Driven Development / SDD) master orchestrator. Guides the full structured development cycle from constitution, specification, clarification, technical planning, task breakdown, implementation to convergence.
---

# GitHub Spec Kit (Spec-Driven Development - SDD)

Master orchestration skill for GitHub Spec Kit. This skill governs the Spec-Driven Development (SDD) lifecycle to transform vague ideas or requirements into rigorously specified, verified, and implemented software.

## The Spec-Driven Development Lifecycle

```mermaid
flowchart TD
    A["1. Constitution<br/>(/speckit-constitution)"] --> B["2. Feature Specification<br/>(/speckit-specify)"]
    B --> C{"3. Clarify & De-risk<br/>(/speckit-clarify)"}
    C --> D["4. Technical Plan<br/>(/speckit-plan)"]
    D --> E["5. Task Breakdown<br/>(/speckit-tasks)"]
    E --> F{"6. Consistency Analysis<br/>(/speckit-analyze & /speckit-checklist)"}
    F --> G["7. Implementation<br/>(/speckit-implement)"]
    G --> H["8. Verification & Convergence<br/>(/speckit-converge)"]
```

## Available Sub-Skills & Commands

| Stage | Skill / Command | Purpose |
|---|---|---|
| **Constitution** | `/speckit-constitution` | Establish project non-negotiables, architecture rules, and engineering principles (`.specify/memory/constitution.md`). |
| **Specify** | `/speckit-specify <description>` | Convert natural language requirements into structured feature specification (`specs/NNN-<feature>/spec.md`). |
| **Clarify** | `/speckit-clarify` | Identify ambiguities, probe edge cases, and eliminate unstated assumptions before technical planning. |
| **Plan** | `/speckit-plan` | Generate technical architecture, data model, APIs, and implementation strategy (`specs/NNN-<feature>/plan.md`). |
| **Tasks** | `/speckit-tasks` | Generate actionable, dependency-ordered, atomic tasks checklist (`specs/NNN-<feature>/tasks.md`). |
| **Analyze** | `/speckit-analyze` | Audit cross-artifact consistency across spec, plan, tasks, and codebase. |
| **Checklist** | `/speckit-checklist` | Create quality validation checklists for testing and acceptance. |
| **Implement** | `/speckit-implement` | Execute tasks in phased, test-driven order with quality gates. |
| **Converge** | `/speckit-converge` | Audit actual codebase vs spec/plan and append remaining cleanup or remediation tasks. |

## Quickstart / Bootstrap

If the current project workspace does not yet have a `.specify/` folder:
1. Run initialization via PowerShell:
   ```powershell
   specify init --here --force --integration agy --non-interactive --script ps
   ```
2. Or use the bundled templates and scripts located in this skill's directory.

## Best Practices
- Never jump straight into code implementation without an approved specification and task breakdown.
- Keep each task atomic, verifiable, and tied back to a specific requirement in `spec.md`.
- Combine with **EGM (Elephant-Goldfish Model)** (`/egm-review` or `/egm-review-loop`) to conduct independent adversarial review on the drafted spec or architecture plan before implementing.
