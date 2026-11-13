# Oh My Anti (OMA) 🚀

> Unified Spec-Driven Development (Spec Kit) & Adversarial Multi-Agent Review (EGM) Pipeline for Antigravity.

Oh My Anti is an end-to-end engineering suite designed for Google Antigravity and AI coding agents. It orchestrates the full lifecycle of feature development: from natural language requirements, through formal specification, adversarial multi-agent review, technical planning, and task breakdown, to final implementation and verification.

---

## ⚡ Architecture & Pipeline

```mermaid
flowchart TD
    subgraph S1["Stage 1: Specification (Spec Kit)"]
        A1["Project Constitution & Baseline"] --> A2["/speckit-specify<br/>(Generate spec.md)"]
        A2 --> A3["/speckit-clarify<br/>(De-risk assumptions)"]
    end

    subgraph S2["Stage 2: Adversarial Audit (EGM Swarm)"]
        B1["Dispatch Reviewers via invoke_subagent"]
        B1 --> B2["egm-design (Architecture & Failure Modes)"]
        B1 --> B3["egm-zoom-out (Minimalism & Codebase Reuse)"]
        B1 --> B4["egm-codebase-details (Grounding to Live Code)"]
        B2 & B3 & B4 --> B5["egm-synthesizer (Actionable Review Matrix)"]
    end

    subgraph S3["Stage 3: Technical Planning & Tasks"]
        C1["/speckit-plan (Technical Architecture)"]
        C1 --> C2["egm-implementation-readiness (Audit Plan)"]
        C2 --> C3["/speckit-tasks (Atomic Tasks Checklist)"]
        C3 --> C4["/speckit-analyze & /speckit-checklist"]
    end

    subgraph S4["Stage 4: Implementation & Convergence"]
        D1["/speckit-implement (TDD Execution)"]
        D1 --> D2["Test & Lint Verification"]
        D2 --> D3["/speckit-converge (Reconcile Code vs Spec)"]
    end

    S1 --> S2 --> S3 --> S4
```

---

## 📦 What's Included

1. **End-to-End Orchestrator**:
   * `/speckit-egm`: Single autonomous command running the entire 4-stage pipeline from prompt to verified code.
2. **Spec Kit (SDD)**:
   * `/speckit-constitution`: Non-negotiable project architecture principles.
   * `/speckit-specify`: Structured feature specifications.
   * `/speckit-clarify`: Interactive clarification of ambiguous points.
   * `/speckit-plan`: Technical design and API contracts.
   * `/speckit-tasks`: Granular, dependency-ordered tasks.
   * `/speckit-implement`: Phased TDD task implementation.
   * `/speckit-converge`: Verification and codebase reconciliation.
3. **EGM Review Personas**:
   * 10 fresh-context subagent reviewer prompts (`zoom_out`, `design_critic`, `codebase_details`, `synthesizer`, etc.).
   * Document standards for Heilmeier criteria and implementation readiness.
4. **Natural Language Intent Classifier**:
   * Pre-configured `AGENTS.md` rules with bilingual (Vietnamese/English) automatic intent detection.

---

## 🛠️ Quick Installation

### Windows (PowerShell)
```powershell
git clone https://github.com/Royal2005-coder/oh-my-anti.git
cd oh-my-anti
.\install.ps1
```

### macOS / Linux
```bash
git clone https://github.com/Royal2005-coder/oh-my-anti.git
cd oh-my-anti
chmod +x install.sh
./install.sh
```

---

## 📄 License
MIT License. Open-source and free for community use.
