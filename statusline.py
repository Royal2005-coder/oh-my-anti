#!/usr/bin/env python3
"""
Oh-My-Anti / OMP-Style Custom Statusline for Antigravity (agy).
Receives real-time JSON via stdin every cycle and formats a rich, multi-segment visual status bar.
Robust against Windows CP1252/Unicode terminal encoding limitations.
"""

import sys
import json
import os

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

# Segment background / foreground colors
BG_BLUE = "\033[44m"
FG_WHITE = "\033[97m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
FG_BLACK = "\033[30m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_DARK = "\033[48;5;236m"
FG_GRAY = "\033[38;5;250m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_CYAN = "\033[96m"
FG_MAGENTA = "\033[95m"

def render_statusline():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            data = {}
        else:
            data = json.loads(raw_input)
    except Exception:
        data = {}

    # Extract metrics safely
    mode = str(data.get("agentMode", data.get("currentModeId", data.get("mode", "auto")))).upper()
    model = str(data.get("currentModelId", data.get("model", "gemini-3.8"))).replace("models/", "")
    if len(model) > 16:
        model = model[:14] + ".."

    tokens = data.get("input_tokens", data.get("cached_tokens", 0))
    artifact_count = data.get("artifact_count", 0)
    current_dir = data.get("current_dir", os.getcwd())
    dir_name = os.path.basename(current_dir.rstrip("\\/")) or "workspace"

    # Subagents / Background Tasks
    subagents = data.get("Subagents", data.get("active_subagents", []))
    subagent_count = len(subagents) if isinstance(subagents, list) else 0

    # Build stylized segments
    # Segment 1: Mode pill
    mode_color = BG_MAGENTA if "PLAN" in mode else (BG_BLUE if "AUTO" in mode else BG_GREEN)
    seg_mode = f"{mode_color}{FG_WHITE}{BOLD} [MODE: {mode}] {RESET}"

    # Segment 2: Model pill
    seg_model = f"{BG_DARK}{FG_CYAN} [MODEL: {model}] {RESET}"

    # Segment 3: Workspace dir
    seg_dir = f"{BG_DARK}{FG_WHITE} [{dir_name}] {RESET}"

    # Segment 4: Artifacts / Tasks
    seg_artifacts = f"{BG_DARK}{FG_YELLOW} [Tasks: {artifact_count}] {RESET}"

    # Segment 5: Active Subagents (EGM Swarm)
    seg_swarm = f"{BG_DARK}{FG_GREEN} [Swarm: {subagent_count}] {RESET}"

    # Segment 6: Token info
    if isinstance(tokens, (int, float)) and tokens > 0:
        if tokens > 1000:
            token_str = f"{tokens/1000:.1f}k"
        else:
            token_str = str(tokens)
        seg_tokens = f"{BG_DARK}{FG_GRAY} [{token_str} tok] {RESET}"
    else:
        seg_tokens = ""

    # Assemble the final statusline
    line = f"{seg_mode}{seg_model}{seg_dir}{seg_artifacts}{seg_swarm}{seg_tokens}"
    try:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
    except Exception:
        # Fallback to pure ascii if anything fails
        clean = line.encode("ascii", "replace").decode("ascii")
        sys.stdout.write(clean + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    render_statusline()
