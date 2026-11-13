---
name: "egm-speckit"
description: "Master Autonomous Engineering Harness uniting Google Research Harness² (Recursive Agent Harnessing), GitHub Spec Kit (Spec-Driven Development), and Google Elephant-Goldfish Model (Adversarial Multi-Agent Review). End-to-end 5-phase engineering pipeline from inception, adversarial swarm audit, DAG task scheduling, recursive Propose-Probe-Compose TDD execution, to drift audit and experience reflection."
compatibility: "Antigravity invoke_subagent, specify-cli, Harness2 Task Ledger, EGM personas"
metadata:
  author: "Royal2005-coder"
  version: "3.0.0"
  reference: "Google Research Harness² (arXiv:2610.14224)"
---

# `egm-speckit` Master Orchestrator: Full-Cycle Autonomous Harness

`egm-speckit` is an **enterprise-grade autonomous engineering harness** combining three breakthrough systems:
1. **Google Research Harness²**: The 8-component architecture (Prompt, Guardrails, Memory, Tools, Subagents, Skills, Scripts, Plugins), task-level recursion (**Propose – Probe – Compose**), and persistent experience reflection.
2. **GitHub Spec Kit (SDD)**: Rigorous specification, ambiguity clarification, technical architecture planning, and verifiable convergence.
3. **Google Elephant-Goldfish Model (EGM)**: Deep repository memory (Elephant) combined with unbiased adversarial review by fresh-context, isolated subagents (Goldfish Swarm).
4. **Oh-My-Pi (OMP) Parity**: Real-time interactive Task Ledger DAG tracking, phase grouping, and visual progress monitoring.

When triggered via `/egm-speckit <task>` or `/egm <task>`, the agent executes the complete 5-phase pipeline autonomously.

---

## 🔁 Complete Autonomous Architecture

```mermaid
flowchart TD
    subgraph P0["Phase 0: Harness & Invariant Setup (Harness² C1-C8)"]
        A0["Verify / Bootstrap .specify/<br/>(specify init --here --force)"] --> A1["Run Preflight Audit<br/>(python scripts/harness_runner.py preflight)"]
        A1 --> A2["Load Constitution & Invariants<br/>(.specify/memory/constitution.md + AGENTS.md)"]
    end

    subgraph P1["Phase 1: Exploration & Specification (Elephant Context)"]
        B1["Deep Codebase Exploration<br/>(/egm-brainstorm)"] --> B2["Formal Feature Specification<br/>(/speckit-specify -> specs/NNN/spec.md)"]
        B2 --> B3["Ambiguity & Edge-Case Probing<br/>(/speckit-clarify)"]
    end

    subgraph P2["Phase 2: Goldfish Swarm Adversarial Audit (Fresh Context)"]
        C0["Spawn Isolated Reviewers in Parallel<br/>(invoke_subagent)"]
        C0 --> C1["egm-zoom-out (Minimalism & Existing Code Reuse)"]
        C0 --> C2["egm-comprehension (Clarity, Zero Blind Assumptions)"]
        C0 --> C3["egm-design (Hostile Critic: Failure Modes & Security)"]
        C0 --> C4["egm-codebase-details (Live Schema, DTO & Type Match)"]
        C1 & C2 & C3 & C4 --> C5["egm-synthesizer (Consolidated Review Matrix: P0/P1/P2)"]
        C5 --> C6["Architectural Trade-Off Resolution<br/>(/egm-resolve)"]
    end

    subgraph P3["Phase 3: Technical Planning & DAG Task Scheduling (OMP Standard)"]
        D1["Generate Technical Plan<br/>(/speckit-plan -> specs/NNN/plan.md)"] --> D2["Gate Check: Implementation Readiness<br/>(egm-implementation-readiness)"]
        D2 --> D3["Generate Atomic DAG Tasks with Roles & Verification Gates<br/>(/speckit-tasks -> specs/NNN/tasks.md)"]
        D3 --> D4["Compile Live Task Ledger<br/>(python scripts/task_ledger.py specs/NNN/tasks.md --json)"]
    end

    subgraph P4["Phase 4: Harness² Recursive Execution (Propose - Probe - Compose)"]
        E1["Select Next Ready Task in DAG"] --> E2["Propose: Generate Candidate Implementation"]
        E2 --> E3["Probe: Run Isolated Checks & Automated Tests"]
        E3 --> E4["Compose: Synthesize Validated Solution & Verify Gate"]
        E4 --> E5["Update Task Ledger: [✓] DONE<br/>(python scripts/task_ledger.py --update TID DONE)"]
        E5 -->|More tasks| E1
    end

    subgraph P5["Phase 5: Convergence, Drift Audit & Experience Reflection"]
        F1["Spec Convergence Verification<br/>(/speckit-converge)"] --> F2["Spec Drift Report<br/>(/egm-drift-report)"]
        F2 --> F3["Harness² Experience Reflection<br/>(python scripts/harness_runner.py reflect TID Lesson)"]
        F3 --> F4["Final Deliverable Sign-Off"]
    end

    P0 --> P1 --> P2 --> P3 --> P4 --> P5
```

