#!/usr/bin/env python3
"""
Oh-My-Anti / OMP-Parity Custom Statusline for Antigravity (agy).
Matches the exact visual elegance, git tracking, context window, model identification,
and swarm/task monitoring of OMP (Oh My Pi), augmented with Google Research Harness² Task Ledger.
"""

import sys
import json
import os
import glob
import re
import subprocess
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

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

def get_git_info(cwd):
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True, timeout=0.15
        ).strip()
        if not branch:
            return ""
        status_out = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True, timeout=0.25
        )
        lines = [l for l in status_out.splitlines() if l.strip()]
        modified = sum(1 for l in lines if not l.startswith("??"))
        untracked = sum(1 for l in lines if l.startswith("??"))
        
        stat = []
        if modified > 0:
            stat.append(f"*{modified}")
        if untracked > 0:
            stat.append(f"?{untracked}")
        stat_str = " " + " ".join(stat) if stat else ""
        return f"⑂ {branch}{stat_str}"
    except Exception:
        return ""

def get_task_ledger_info(cwd):
    """Deep-dive probe for active tasks in workspace (Harness² & Spec Kit DAG)"""
    try:
        # Check .specify/memory/tasks_ledger.json first
        ledger_path = os.path.join(cwd, ".specify", "memory", "tasks_ledger.json")
        if os.path.exists(ledger_path):
            with open(ledger_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                total = data.get("total_tasks", 0)
                done = data.get("completed_tasks", 0)
                active_task = None
                for t in data.get("tasks", []):
                    if t.get("status") == "IN_PROGRESS":
                        t_id = t.get("id", "TASK")
                        t_title = t.get("title", "")[:18]
                        active_task = f"[{t_id}:▶ {t_title}]"
                        break
                    if not active_task and t.get("status") == "TODO":
                        t_id = t.get("id", "TASK")
                        t_title = t.get("title", "")[:18]
                        active_task = f"[{t_id}:▶ {t_title}]"
                if total > 0:
                    badge = f" {active_task}" if active_task else ""
                    return f"📋 {done}/{total}{badge}"

        # Fallback to inspecting specs/*/tasks.md
        spec_tasks = glob.glob(os.path.join(cwd, "specs", "*", "tasks.md"))
        if spec_tasks:
            latest = max(spec_tasks, key=os.path.getmtime)
            with open(latest, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            
            total = sum(1 for l in lines if re.match(r"^\s*-\s*\[[ xX>!~]\]", l))
            done = sum(1 for l in lines if re.match(r"^\s*-\s*\[[xX]\]", l))
            
            active_badge = ""
            for l in lines:
                m = re.match(r"^\s*-\s*\[([ >])\]\s*(\[?(T\d+)\]?:?)?\s*(.*)", l)
                if m:
                    marker, _, tid, desc = m.groups()
                    tid_str = tid if tid else "TASK"
                    clean_desc = desc.strip()
                    if ":" in clean_desc and len(clean_desc.split(":", 1)[0]) < 20:
                        clean_desc = clean_desc.split(":", 1)[1].strip()
                    short_desc = (clean_desc[:16] + "..") if len(clean_desc) > 18 else clean_desc
                    active_badge = f" [{tid_str}:▶ {short_desc}]"
                    break
                    
            if total > 0:
                return f"📋 {done}/{total}{active_badge}"
    except Exception:
        pass
    return None

def render_statusline():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            data = {}
        else:
            data = json.loads(raw_input)
    except Exception:
        data = {}

    current_dir = data.get("current_dir", os.getcwd())

    # 1. Mode Pill
    mode = str(data.get("agentMode", data.get("currentModeId", data.get("mode", "auto")))).upper()
    mode_symbol = "⚡"
    if "PLAN" in mode:
        mode_str = f"{FG_MAGENTA}{BOLD}{mode_symbol} PLAN{RESET}"
    elif "ACCEPT" in mode:
        mode_str = f"{FG_GREEN}{BOLD}{mode_symbol} ACCEPT{RESET}"
    else:
        mode_str = f"{FG_BLUE}{BOLD}{mode_symbol} AUTO{RESET}"

    # 2. Model Name Extraction
    model_raw = data.get("currentModelId") or data.get("model") or data.get("selectedModel") or "Gemini 3.8 Flash"
    if isinstance(model_raw, dict):
        model_name = model_raw.get("label") or model_raw.get("name") or model_raw.get("displayName") or model_raw.get("id") or "Gemini"
    else:
        model_name = str(model_raw)
    
    # Strip prefixes and format
    model_name = model_name.replace("models/", "").replace("google/", "").replace("(High)", "").strip()
    if len(model_name) > 22:
        model_name = model_name[:20] + ".."
    model_str = f"{FG_CYAN}◒ {model_name}{RESET}"

    # 3. Directory
    dir_name = os.path.basename(current_dir.rstrip("\\/")) or "workspace"
    dir_str = f"{FG_WHITE}📁 …/{dir_name}{RESET}"

    # 4. Git Info
    git_info = get_git_info(current_dir)
    git_str = f"{FG_MAGENTA}{git_info}{RESET}" if git_info else ""

    # 5. Context Window & Token percentage
    input_tokens = data.get("input_tokens", 0) or 0
    cached_tokens = data.get("cached_tokens", 0) or 0
    total_tokens = input_tokens + cached_tokens
    max_context = 1000000  # 1M context window for Gemini
    pct = (total_tokens / max_context) * 100 if total_tokens > 0 else 0.0
    context_str = f"{FG_YELLOW}◫ {pct:.1f}%/1M ⟲{RESET}"

    # 6. Cost / Quota
    usd = data.get("subagent_usd", data.get("total_usd", None))
    if usd is not None and isinstance(usd, (int, float)):
        cost_str = f"{FG_GREEN}${usd:.2f}{RESET}"
    else:
        cost_str = f"{FG_GREEN}free{RESET}"

    # 7. Tasks & Swarm Deep Dive
    task_ledger_str = get_task_ledger_info(current_dir)
    if task_ledger_str:
        task_str = f"{FG_YELLOW}{task_ledger_str}{RESET}"
    else:
        artifact_count = data.get("artifact_count", 0) or 0
        task_str = f"{FG_YELLOW}📋 {artifact_count}{RESET}"

    subagents = data.get("Subagents", data.get("active_subagents", []))
    subagent_count = len(subagents) if isinstance(subagents, list) else 0

    swarm_icon = "🐝" if subagent_count > 0 else "💤"
    swarm_str = f"{FG_CYAN}{swarm_icon} {subagent_count}{RESET}"

    # Separator
    sep = f"{FG_DARKGRAY} · {RESET}"

    # Assemble elements
    elements = [
        f"{FG_CYAN}{BOLD}π{RESET}",
        mode_str,
        model_str,
        dir_str
    ]
    if git_str:
        elements.append(git_str)
    elements.extend([
        context_str,
        cost_str,
        task_str,
        swarm_str
    ])

    line = sep.join(elements)

    try:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
    except Exception:
        clean = line.encode("ascii", "replace").decode("ascii")
        sys.stdout.write(clean + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    render_statusline()
