#!/usr/bin/env python3
"""
Task Ledger & DAG Engine for Antigravity (agy / oh-my-anti)
Inspired by Google Research Harness2 and Oh-My-Pi (OMP).
Parses, schedules, and tracks atomic task checklists with visual Tree Views, DAGs, and verification gates.
"""

from __future__ import annotations
import os
import re
import sys
import glob
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

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
FG_WHITE = "\033[97m"
FG_GRAY = "\033[38;5;245m"
FG_DARKGRAY = "\033[38;5;239m"
FG_CYAN = "\033[96m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_MAGENTA = "\033[95m"
FG_RED = "\033[91m"
FG_BLUE = "\033[94m"

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
    phase_pattern = re.compile(r"^#+\s*(Phase\s*\d+[^:\n]*|Setup|Foundational|Verification|Readiness|Product detail|Header search|Polish)", re.IGNORECASE)
    task_pattern = re.compile(r"^[-*]\s*\[([ xX>!~])\]\s*(?:\[?(T[0-9a-zA-Z_\-]+)\]?:?)?\s*(.*)$")
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

            task_id = raw_id if raw_id else f"T{task_counter:03d}"
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

    return TaskLedger(
        feature_name=feature_name,
        spec_path=str(path.parent / "spec.md"),
        tasks_path=str(path),
        total_tasks=len(tasks),
        completed_tasks=completed,
        in_progress_tasks=in_prog,
        tasks=tasks,
    )

def render_omp_task_tree(ledger: TaskLedger, color: bool = True) -> str:
    """Render a hierarchical tree showing completed, in-progress, and next-up tasks."""
    c_reset = RESET if color else ""
    c_bold = BOLD if color else ""
    c_green = FG_GREEN if color else ""
    c_cyan = FG_CYAN if color else ""
    c_yellow = FG_YELLOW if color else ""
    c_gray = FG_GRAY if color else ""
    c_darkgray = FG_DARKGRAY if color else ""

    pct = ledger.progress_percentage()
    bar_width = 20
    filled = int(bar_width * (pct / 100.0))
    bar = "█" * filled + "░" * (bar_width - filled)

    lines = []
    lines.append(f"{c_bold}🌳 TASK EXECUTION TREE · {ledger.feature_name}{c_reset}")
    lines.append(f"{c_gray}Progress: [{c_green}{bar}{c_gray}] {c_yellow}{ledger.completed_tasks}/{ledger.total_tasks} done ({pct}%){c_reset}")
    lines.append(f"{c_darkgray}{'─' * 70}{c_reset}")

    # Group by phase
    phases: Dict[str, List[TaskItem]] = {}
    for t in ledger.tasks:
        phases.setdefault(t.phase, []).append(t)

    phase_items = list(phases.items())
    active_found = False

    for p_idx, (phase_name, phase_tasks) in enumerate(phase_items):
        is_last_phase = (p_idx == len(phase_items) - 1)
        p_prefix = "└── " if is_last_phase else "├── "
        p_sub = "    " if is_last_phase else "│   "

        p_done = sum(1 for t in phase_tasks if t.status == "DONE")
        p_total = len(phase_tasks)
        p_status_badge = f"{c_green}[{p_done}/{p_total}]{c_reset}" if p_done == p_total else f"{c_yellow}[{p_done}/{p_total}]{c_reset}"

        lines.append(f"{c_bold}{p_prefix}📂 {phase_name} {p_status_badge}{c_reset}")

        for t_idx, t in enumerate(phase_tasks):
            is_last_task = (t_idx == len(phase_tasks) - 1)
            t_prefix = "└── " if is_last_task else "├── "

            # Determine badge & highlight
            if t.status == "DONE":
                badge = f"{c_green}[✓] {t.id}{c_reset}"
                title_str = f"{c_gray}{t.title}{c_reset}"
                extra = ""
            elif t.status == "IN_PROGRESS" or (t.status == "TODO" and not active_found):
                active_found = True
                badge = f"{c_cyan}{c_bold}[▶] {t.id}{c_reset}"
                title_str = f"{c_cyan}{c_bold}{t.title}{c_reset}"
                extra = f" {c_yellow}◀ CURRENT ACTIVE TASK{c_reset}"
            elif t.status == "BLOCKED":
                badge = f"{c_yellow}[~] {t.id}{c_reset}"
                title_str = f"{c_gray}{t.title}{c_reset}"
                extra = f" {c_yellow}(Blocked){c_reset}"
            elif t.status == "FAILED":
                badge = f"{FG_RED}[✗] {t.id}{c_reset}"
                title_str = f"{t.title}{c_reset}"
                extra = f" {FG_RED}(Failed){c_reset}"
            else:
                badge = f"{c_darkgray}[ ] {t.id}{c_reset}"
                title_str = f"{c_darkgray}{t.title}{c_reset}"
                extra = ""

            # Truncate title cleanly if too long
            max_len = 55
            if len(t.title) > max_len:
                title_clean = t.title[:max_len] + ".."
            else:
                title_clean = t.title

            if extra:
                lines.append(f"{p_sub}{t_prefix}{badge} {title_str}{extra}")
            else:
                lines.append(f"{p_sub}{t_prefix}{badge} {title_str}")

    lines.append(f"{c_darkgray}{'─' * 70}{c_reset}")
    return "\n".join(lines)

def render_omp_task_table(ledger: TaskLedger) -> str:
    lines = []
    pct = ledger.progress_percentage()
    bar_width = 24
    filled = int(bar_width * (pct / 100.0))
    bar = "█" * filled + "░" * (bar_width - filled)

    lines.append(f"┌{'─' * 74}┐")
    lines.append(f"│  🎯 TASK ORCHESTRATION LEDGER · {ledger.feature_name:<30} {pct:>5.1f}% │")
    lines.append(f"│  Progress: [{bar}] ({ledger.completed_tasks}/{ledger.total_tasks} done) {' ' * max(0, 24 - len(str(ledger.completed_tasks)) - len(str(ledger.total_tasks)))}│")
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

def find_latest_tasks_file(cwd: Path) -> Optional[Path]:
    candidates = list(cwd.glob("specs/*/tasks.md"))
    if not candidates:
        candidates = list(cwd.glob(".specify/**/tasks.md"))
    if candidates:
        return max(candidates, key=lambda p: p.stat().st_mtime)
    return None

if __name__ == "__main__":
    target_path = None
    args = sys.argv[1:]

    # Check for target file in args
    for arg in args:
        if not arg.startswith("--") and Path(arg).is_file():
            target_path = Path(arg)
            break

    if not target_path:
        target_path = find_latest_tasks_file(Path.cwd())

    if not target_path or not target_path.exists():
        print("No tasks.md found in workspace (expected in specs/<feature>/tasks.md)")
        sys.exit(0)

    ledger = parse_tasks_md(target_path)

    if "--json" in args:
        j_idx = args.index("--json")
        out_json = args[j_idx + 1] if j_idx + 1 < len(args) else ".specify/memory/tasks_ledger.json"
        Path(out_json).parent.mkdir(parents=True, exist_ok=True)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(asdict(ledger), f, indent=2, ensure_ascii=False)
        print(f"Saved {out_json}")
    elif "--table" in args:
        print(render_omp_task_table(ledger))
    else:
        # Default: render Tree View
        print(render_omp_task_tree(ledger))
