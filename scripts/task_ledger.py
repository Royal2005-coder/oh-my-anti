#!/usr/bin/env python3
"""
Task Ledger & DAG Engine for Antigravity (agy / oh-my-anti)
Inspired by Google Research Harness2 and Oh-My-Pi (OMP).
Parses, schedules, and tracks atomic task checklists with dependencies and verification gates.
"""

from __future__ import annotations
import os
import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

# UTF-8 safe stdout for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

@dataclass
class TaskItem:
    id: str
    title: str
    phase: str
    status: str  # "TODO", "IN_PROGRESS", "DONE", "BLOCKED", "FAILED"
    dependencies: List[str] = field(default_factory=list)
    role: str = "general"
    verify_cmd: str = ""
    line_number: int = -1

@dataclass
class TaskLedger:
    feature_name: str
    spec_path: str
    tasks_path: str
    total_tasks: int = 0
    completed_tasks: int = 0
    in_progress_tasks: int = 0
    tasks: List[TaskItem] = field(default_factory=list)

    def progress_percentage(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round((self.completed_tasks / self.total_tasks) * 100, 1)

    def current_active_task(self) -> Optional[TaskItem]:
        for t in self.tasks:
            if t.status == "IN_PROGRESS":
                return t
        for t in self.tasks:
            if t.status == "TODO":
                return t
        return None

def parse_tasks_md(tasks_path: str | Path) -> TaskLedger:
    path = Path(tasks_path)
    if not path.exists():
        return TaskLedger(feature_name="Unknown", spec_path="", tasks_path=str(tasks_path))

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    current_phase = "Phase 1: Implementation"
    tasks: List[TaskItem] = []
    feature_name = path.parent.name if path.parent else "feature"

    # Regex patterns
    phase_pattern = re.compile(r"^#+\s*(Phase\s*\d+[^:\n]*|Setup|Verification|Polish)", re.IGNORECASE)
    task_pattern = re.compile(r"^[-*]\s*\[([ xX>!~])\]\s*(?:\[?(T\d+)\]?:?)?\s*(.*)$")
    dep_pattern = re.compile(r"\[(?:depends\s*on|deps?):\s*([^\]]+)\]", re.IGNORECASE)
    role_pattern = re.compile(r"\[(?:role|agent):\s*([^\]]+)\]", re.IGNORECASE)
    verify_pattern = re.compile(r"\[(?:verify|test):\s*`?([^\]`]+)`?\]", re.IGNORECASE)

    task_counter = 1

    for idx, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue

        phase_match = phase_pattern.match(line_clean)
        if phase_match:
            current_phase = phase_match.group(1).strip()
            continue

        task_match = task_pattern.match(line_clean)
        if task_match:
            marker = task_match.group(1).strip()
            raw_id = task_match.group(2)
            raw_desc = task_match.group(3).strip()

            task_id = raw_id if raw_id else f"T{task_counter:02d}"
            task_counter += 1

            status = "TODO"
            if marker.lower() == "x":
                status = "DONE"
            elif marker == ">":
                status = "IN_PROGRESS"
            elif marker == "!":
                status = "FAILED"
            elif marker == "~":
                status = "BLOCKED"

            deps = []
            dep_m = dep_pattern.search(raw_desc)
            if dep_m:
                deps = [d.strip() for d in dep_m.group(1).split(",") if d.strip()]
                raw_desc = dep_pattern.sub("", raw_desc).strip()

            role = "general"
            role_m = role_pattern.search(raw_desc)
            if role_m:
                role = role_m.group(1).strip()
                raw_desc = role_pattern.sub("", raw_desc).strip()

            verify = ""
            verify_m = verify_pattern.search(raw_desc)
            if verify_m:
                verify = verify_m.group(1).strip()
                raw_desc = verify_pattern.sub("", raw_desc).strip()

            clean_title = re.sub(r"\s+", " ", raw_desc).strip()

            tasks.append(
                TaskItem(
                    id=task_id,
                    title=clean_title,
                    phase=current_phase,
                    status=status,
                    dependencies=deps,
                    role=role,
                    verify_cmd=verify,
                    line_number=idx,
                )
            )

    completed = sum(1 for t in tasks if t.status == "DONE")
    in_prog = sum(1 for t in tasks if t.status == "IN_PROGRESS")

    ledger = TaskLedger(
        feature_name=feature_name,
        spec_path=str(path.parent / "spec.md"),
        tasks_path=str(path),
        total_tasks=len(tasks),
        completed_tasks=completed,
        in_progress_tasks=in_prog,
        tasks=tasks,
    )
    return ledger

def save_ledger_json(ledger: TaskLedger, output_json: str | Path) -> None:
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(ledger), f, indent=2, ensure_ascii=False)

