---
name: "egm-speckit"
description: "Full-Cycle Unified Engineering Pipeline: Combines EGM Context & Adversarial Review with Spec Kit SDD. Manually triggered via /egm-speckit to run end-to-end: specification -> Goldfish swarm audit -> technical planning -> atomic tasks -> TDD implementation -> convergence."
compatibility: "Antigravity invoke_subagent, specify-cli, and EGM subagents"
metadata:
  author: "Royal2005-coder"
  version: "1.3.0"
---

# EGM + Spec Kit Full-Cycle Unified Pipeline (`/egm-speckit`)

This skill provides a manual trigger (`/egm-speckit`) for complex feature development or major architectural refactors. It executes a complete, rigorous, closed-loop pipeline combining **Elephant-Goldfish Model (EGM)** and **GitHub Spec Kit (SDD)**.

When triggered, the agent autonomously drives the task through all 4 stages to completion without skipping validation gates.

```mermaid
flowchart TD
    subgraph S1["Stage 1: Specification (Elephant + Spec Kit)"]
        A1["Check/Bootstrap .specify/<br/>(specify init --here --force)"] --> A2["/speckit-specify<br/>(Write spec.md)"]
        A2 --> A3["/speckit-clarify<br/>(Clarify edge cases & invariants)"]
    end

    subgraph S2["Stage 2: Adversarial Goldfish Swarm (EGM Subagents)"]
        B1["Dispatch Reviewers in Parallel<br/>(invoke_subagent)"]
        B1 --> B2["egm-design (Critic: Failure modes & security)"]
        B1 --> B3["egm-zoom-out (Architect: YAGNI & code reuse)"]
        B1 --> B4["egm-codebase-details (Auditor: Live schemas & DTOs)"]
        B2 & B3 & B4 --> B5["egm-synthesizer<br/>(Consolidated Review Matrix: P0/P1/P2)"]
    end

    subgraph S3["Stage 3: Technical Planning & Task Decomposition"]
        C1["/speckit-plan<br/>(Incorporate EGM Review Matrix into plan.md)"] --> C2["Validate Readiness<br/>(egm-implementation-readiness)"]
        C2 --> C3["/speckit-tasks<br/>(Generate atomic tasks.md)"]
        C3 --> C4["/speckit-analyze & /speckit-checklist<br/>(Cross-artifact consistency audit)"]
    end

    subgraph S4["Stage 4: Implementation & Convergence"]
        D1["/speckit-implement<br/>(Phase-ordered TDD execution)"] --> D2["Verification<br/>(Typecheck, lint, automated tests)"]
        D2 --> D3["/speckit-converge<br/>(Reconcile codebase vs spec & finalize)"]
    end

    S1 --> S2 --> S3 --> S4
```

---

## Autonomous Execution Guide

### Trigger
```text
/egm-speckit <feature description or architectural requirement>
```

### Phase 1: Specification & Clarification
1. Verify if `.specify/` exists in project root. If missing, initialize via:
   ```powershell
   specify init --here --force --integration agy --non-interactive --script ps
   ```
2. Read project constitution from `.specify/memory/constitution.md` and repository conventions from `AGENTS.md`.
3. Create the feature directory (e.g. `specs/NNN-<feature>/`) and write the baseline `spec.md` with user stories, acceptance criteria, and constraints.
4. Run clarification on any ambiguous requirements, edge cases, or unspoken assumptions using `/speckit-clarify`.

### Phase 2: Goldfish Swarm Audit (Isolated Context Subagents)
Spawn fresh-context subagents via `invoke_subagent` to independently critique the specification:
* **`egm-design`**: Analyzes failure scenarios, boundary conditions, performance bottlenecks, and security attack surfaces.
* **`egm-zoom-out`**: Challenges over-engineering, enforces YAGNI, and maps reusable components already in the codebase.
* **`egm-codebase-details`**: Verifies exact file paths, exported types, API models, and database contracts against actual code.
* **`egm-synthesizer`**: Compiles findings into an actionable Review Matrix (P0 Blockers, P1 Majors, P2 Minors).

### Phase 3: Technical Planning & Tasks Breakdown
1. Incorporate all P0/P1 findings into `/speckit-plan` and produce `specs/NNN-<feature>/plan.md`.
2. Audit plan feasibility using `egm-implementation-readiness` (ensuring no design ambiguity is left to implementers).
3. Generate granular, atomic tasks in `specs/NNN-<feature>/tasks.md` via `/speckit-tasks`.
4. Audit cross-artifact traceability using `/speckit-analyze` and generate acceptance criteria using `/speckit-checklist`.

### Phase 4: Implementation & Convergence
1. Execute tasks in sequence using `/speckit-implement` following TDD and strict repository coding standards.
2. Run project verification suite (typecheck, lint, automated tests).
3. Execute `/speckit-converge` to verify that all requirements from `spec.md` are completely met by the implementation, closing all checklist items.
