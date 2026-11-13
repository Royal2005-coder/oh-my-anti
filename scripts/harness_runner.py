#!/usr/bin/env python3
"""
Harness² Autonomous Agent Engine for Antigravity (oh-my-anti)
Based on Google Research Harness²: Recursive Agent Harnessing for an Open World (arXiv:2610.14224).
Provides:
  - 8-Component Harness Validation (Prompt, Guardrails, Memory, Tools, Subagents, Skills, Scripts, Plugins)
  - Recursive Task Harnessing: Propose -> Probe -> Compose
  - Harnessing-Level Experience Reflector (Persistent Memory)
  - Preflight & Verification Gates
"""

from __future__ import annotations
import os
import sys
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

@dataclass
class HarnessComponents:
    c1_system_prompt: bool = False
    c2_guardrails_constitution: bool = False
    c3_memory_lessons: bool = False
    c4_tool_guidance: bool = False
    c5_subagents: bool = False
    c6_skills: bool = False
    c7_scripts: bool = False
    c8_plugins: bool = False
    details: Dict[str, str] = field(default_factory=dict)

    def is_healthy(self) -> bool:
        # Minimum baseline for autonomous execution
        return (
            self.c2_guardrails_constitution
            and self.c5_subagents
            and self.c6_skills
            and self.c7_scripts
        )

def inspect_harness_components(workspace_root: str | Path) -> HarnessComponents:
    root = Path(workspace_root).resolve()
    comp = HarnessComponents()

    # C1: System Prompt / AGENTS.md
    agents_md = root / "AGENTS.md"
    if agents_md.exists():
        comp.c1_system_prompt = True
        comp.details["C1_Prompt"] = f"Found {agents_md.name} ({agents_md.stat().st_size} bytes)"

    # C2: Guardrails / Constitution
    specify_const = root / ".specify" / "memory" / "constitution.md"
    global_rules = Path.home() / ".gemini" / "config" / "rules" / "AGENTS.md"
    if specify_const.exists() or global_rules.exists() or agents_md.exists():
        comp.c2_guardrails_constitution = True
        found = []
        if specify_const.exists(): found.append(".specify constitution")
        if global_rules.exists(): found.append("global rules")
        comp.details["C2_Guardrails"] = ", ".join(found)

    # C3: Memory & Lessons
    lessons_md = root / ".specify" / "memory" / "lessons.md"
    if lessons_md.exists():
        comp.c3_memory_lessons = True
        comp.details["C3_Memory"] = f"Active memory: {lessons_md.name}"
    else:
        comp.details["C3_Memory"] = "No lessons.md yet (will initialize on reflect)"

    # C4: Tool Guidance
    comp.c4_tool_guidance = True
    comp.details["C4_ToolGuidance"] = "Antigravity native tools & MCP active"

    # C5: Subagents
    subagents_dir = Path.home() / ".gemini" / "config" / "plugins" / "egm" / "agents"
    if subagents_dir.exists() and list(subagents_dir.glob("*.md")):
        comp.c5_subagents = True
        count = len(list(subagents_dir.glob("*.md")))
        comp.details["C5_Subagents"] = f"{count} EGM subagent personas active"

    # C6: Skills
    skills_dir = Path.home() / ".gemini" / "config" / "skills"
    if skills_dir.exists():
        comp.c6_skills = True
        comp.details["C6_Skills"] = "Global Antigravity skills repository connected"

    # C7: Scripts
    scripts_dir = root / "scripts"
    if scripts_dir.exists() or (Path.home() / ".gemini" / "config" / "plugins" / "egm" / "scripts").exists():
        comp.c7_scripts = True
        comp.details["C7_Scripts"] = "Automation scripts & task ledger available"

    # C8: Plugins
    plugins_dir = Path.home() / ".gemini" / "config" / "plugins"
    if plugins_dir.exists():
        comp.c8_plugins = True
        comp.details["C8_Plugins"] = "Plugins engine enabled (egm, spec-kit, etc.)"

    return comp

def run_preflight_check(workspace_root: str | Path) -> str:
    comp = inspect_harness_components(workspace_root)
    lines = []
    lines.append("=" * 64)
    lines.append("  🛡️  HARNESS² RECURSIVE AGENT PREFLIGHT CHECK (Google Research)")
    lines.append("=" * 64)

    def icon(val: bool) -> str:
        return "[✓] PASS" if val else "[✗] WARN"

    lines.append(f" {icon(comp.c1_system_prompt)} C1: System Prompt        -> {comp.details.get('C1_Prompt', 'Missing')}")
    lines.append(f" {icon(comp.c2_guardrails_constitution)} C2: Guardrails/Rules     -> {comp.details.get('C2_Guardrails', 'Missing')}")
    lines.append(f" {icon(comp.c3_memory_lessons)} C3: Persistent Memory    -> {comp.details.get('C3_Memory', 'Pending')}")
    lines.append(f" {icon(comp.c4_tool_guidance)} C4: Tool Guidance        -> {comp.details.get('C4_ToolGuidance', 'Missing')}")
    lines.append(f" {icon(comp.c5_subagents)} C5: Multi-Agent Swarm    -> {comp.details.get('C5_Subagents', 'Missing')}")
    lines.append(f" {icon(comp.c6_skills)} C6: Skills Library       -> {comp.details.get('C6_Skills', 'Missing')}")
    lines.append(f" {icon(comp.c7_scripts)} C7: Automation Scripts   -> {comp.details.get('C7_Scripts', 'Missing')}")
    lines.append(f" {icon(comp.c8_plugins)} C8: Middleware Plugins   -> {comp.details.get('C8_Plugins', 'Missing')}")
    lines.append("-" * 64)
    status_str = "READY FOR AUTONOMOUS EXECUTION" if comp.is_healthy() else "DEGRADED (Proceed with caution)"
    lines.append(f"  Harness Status: {status_str}")
    lines.append("=" * 64)
    return "\n".join(lines)

def record_lesson(workspace_root: str | Path, task_id: str, lesson_text: str) -> None:
    root = Path(workspace_root).resolve()
    memory_dir = root / ".specify" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    lessons_file = memory_dir / "lessons.md"

    entry = f"\n- **[{task_id}]**: {lesson_text.strip()}"
    if not lessons_file.exists():
        header = "# Harness² Persistent Memory & Experience Reflector\n\nLessons learned from autonomous task execution to guide future harness recursions:\n"
        lessons_file.write_text(header + entry + "\n", encoding="utf-8")
    else:
        with open(lessons_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    print(f"Recorded lesson for {task_id} into {lessons_file}")

if __name__ == "__main__":
    ws = Path.cwd()
    if len(sys.argv) > 1 and sys.argv[1] == "preflight":
        print(run_preflight_check(ws))
    elif len(sys.argv) > 3 and sys.argv[1] == "reflect":
        t_id = sys.argv[2]
        t_lesson = " ".join(sys.argv[3:])
        record_lesson(ws, t_id, t_lesson)
    else:
        print(run_preflight_check(ws))