def render_omp_task_table(ledger: TaskLedger) -> str:
    """Render an OMP-style visual task table with phase grouping and status badges."""
    lines = []
    pct = ledger.progress_percentage()
    bar_width = 24
    filled = int(bar_width * (pct / 100.0))
    bar = "█" * filled + "░" * (bar_width - filled)

    lines.append(f"┌{'─' * 74}┐")
    lines.append(f"│  🎯 TASK ORCHESTRATION LEDGER · {ledger.feature_name:<30} {pct:>5.1f}% │")
    lines.append(f"│  Progress: [{bar}] ({ledger.completed_tasks}/{ledger.total_tasks} done) {' ' * (24 - len(str(ledger.completed_tasks)) - len(str(ledger.total_tasks)))}│")
    lines.append(f"├{'─'*8}┬{'─'*6}┬{'─'*43}┬{'─'*13}┤")
    lines.append(f"│ Status │ ID   │ Task Description                         │ Role        │")
    lines.append(f"├{'─'*8}┼{'─'*6}┼{'─'*43}┼{'─'*13}┤")

    status_badges = {
        "DONE": "[✓] DONE",
        "IN_PROGRESS": "[▶] PROG",
        "TODO": "[ ] TODO",
        "BLOCKED": "[~] BLOK",
        "FAILED": "[✗] FAIL",
    }

    current_p = None
    for t in ledger.tasks:
        if t.phase != current_p:
            current_p = t.phase
            clean_phase = current_p[:70]
            lines.append(f"│ 📂 {clean_phase:<69} │")

        badge = status_badges.get(t.status, "[ ] TODO")
        short_title = (t.title[:40] + "..") if len(t.title) > 42 else t.title
        short_role = t.role[:11]
        lines.append(f"│ {badge:<6} │ {t.id:<4} │ {short_title:<41} │ {short_role:<11} │")

    lines.append(f"└{'─'*8}┴{'─'*6}┴{'─'*43}┴{'─'*13}┘")
    return "\n".join(lines)

def update_task_status(tasks_path: str | Path, task_id: str, new_status: str) -> bool:
    path = Path(tasks_path)
    if not path.exists():
        return False

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    marker_map = {
        "DONE": "x",
        "IN_PROGRESS": ">",
        "TODO": " ",
        "BLOCKED": "~",
        "FAILED": "!",
    }
    marker = marker_map.get(new_status.upper(), " ")

    task_pattern = re.compile(rf"^([-*]\s*\[)[ xX>!~](\]\s*\[?{re.escape(task_id)}\]?:?.*)$")

    updated = False
    new_lines = []
    for line in lines:
        if task_pattern.match(line):
            line = task_pattern.sub(rf"\g<1>{marker}\g<2>", line)
            updated = True
        new_lines.append(line)

    if updated:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return updated

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: task_ledger.py <path_to_tasks.md> [--json <out.json>] [--update <TASK_ID> <STATUS>]")
        sys.exit(0)

    target_md = sys.argv[1]
    if "--update" in sys.argv:
        u_idx = sys.argv.index("--update")
        t_id = sys.argv[u_idx + 1]
        t_status = sys.argv[u_idx + 2]
        if update_task_status(target_md, t_id, t_status):
            print(f"Updated {t_id} -> {t_status}")
        else:
            print(f"Failed to find {t_id}")

    ledger = parse_tasks_md(target_md)
    if "--json" in sys.argv:
        j_idx = sys.argv.index("--json")
        out_json = sys.argv[j_idx + 1]
        save_ledger_json(ledger, out_json)
        print(f"Ledger JSON saved to {out_json}")
    else:
        print(render_omp_task_table(ledger))
