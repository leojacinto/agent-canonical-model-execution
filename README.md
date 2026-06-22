# Agent Canonical Model Execution (ACME)

A data-driven analysis of how AI coding agents actually perform when building ServiceNow applications with the Fluent SDK - extracted from 74 real sessions, 720 prompts, and every correction along the way.

---

## What This Is

Over 6+ months of building ServiceNow implementations using Claude Code, Cascade, and an internal multi-agent ServiceNow orchestrator<sup>[1]</sup>, a delivery pipeline crystallised. This repo codifies that pipeline and the rules behind it - extracted directly from conversation logs between a human Solution Engineer and AI coding agents.

**The approach:** Trace actual conversations. Find where the agent failed. Classify the failures. Turn them into guardrails.

**The scope:** ServiceNow Fluent SDK delivery, from ideation to social card. The anti-patterns themselves apply to any AI-assisted build pipeline - the evidence is ServiceNow-specific, the lessons transfer.

**Methodology:** Two stages. First, `extract_session_patterns.py` scans Claude Code JSONL logs using regex pattern matching to surface correction moments (user frustration, redirections, profanity) and decision points. The script does not classify anything - it produces raw material. Second, an LLM (Claude/Cascade) read all 57 corrections with surrounding session context and clustered them into the 11 named anti-patterns, assigned severity ratings, and wrote the case study narratives. The human reviewed, edited, and approved every classification. This repo is the product of human-directed LLM analysis of human-AI coding sessions - not a fully automated pipeline. If you run the extraction script on your own sessions, you get raw corrections and decisions. The taxonomy is yours to build.

**Who this is for:** Solution Architects, Solution Engineers, and developers who use AI coding agents to build on ServiceNow.

**How to use this:** This is a starting point and by no means a prescription. The pipeline phases, rules, and anti-patterns reflect one Solution Engineer's delivery pattern across specific projects and agents. Your tooling, instance configuration, team structure, and risk tolerance will differ. Read the case studies for context, then adjust the pipeline and rules to match how you actually work. Delete what does not apply. Add what is missing.

## Getting Started

1. **Read the case studies first** (`session-case-studies.md`) - they give you the context behind the rules. Without the stories, the rules are just a checklist.

2. **Review the anti-patterns** (`anti-patterns.md`) - identify which ones you have already hit. Most teams recognise AP-01 (Confident Fabricator) and AP-06 (Visual Illiterate) immediately.

3. **Adopt the pipeline selectively** (`servicenow-fluent-delivery-pipeline.md`) - start with the phases you already follow and add the decision gates that would have caught your last failure.

4. **Use the rules as a pre-flight checklist** (`pipeline-rules.md`) - print them, pin them, or paste them into your agent's system prompt or `CLAUDE.md`.

5. **Run the extraction on your own sessions** - if you use Claude Code, point the script at your JSONL logs:
   ```bash
   python3 extract_session_patterns.py --verbose
   ```
   Your corrections are your rules. This script helps you find them.

6. **Wire it into your agent sessions** - use `pipeline-rules-insert.md` to bring the rules into every new session:
   - **Claude Code:** Copy into `~/.claude/projects/[your-project]/memory/pipeline-rules.md`  -  it loads automatically
   - **Claude Code (CLAUDE.md):** Paste the rules into your project's `CLAUDE.md` under a `## Pipeline Rules` section
   - **Cascade:** Create `.windsurf/workflows/pipeline-checklist.md` with the insert content, then invoke via slash command
   - **Any agent:** Paste the contents into your first message or system prompt at session start

7. **Fork and adapt** - delete what does not apply. Rename the phases. Add your own anti-patterns. The value is in the structure, not the specifics.

## Contents

| File | What It Is |
|------|-----------|
| `servicenow-fluent-delivery-pipeline.md` | 7-phase pipeline - Ideation, Spec, Architecture, Build, Validation, Documentation, Deliverable. Decision gates, agent routing, Fluent SDK conventions. |
| `anti-patterns.md` | 11 named agent failure modes with severity ratings and a priority matrix. |
| `pipeline-rules.md` | 12 hard rules - each backed by real session evidence. Includes capture spec and brand compliance. |
| `session-case-studies.md` | 3 detailed case studies showing what went right, what went wrong, and what was learned. |
| `pipeline-rules-insert.md` | Compact, paste-ready version of the rules and top anti-patterns. Drop this into your agent's context at session start. |
| `extract_session_patterns.py` | Python script to extract patterns from Claude Code JSONL logs. Rerunnable. |

## Key Findings

