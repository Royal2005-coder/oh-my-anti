---
name: "speckit-egm"
description: "Unified Spec-Driven Development (Spec Kit) and Adversarial Multi-Agent Review (EGM) Pipeline. End-to-end autonomous pipeline from specification, multi-agent adversarial audit, technical planning, task breakdown, to implementation and convergence."
compatibility: "Requires specify-cli, Antigravity invoke_subagent, and EGM reviewer subagents"
metadata:
  author: "github-spec-kit & google-egm"
  version: "1.2.0"
---

# Unified Spec Kit + EGM Engineering Pipeline (End-to-End Orchestrator)

Execute a complete end-to-end engineering cycle combining **GitHub Spec Kit** (for rigorous specification, planning, and task tracking) and **Google Elephant-Goldfish Model (EGM)** (for independent adversarial multi-agent review via isolated subagents).

When invoked, the agent autonomously drives the feature or architectural change through all 4 stages to final convergence without skipping quality gates.

```mermaid
flowchart TD
    subgraph S1["Stage 1: Specification (Spec Kit)"]
        A1["Check / Init .specify/<br/>(specify init --here --force)"] --> A2["/speckit-specify<br/>(Create spec.md)"]
        A2 --> A3["/speckit-clarify<br/>(Resolve edge cases)"]
    end

    subgraph S2["Stage 2: EGM Adversarial Audit (Fresh Context Subagents)"]
        B1["Dispatch Reviewers in Parallel<br/>(invoke_subagent)"]
        B1 --> B2["egm-design (Critic)"]
        B1 --> B3["egm-zoom-out (Architect)"]
        B1 --> B4["egm-codebase-details (Auditor)"]
        B2 & B3 & B4 --> B5["egm-synthesizer<br/>(Consolidate Review Matrix)"]
    end

    subgraph S3["Stage 3: Technical Planning & Task Breakdown"]
        C1["/speckit-plan<br/>(Incorporate EGM feedback into plan.md)"] --> C2["Validate Readiness<br/>(egm-implementation-readiness)"]
        C2 --> C3["/speckit-tasks<br/>(Generate atomic tasks.md)"]
        C3 --> C4["/speckit-analyze & /speckit-checklist<br/>(Cross-artifact consistency check)"]
    end

    subgraph S4["Stage 4: Implementation & Convergence"]
        D1["/speckit-implement<br/>(Execute tasks with TDD)"] --> D2["Verification<br/>(Typecheck, lint, unit tests)"]
        D2 --> D3["/speckit-converge<br/>(Reconcile code vs spec & close)"]
    end

    S1 --> S2 --> S3 --> S4
```

---

## Autonomous Execution Protocol

### Step 0: Environment & Workspace Check
1. Check if `.specify/` exists in the project root.
   - If not, automatically run:
     ```powershell
     specify init --here --force --integration agy --non-interactive --script ps
     ```
2. Read project principles from `.specify/memory/constitution.md` and repository conventions from `AGENTS.md`.

---

### Step 1: Specification (Spec Kit)
1. Invoke `/speckit-specify` using the user's natural language requirements.
2. Formulate the short name, target feature directory (e.g. `specs/NNN-<feature>/`), and write initial `spec.md`.
3. If ambiguities, assumptions, or missing requirements exist, run `/speckit-clarify` to resolve them before proceeding.
4. Record resolved requirements into `spec.md`.

---

### Step 2: Adversarial Multi-Agent Audit (EGM Swarm)
Before drafting the implementation plan or touching code, launch the isolated EGM reviewer subagents using `invoke_subagent` (ensuring each runs in a fresh, un-biased context):

1. **`egm-design`**:
   - Prompt: Review the specification at `specs/NNN-<feature>/spec.md` against existing architecture, failure modes, scalability limits, and security vulnerabilities.
2. **`egm-zoom-out`**:
   - Prompt: Scrutinize the design for over-engineering (YAGNI), excessive abstractions, and identify opportunities for reusing existing codebase modules and libraries.
3. **`egm-codebase-details`**:
   - Prompt: Verify exact file paths, schemas, interfaces, DTOs, and database contracts against live codebase implementation.
4. **`egm-synthesizer`**:
   - Compile findings into a consolidated **Review Matrix**:
     * **Blockers (P0)**: Architectural defects that must be resolved prior to planning.
     * **Majors (P1)**: Edge cases and failure recovery paths to integrate into `plan.md`.
     * **Minors (P2)**: Code quality and naming polish items.

---

### Step 3: Technical Planning & Task Breakdown
1. Incorporate all P0/P1 items from the EGM synthesis into `/speckit-plan`.
2. Generate `specs/NNN-<feature>/plan.md` covering architecture, contracts, dependencies, and test strategies.
3. Validate plan readiness using `egm-implementation-readiness` (confirm zero ambiguity remains for the implementer).
4. Run `/speckit-tasks` to generate atomic, dependency-ordered tasks in `specs/NNN-<feature>/tasks.md`.
5. Run `/speckit-analyze` and `/speckit-checklist` to guarantee 100% traceability between requirements in `spec.md` and tasks in `tasks.md`.

---

### Step 4: Implementation & Convergence
1. Run `/speckit-implement`:
   - Execute tasks in phase order.
   - Adhere strictly to project coding standards (strict types, JSDoc, MVVM/Signals, no `any`, zero regression).
2. Run automated validation:
   - Run type checking, linting, and automated unit tests.
3. Run `/speckit-converge`:
   - Reconcile codebase state against `spec.md` and `plan.md`.
   - Ensure all acceptance criteria are met and no orphaned tasks remain.
   - Summarize the completed delivery for the user.
