#!/usr/bin/env python3
"""
Extract patterns, pitfalls, and decision points from Claude Code JSONL sessions.

Usage:
    python extract_session_patterns.py                    # All sessions
    python extract_session_patterns.py --project MyProject # Filter by project name substring
    python extract_session_patterns.py --output report.md # Custom output path

Scans ~/.claude/projects/*/*.jsonl for:
  - Session titles and sizes
  - User corrections / redirections (pitfalls)
  - Decision points (user choosing between approaches)
  - Error patterns (tool failures, retries)
  - Phase transitions (ideation > spec > build > etc.)
  - Agent/skill invocations

NOTE: This script uses regex pattern matching, not semantic classification.
It surfaces raw correction moments and decision points. The 11 anti-patterns
(AP-01 through AP-11) in this repo were classified separately by an LLM
reading the script's output with session context, then reviewed and approved
by the human author. Running this script gives you raw material, not a
finished taxonomy. The classification step is yours.
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime


CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"

# Patterns that indicate user frustration / correction
CORRECTION_PATTERNS = [
    r"(?i)no[,.]?\s+(?:that's not|i said|i meant|stop|don't|wrong)",
    r"(?i)(?:you're|you are)\s+(?:wrong|missing|not listening|ignoring)",
    r"(?i)(?:i already|i just|we already)\s+(?:told|said|mentioned)",
    r"(?i)(?:read it again|re-read|look again|try again)",
    r"(?i)(?:that's not what i|not what i asked|not what i meant)",
    r"(?i)(?:wtf|ffs|damn|shit|bloody|for god)",
    r"(?i)(?:start over|from scratch|reset|undo)",
]

# Patterns that indicate a decision point
DECISION_PATTERNS = [
    r"(?i)(?:let's go with|i prefer|option [a-d1-4]|approach [a-d1-4])",
    r"(?i)(?:use .+ instead of|switch to|change to|pivot to)",
    r"(?i)(?:we should|let's use|go with|choose)",
    r"(?i)(?:fluent|mcp|jarvis|sdk)\s+(?:instead|over|not)",
]

# Patterns that indicate phase transitions
PHASE_PATTERNS = {
    "discovery": [r"(?i)(?:discovery|requirements|stakeholder|customer said|they want)"],
    "spec": [r"(?i)(?:spec\.md|whitepaper|architecture doc|write up|document the)"],
    "architecture": [r"(?i)(?:diagram|mermaid|flow map|table design|component|module)"],
    "build": [r"(?i)(?:scaffold|create the|build the|implement|\.now\.ts|now\.config)"],
    "validation": [r"(?i)(?:test|playwright|validate|verify|check if|does it work)"],
    "documentation": [r"(?i)(?:clickthrough|briefing|html|export|archive|deliverable)"],
    "social": [r"(?i)(?:social card|gif|linkedin|share|post about)"],
}

# Tool/skill invocations to track (patterns match raw JSONL log data)
SKILL_PATTERNS = [
    r"now-sdk-explain",
    r"jarvis",
    r"comprehensive-self-improvement",
    r"learning-mode",
    r"servicenow-browser-testing",
    r"servicenow-architect-agent",
    r"mcp__jarvis-servicenow",
    r"mcp__playwright",
]


def find_all_sessions(project_filter=None):
    """Find all JSONL session files under ~/.claude/projects/"""
    sessions = []
    if not CLAUDE_PROJECTS.exists():
        print(f"ERROR: {CLAUDE_PROJECTS} does not exist")
        sys.exit(1)

    for jsonl_file in CLAUDE_PROJECTS.rglob("*.jsonl"):
        project_dir = jsonl_file.parent.name
        if project_filter and project_filter.lower() not in project_dir.lower():
            continue
        sessions.append({
            "path": jsonl_file,
            "project": project_dir,
            "session_id": jsonl_file.stem,
        })
    return sorted(sessions, key=lambda s: s["project"])


def parse_session(session_path):
    """Parse a JSONL session file and extract structured data."""
    messages = []
    title = None
    metadata = {}
    errors = []

    with open(session_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                errors.append(f"Line {line_num}: invalid JSON")
                continue

            entry_type = entry.get("type")

            # Extract title
            if entry_type == "ai-title":
                title = entry.get("aiTitle", title)

            # Extract user messages
            if entry_type == "user":
                msg = entry.get("message", {})
                content_parts = msg.get("content", [])
                text = ""
                for part in content_parts:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text += part.get("text", "") + "\n"
                    elif isinstance(part, str):
                        text += part + "\n"
                if text.strip():
                    messages.append({
                        "role": "user",
                        "text": text.strip(),
                        "timestamp": entry.get("timestamp"),
                        "line": line_num,
                    })

            # Extract assistant messages
            if entry_type == "assistant":
                msg = entry.get("message", {})
                content_parts = msg.get("content", [])
                text = ""
                tool_uses = []
                for part in content_parts:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text += part.get("text", "") + "\n"
                        elif part.get("type") == "tool_use":
                            tool_uses.append(part.get("name", "unknown"))
                if text.strip() or tool_uses:
                    messages.append({
                        "role": "assistant",
                        "text": text.strip(),
                        "tools": tool_uses,
                        "timestamp": entry.get("timestamp"),
                        "line": line_num,
                    })

            # Extract metadata
            if entry.get("version"):
                metadata["version"] = entry["version"]
            if entry.get("entrypoint"):
                metadata["entrypoint"] = entry["entrypoint"]
            if entry.get("cwd"):
                metadata["cwd"] = entry["cwd"]

    return {
        "title": title or "(untitled)",
        "messages": messages,
        "metadata": metadata,
        "errors": errors,
        "line_count": line_num if messages else 0,
    }


def analyze_session(parsed):
    """Analyze a parsed session for patterns."""
    analysis = {
        "corrections": [],
        "decisions": [],
        "phases_detected": set(),
        "skills_used": Counter(),
        "tool_calls": Counter(),
        "user_message_count": 0,
        "assistant_message_count": 0,
        "error_retries": 0,
    }

    user_messages = [m for m in parsed["messages"] if m["role"] == "user"]
    assistant_messages = [m for m in parsed["messages"] if m["role"] == "assistant"]
    analysis["user_message_count"] = len(user_messages)
    analysis["assistant_message_count"] = len(assistant_messages)

    # Scan user messages for corrections
    for msg in user_messages:
        text = msg["text"]
        for pattern in CORRECTION_PATTERNS:
            if re.search(pattern, text):
                # Get surrounding context (truncated)
                snippet = text[:300].replace("\n", " ")
                analysis["corrections"].append({
                    "line": msg["line"],
                    "snippet": snippet,
                    "timestamp": msg.get("timestamp"),
                })
                break

    # Scan user messages for decisions
    for msg in user_messages:
        text = msg["text"]
        for pattern in DECISION_PATTERNS:
            if re.search(pattern, text):
                snippet = text[:300].replace("\n", " ")
                analysis["decisions"].append({
                    "line": msg["line"],
                    "snippet": snippet,
                    "timestamp": msg.get("timestamp"),
                })
                break

    # Detect phases
    all_text = " ".join(m["text"] for m in parsed["messages"])
    for phase, patterns in PHASE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, all_text):
                analysis["phases_detected"].add(phase)
                break

    # Track skills and tools
    for msg in assistant_messages:
        for tool in msg.get("tools", []):
            analysis["tool_calls"][tool] += 1
            for skill_pattern in SKILL_PATTERNS:
                if re.search(skill_pattern, tool, re.IGNORECASE):
                    analysis["skills_used"][skill_pattern] += 1

    # Check for skill invocations in user text
    for msg in user_messages:
        for skill_pattern in SKILL_PATTERNS:
            if re.search(skill_pattern, msg["text"], re.IGNORECASE):
                analysis["skills_used"][skill_pattern] += 1

    return analysis


def generate_report(all_results, output_path=None):
    """Generate a markdown report from all session analyses."""
    lines = []
    lines.append("# ServiceNow Delivery Pipeline - Session Analysis Report")
    lines.append(f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append(f"\n**Sessions analyzed:** {len(all_results)}")

    # Summary stats
    total_user = sum(r["analysis"]["user_message_count"] for r in all_results)
    total_asst = sum(r["analysis"]["assistant_message_count"] for r in all_results)
    total_corrections = sum(len(r["analysis"]["corrections"]) for r in all_results)
    total_decisions = sum(len(r["analysis"]["decisions"]) for r in all_results)

    lines.append(f"\n**Total user messages:** {total_user}")
    lines.append(f"**Total assistant messages:** {total_asst}")
    lines.append(f"**Corrections/redirections detected:** {total_corrections}")
    lines.append(f"**Decision points detected:** {total_decisions}")

    # Phase coverage
    all_phases = Counter()
    for r in all_results:
        for phase in r["analysis"]["phases_detected"]:
            all_phases[phase] += 1

    lines.append("\n## Phase Coverage Across Sessions\n")
    lines.append("| Phase | Sessions | % |")
    lines.append("|-------|----------|---|")
    for phase, count in sorted(all_phases.items(), key=lambda x: -x[1]):
        pct = round(100 * count / len(all_results))
        lines.append(f"| {phase} | {count} | {pct}% |")

    # Tool usage
    all_tools = Counter()
    for r in all_results:
        all_tools.update(r["analysis"]["tool_calls"])

    lines.append("\n## Top Tool Usage\n")
    lines.append("| Tool | Invocations |")
    lines.append("|------|-------------|")
    for tool, count in all_tools.most_common(20):
        lines.append(f"| `{tool}` | {count} |")

    # Skill usage
    all_skills = Counter()
    for r in all_results:
        all_skills.update(r["analysis"]["skills_used"])

    if all_skills:
        lines.append("\n## Skill/Agent Invocations\n")
        lines.append("| Skill | Mentions |")
        lines.append("|-------|----------|")
        for skill, count in all_skills.most_common():
            lines.append(f"| `{skill}` | {count} |")

    # Per-project breakdown
    by_project = defaultdict(list)
    for r in all_results:
        by_project[r["project"]].append(r)

    lines.append("\n---\n## Sessions by Project\n")
    for project, results in sorted(by_project.items()):
        clean_name = project.replace("-Users-leo-francia-", "").replace("-", " / ")
        if not clean_name or clean_name == "":
            clean_name = "(home directory)"
        lines.append(f"\n### {clean_name}\n")
        for r in results:
            title = r["parsed"]["title"]
            n_lines = r["parsed"]["line_count"]
            n_corrections = len(r["analysis"]["corrections"])
            n_decisions = len(r["analysis"]["decisions"])
            phases = ", ".join(sorted(r["analysis"]["phases_detected"])) or "none detected"
            lines.append(f"- **{title}** ({n_lines} lines)")
            lines.append(f"  - Phases: {phases}")
            lines.append(f"  - Corrections: {n_corrections} | Decisions: {n_decisions}")
            if r["analysis"]["corrections"]:
                lines.append(f"  - Top correction: _{r['analysis']['corrections'][0]['snippet'][:120]}..._")

    # Corrections deep-dive (the gold)
    all_corrections = []
    for r in all_results:
        for c in r["analysis"]["corrections"]:
            all_corrections.append({
                "project": r["project"],
                "title": r["parsed"]["title"],
                **c,
            })

    if all_corrections:
        lines.append("\n---\n## All Corrections & Redirections (Pitfalls Gold Mine)\n")
        lines.append("These are moments where the user corrected the agent - each one is a potential pipeline rule.\n")
        for i, c in enumerate(all_corrections, 1):
            clean_project = c["project"].replace("-Users-leo-francia-", "")
            lines.append(f"### Correction {i} - {clean_project}")
            lines.append(f"**Session:** {c['title']}")
            lines.append(f"**Line:** {c['line']}")
            lines.append(f"\n> {c['snippet']}\n")

    # Decision points deep-dive
    all_decisions = []
    for r in all_results:
        for d in r["analysis"]["decisions"]:
            all_decisions.append({
                "project": r["project"],
                "title": r["parsed"]["title"],
                **d,
            })

    if all_decisions:
        lines.append("\n---\n## All Decision Points\n")
        lines.append("Moments where the user chose between approaches - these become pipeline branching logic.\n")
        for i, d in enumerate(all_decisions, 1):
            clean_project = d["project"].replace("-Users-leo-francia-", "")
            lines.append(f"### Decision {i} - {clean_project}")
            lines.append(f"**Session:** {d['title']}")
            lines.append(f"\n> {d['snippet']}\n")

    report = "\n".join(lines)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(report)
        print(f"Report written to {output_path}")
    else:
        print(report)

    return report


def main():
    parser = argparse.ArgumentParser(description="Extract patterns from Claude Code JSONL sessions")
    parser.add_argument("--project", help="Filter sessions by project name substring")
    parser.add_argument("--output", help="Output path for the report (default: stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    args = parser.parse_args()

    sessions = find_all_sessions(args.project)
    if not sessions:
        print("No sessions found.")
        sys.exit(1)

    if args.verbose:
        print(f"Found {len(sessions)} sessions")

    all_results = []
    for session in sessions:
        if args.verbose:
            print(f"  Parsing {session['project']}/{session['session_id']}...")
        parsed = parse_session(session["path"])
        analysis = analyze_session(parsed)
        all_results.append({
            "project": session["project"],
            "session_id": session["session_id"],
            "parsed": parsed,
            "analysis": analysis,
        })

    output = args.output or str(
        Path(__file__).parent / "session-analysis-report.md"
    )
    generate_report(all_results, output)


if __name__ == "__main__":
    main()
