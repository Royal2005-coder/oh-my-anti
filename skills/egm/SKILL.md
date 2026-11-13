---
name: "egm"
description: "Master Elephant-Goldfish Model (EGM) and Spec Kit orchestrator. Triggers adversarial multi-agent reviews, deep codebase exploration (Elephant), fresh-context subagents (Goldfish), and unified full-cycle SDD engineering (/egm-speckit)."
compatibility: "Antigravity invoke_subagent, specify-cli, EGM personas"
metadata:
  author: "Royal2005-coder"
  version: "2.0.0"
---

# `egm` — Master Elephant-Goldfish Model & Full-Cycle SDD Engine

The `egm` skill is the primary entry point for Google Elephant-Goldfish Model (EGM) reasoning, multi-agent adversarial audits, and unified Spec-Driven Development (Spec Kit).

## Commands & Modes

When called via `/egm [command / task]`:

1. **Full-Cycle End-to-End Orchestration** (Default when a feature/refactor/bug is specified):
   - Automatically executes the 5-phase pipeline:
     * **Phase 0**: Workspace & Constitution setup (`.specify/` & `AGENTS.md`)
     * **Phase 1**: Exploration & Specification (`/egm-brainstorm` -> `/speckit-specify` -> `/speckit-clarify`)
     * **Phase 2**: Adversarial Goldfish Swarm Review (`invoke_subagent` with `egm-zoom-out`, `egm-comprehension`, `egm-design`, `egm-codebase-details` -> `egm-synthesizer` -> `/egm-resolve`)
     * **Phase 3**: Technical Planning & Task Decomposition (`/speckit-plan` -> `egm-implementation-readiness` -> `/speckit-tasks` -> `/speckit-analyze`)
     * **Phase 4**: TDD Implementation & Verification (`/speckit-implement` -> automated testing)
     * **Phase 5**: Convergence & Drift Audit (`/speckit-converge` -> `/egm-drift-report`)

2. **Targeted Sub-Commands**:
   - `/egm review [file/spec]`: Dispatches parallel isolated Goldfish personas (`invoke_subagent`) to audit the target without conversation history bias.
   - `/egm brainstorm [topic]`: Performs deep contextual exploration across the codebase (Elephant Memory) to analyze tradeoffs and formulate architectures.
   - `/egm bootstrap [path]`: Generates structured documentation and bootstraps context for a repository or directory.
   - `/egm drift [spec-path]`: Analyzes divergence between implemented code and original specifications.