- **57 corrections** across 74 sessions - most clustered in 3 high-complexity sessions
- **Top failure mode:** "The Confident Fabricator" - agent presents unverified output with the same confidence as verified output (18 occurrences)
- **Most expensive failure:** Spec errors cascading into parallel builds - hours of compute wasted on broken experiment conditions
- **Headroom experiment:** A controlled A/B test of context compression (using the [Headroom](https://github.com/chopratejas/headroom) repo) on a Fluent SDK build showed minimal quality difference between compressed and uncompressed contexts - but exposed 5 restart cycles worth of tooling failures that generated half the corpus's anti-patterns
- **Agents excel at structured analysis** and fail at aesthetic judgment. Route accordingly.
- **Social content needs 5-8 revision rounds.** This is normal. Budget for it.

## The Frustration Curve

Every high-correction session follows the same escalation:

```
1. Polite redirection     > "Can we do X instead?"
2. Firm correction        > "I said X. Do X."
3. Pointed feedback       > "Check the artifact first and stop guessing"
4. Explicit rule          > "Stop making it sound like a discovery when you caused the problem"
5. Permanent guardrail    > Memory file or CLAUDE.md rule created
```

Step 4 is where the transferable rule lives. Step 5 is where it becomes permanent.

## The 11 Anti-Patterns

| ID | Name | Severity | What Happens |
|----|------|----------|-------------|
| AP-01 | The Confident Fabricator | Critical | Presents fabricated paths, URLs, API patterns with full confidence |
| AP-02 | The Discovery Reframer | High | Presents its own errors as newly "discovered" issues |
| AP-03 | The Wheel Reinventor | High | Creates new versions instead of editing existing files, losing prior work |
| AP-04 | The Stale Data Polluter | High | Leaves remnants of abandoned approaches in the artifact |
| AP-05 | The Rube Goldberg Architect | Medium | Creates complex multi-tool workflows when simpler approaches exist |
| AP-06 | The Visual Illiterate | Medium | Produces structurally correct but visually poor output |
| AP-07 | The Inconsistency Generator | High | Tables and diagrams that describe the same process don't match |
| AP-08 | The Premature Researcher | Medium | Fetches docs before prerequisites are met |
| AP-09 | The Scope Leaker | Critical | Reads/writes to wrong directory in multi-condition experiments |
| AP-10 | The LLMism Leaker | Low | Produces AI-sounding prose with hedging and em dashes |
| AP-11 | The Tool Wanderer | Medium | Tries wrong tool repeatedly before finding the right one |

## Referenced Experiments

The case studies and findings in this repo draw from two published experiments:

| Experiment | Repo | What It Tested |
|-----------|------|---------------|
| Headroom Experiment | [leojacinto/headroom-experiment](https://github.com/leojacinto/headroom-experiment) | A/B test of context compression (Headroom) on a Fluent SDK build. Same spec, same model, two conditions. |
| Project Moreau | [leojacinto/project-moreau-test](https://github.com/leojacinto/project-moreau-test) | Does giving an AI build agent access to an existing codebase (monorepo) produce better ServiceNow apps? |

## Scope & Limitations

This pipeline covers **external AI coding agents** (Claude Code, Cascade, Devin) building ServiceNow applications via Fluent SDK and MCP, then side-loading artifacts into an instance.

It does **not** cover [ServiceNow Build Agent](https://www.servicenow.com/docs), which operates inside Studio/IDE within the instance itself. Build Agent is a different paradigm  -  no side-loading, no local file system, no external orchestration. It will have its own failure modes and its own pipeline patterns. An approach for documenting those is being explored separately.

## ServiceNow Documentation for LLMs

ServiceNow's documentation site (`docs.servicenow.com`) blocks bot/crawler access, which means AI coding agents cannot fetch current API references, table schemas, or platform documentation directly. This is a contributing factor to AP-01 (Confident Fabricator)  -  agents hallucinate ServiceNow API patterns because they cannot verify against the real docs.

**The workaround:** ServiceNow publishes LLM-optimised documentation on GitHub:

- **Repo:** [ServiceNow/ServiceNowDocs](https://github.com/ServiceNow/ServiceNowDocs) (Australia release family)
- **Format:** Markdown files + `llms.txt` index, designed for AI agent consumption
- **Usage:** Point your agent at the raw GitHub content, or clone the repo locally for offline reference

This should be the primary documentation source for any AI-assisted ServiceNow build. It is more reliable than letting the agent guess from training data.

## Data Sources

- **Primary:** Claude Code JSONL conversation logs (`~/.claude/projects/`)
- **Secondary:** Cascade/Devin session metadata (conversation content is server-side, not locally recoverable)
- **Corpus:** 12 ServiceNow project directories, Fluent SDK builds, customer engagements, Headroom context compression experiments

## Running the Extraction

```bash
python3 extract_session_patterns.py --verbose
python3 extract_session_patterns.py --project MyProject --verbose
python3 extract_session_patterns.py --output custom-report.md
```

## The Meta-Rule

> The agent is a tool, not a colleague. It does not have judgment, taste, or context awareness. Every output must be verified by the human before it leaves the pipeline.

---

*Built by Leo Francia. Extracted from real ServiceNow Fluent SDK delivery sessions, June 2026.*

---

<sup>[1]</sup> A custom orchestrator that routes to 84 domain-specialist sub-agents (ITSM, CSM, ITOM, HRSD, etc.) and executes against ServiceNow instances via MCP. Commercial equivalents in this emerging category include [EchelonAI](https://echelonai.com) and [Phyllis](https://phyllis.app), which connect AI agents directly to your instance for build and lifecycle operations. The anti-patterns documented here apply regardless of which orchestrator you use.