---

## 📋 Step-by-Step Execution Protocol

### Phase 0: Harness & Invariant Setup
1. **Preflight Audit**:
   - Run `python scripts/harness_runner.py preflight` to ensure all 8 harness components (Prompt, Guardrails, Memory, Tools, Subagents, Skills, Scripts, Plugins) are active.
2. **Infrastructure**:
   - Verify `.specify/` exists. If missing, initialize:
     ```powershell
     specify init --here --force --integration agy --non-interactive --script ps
     ```
3. **Constitution & Invariants**:
   - Extract non-negotiable architectural rules from `AGENTS.md` and `.specify/memory/constitution.md`.

### Phase 1: Exploration & Specification
1. **Elephant Brainstorming (`/egm-brainstorm`)**:
   - Explore repository context, dependencies, and previous lessons learned. Formulate concrete architectures.
2. **Draft Baseline Specification (`/speckit-specify`)**:
   - Generate `specs/NNN-<feature>/spec.md` with User Stories, inputs/outputs, non-functional requirements, and acceptance criteria.
3. **Clarify Ambiguities (`/speckit-clarify`)**:
   - Probe edge cases: network timeout, null state, authorization boundary, race conditions.

### Phase 2: Goldfish Swarm Adversarial Audit
> [!IMPORTANT]
> Goldfish subagents **MUST** execute in fresh, isolated contexts using `invoke_subagent`. They audit the drafted `spec.md` without conversation bias.
1. Dispatch parallel personas: `egm-zoom-out`, `egm-comprehension`, `egm-design`, `egm-codebase-details`.
2. Compile Review Matrix via `egm-synthesizer` and resolve critical findings via `/egm-resolve`.

### Phase 3: Technical Planning & DAG Task Scheduling
1. **Technical Architecture Plan (`/speckit-plan`)**:
   - Create `specs/NNN-<feature>/plan.md` defining models, services, DTOs, state flow, and error handling.
2. **Implementation Readiness Gate (`egm-implementation-readiness`)**:
   - Ensure zero architectural ambiguity is left for the implementer.
3. **DAG Task Breakdown (`/speckit-tasks`)**:
   - Generate `specs/NNN-<feature>/tasks.md` in **OMP-Format**:
     - `[ID]` e.g. `[T01]`
     - `[Role: subagent-frontend | backend | architect]`
     - `[Depends on: T01]`
     - `[Verify: npm run test ...]`
4. **Initialize Task Ledger**:
   - Run `python scripts/task_ledger.py specs/NNN/tasks.md --json .specify/memory/tasks_ledger.json` to enable live statusline tracking.

### Phase 4: Harness² Recursive Execution (Propose – Probe – Compose)
For each atomic task in the DAG:
1. Mark task `IN_PROGRESS` in Task Ledger.
2. **Propose**: Generate candidate implementation diff.
3. **Probe**: Run automated tests, typechecks, or subagent review.
4. **Compose & Verify**: Integrate verified code and execute the task's verification gate.
5. Mark task `DONE` in Task Ledger (`python scripts/task_ledger.py --update TID DONE`).

### Phase 5: Convergence, Drift Audit & Experience Reflection
1. **Spec Convergence (`/speckit-converge`)**: Verify all requirements are satisfied in code.
2. **Spec Drift Audit (`/egm-drift-report`)**: Verify zero unintended deviation occurred.
3. **Harness² Experience Reflector**:
   - Run `python scripts/harness_runner.py reflect <TID> "<lesson>"` to persist insights in `.specify/memory/lessons.md`.
4. Present final report with test results, links, and git commit details.
