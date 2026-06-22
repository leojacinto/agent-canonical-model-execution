# ServiceNow Fluent SDK Delivery Pipeline
## Codified from 74 Claude Code & Cascade Sessions

---

## Pipeline Overview

```
IDEATION ──> SPEC ──> ARCHITECTURE ──> BUILD ──> VALIDATION ──> DOCUMENTATION ──> PRESENTATION
   │           │          │              │           │               │               │
   ▼           ▼          ▼              ▼           ▼               ▼               ▼
 Discovery   Deliverable Diagrams     Fluent SDK  SDK Install     Deliverable     + Demo HTML
 Notes       + Spec.md   + Flows      .now.ts     Playwright      + Briefing      Deck        
 Narratives  CLAUDE.md   OOB Mapping  Iteration   Data Check      Clickthrough    Social Card
```

---

## Phase 1: IDEATION & DISCOVERY

**What happens:** Raw inputs collected - discovery sessions, PDFs, DOCX, customer narratives, additional notes.

**Artifacts produced:**
- Discovery session notes (DOCX)
- Process step documents (PDF)
- `additional_notes.md` - freeform capture of questions, edge cases, business rules
- Stakeholder mapping (who owns what)

**Agent routing:** None yet - this is human work. Claude/Cascade used for *analysis* of inputs, not generation.

**Decision gate:** Do we have enough to write a spec?
- [ ] Process steps identified (even if incomplete)
- [ ] System boundaries known (SAP, RPA, spreadsheets, etc.)
- [ ] Pain points catalogued
- [ ] Client agency/department structure understood

**Known pitfalls:**
- Discovery notes are often scattered across formats - consolidate early
- Questions raised in discovery (e.g., "where is the counter source of truth?") become spec gaps if not resolved
- Bot/RPA details are often vague - push for specifics on what the bot actually does vs. what it is supposed to do

---

## Phase 2: SPEC CREATION

**What happens:** Transform discovery into structured architecture document + per-build spec files.

**Artifacts produced:**
- Architecture deliverable (as-is/to-be)
- `spec.md` (per build directory) - scoped build instructions for the agent
- `CLAUDE.md` - hard rules and constraints for agent behavior
- Mermaid diagrams (`diagrams/*.mmd` to `diagrams/*.png`)
- `generic/` variant - anonymised version for reuse

**Agent routing:**
- Claude Code (primary) for deliverable drafting
- Cascade for diagram generation and HTML rendering
- SN orchestrator<sup>[1]</sup> for engagement analysis, product mapping, OOB feature identification, and build approach recommendation. The orchestrator can also configure and build directly via MCP - in this pipeline it operates in advisory mode during early phases and shifts to execution mode from Phase 4 onward.

**Decision gate:** Architecture approval before build begins.
- [ ] Deliverable covers as-is + to-be
- [ ] Diagrams exported (Mermaid source + PNG)
- [ ] spec.md written per build condition
- [ ] CLAUDE.md hard rules defined (Fluent only? MCP allowed? REST for config only?)
- [ ] Component mapping done (CSM tables, PSDS flows, etc.)

**Known pitfalls:**
- Deliverable scope creep - keep it to what matters for the build
- Diagram versioning: `diagram_1.mmd`, `diagram_1a.mmd` - use suffixes for variants, not separate numbering
- Generic/anonymised version should be created alongside, not after
- `spec.md` must be agent-readable: structured, no ambiguity, explicit about what to create vs. what exists

---

## Phase 3: ARCHITECTURE & FLOW MAPPING

**What happens:** Map customer processes to ServiceNow capabilities. Identify which OOB flows, tables, and modules to use.

**Artifacts produced:**
- Flow mapping (customer step to SN capability to implementation approach)
- Table/module selection (CSM cases, PSDS, custom scoped tables)
- Agent specialist selection (which orchestrator agents activate)
- Build approach decision: Fluent SDK vs. MCP vs. manual

**Agent routing:**
- SN orchestrator (UNDERSTAND phase) - parse request, detect engagement type
- Claude Code with `now-sdk-explain` skill - for Fluent SDK patterns
- Specialist agents as needed (CSM, ITSM, ITOM, etc.)

**Decision gate:** Build approach locked.
- [ ] Tables identified (extend OOB vs. custom scoped)
- [ ] Flows mapped (which SN flows handle which process steps)
- [ ] Build tool decided (Fluent SDK `.now.ts` vs. MCP vs. hybrid)
- [ ] Conditions defined (if running comparison experiments)

**Known pitfalls:**
- CSM vs PSDS decision matters early - they have different table structures
- Fluent SDK has no existing PSDS/CSM reference repos - conversion is new work every time
- Do not assume OOB flows exist for every customer process step - some need custom flows
- `now-sdk-explain` is demand-driven, not a pre-loaded context dump

---

## Phase 4: BUILD / EXECUTION

**What happens:** Agents execute the build. This is where most session time is spent.

**Artifacts produced:**
- Fluent SDK repo structure (`src/fluent/tables/`, `src/fluent/flows/`, etc.)
- `now.config.json` - scoped app configuration
- `.now.ts` files - table definitions, business rules, flows
- MCP-created artifacts (if not Fluent): records, flows, UI pages via ServiceNow MCP

**Agent routing:**
- **Fluent path:** Claude Code with `now-sdk-explain` skill, working in scoped directory
- **MCP path:** SN orchestrator dispatching specialist agents with ServiceNow MCP tools
- **Hybrid:** Architecture in Claude Code, execution via MCP (common for demos)

**Build loop:**
```
1. Agent reads spec.md + CLAUDE.md
2. Agent reads memory files (project context, user preferences, feedback)
3. Agent scaffolds structure
4. Agent creates artifacts iteratively
5. User reviews, corrects, redirects
6. Agent incorporates corrections
7. Repeat 4-6 until build complete
```

**Decision gate:** Build complete enough for validation.
- [ ] All spec items addressed
- [ ] No placeholder/stub code remaining
- [ ] SDK install succeeds (`npx @servicenow/sdk install`)
- [ ] Data model matches architecture diagrams

**Known pitfalls (high value - mined from sessions):**
- **Path verification:** Agent assumes paths exist that don't - always verify before acting
- **Cross-directory contamination:** Build conditions must stay in their own subdirectory
- **SDK documentation gaps:** Agent may hallucinate Fluent API patterns - use `now-sdk-explain` to verify
- **Memory staleness:** Memory files from prior sessions may reference outdated decisions
- **Bot simulation traps:** When replacing RPA, do not replicate bot logic - reimagine the workflow
- **Scope discipline:** Constraints vary per project - enforce via CLAUDE.md
- **Recursive correction loops:** Agent fixates on literal word interpretation - redirect with intent
- **Instance connectivity:** Do not research SDK docs until instance is connected and ready

---

## Phase 5: VALIDATION

**What happens:** Verify the build works. Playwright for UI, SDK install for artifacts, manual spot-checks.

**Artifacts produced:**
- Playwright test results
- Demo readiness checklist (no empty screens, connected data)
- Regression test suite (if applicable)

**Agent routing:**
- SN orchestrator (BUILD phase) - Demo Readiness Check
- Playwright MCP for browser-based validation
- Manual review by SE

**Decision gate:** Demo-ready.
- [ ] SDK install clean
- [ ] Key workflows testable end-to-end
- [ ] No empty dashboards / missing data
- [ ] Playwright screenshots captured

**Known pitfalls:**
- ServiceNow shadow DOM breaks standard selectors
- SSO/CSP/session timeout issues with Playwright against SN instances
- Demo data must be realistic - not "Test Incident 1"

---

## Phase 6: DOCUMENTATION

**What happens:** Generate stakeholder-facing deliverables from the build.

**Artifacts produced:**
- Architecture deliverable (final version)
- Demo Clickthrough HTML
- Executive Briefing HTML
- Update sets (XML, if MCP path)
- Archive folder (session logs, scan results, manifests)

**Agent routing:**
- Claude Code / Cascade for HTML generation
- SN orchestrator (FINALIZE phase) - auto-generates Clickthrough + Briefing
- Mermaid to PNG pipeline for final diagrams

**Decision gate:** Deliverable complete.
- [ ] Deliverable final
- [ ] HTML renders correctly (test in browser)
- [ ] All diagrams current
- [ ] Archive contains session artifacts

**Known pitfalls:**
- HTML rendering: always preview in browser, not just markdown preview
- Diagram exports: PNG must match latest Mermaid source (easy to get out of sync)
- Archive naming: use ISO timestamps for versioning

---

## Phase 7: PRESENTATION / SOCIAL

**What happens:** Package for external consumption - social cards, GIFs, shareable demos.

**Artifacts produced:**
- Social card images
- Comparison GIFs
- Interactive HTML demos
- LinkedIn/internal post content

**Agent routing:**
- Cascade for visual generation and HTML interactives
- Claude Code for content drafting

---

## Cross-Cutting Concerns

### Memory System
- Per-project memory files track context, preferences, and corrections
- Memory carries between sessions but can go stale - validate on resume
- Feedback files capture correction patterns that become permanent rules

### Agent Routing Decision Tree

```
Does the task touch a ServiceNow instance?
|
+-- YES: Is an SN orchestrator connected?
|   |
|   +-- YES: Use the orchestrator.
|   |   It can plan, build, configure, validate, and document.
|   |   Claude Code / Cascade assist for:
|   |     - Local file generation (Fluent SDK .now.ts files)
|   |     - Non-SN artifacts (deliverables, diagrams, social cards)
|   |     - Tasks the orchestrator cannot reach (local filesystem, non-SN APIs)
|   |
|   +-- NO: Use Claude Code + now-sdk-explain + ServiceNowDocs repo.
|       Manual instance configuration or Fluent SDK side-loading.
|
+-- NO: Use Claude Code / Cascade directly.
    Documentation, analysis, diagrams, HTML, social content.
```

### Multi-Tool Routing
| Scenario | Primary Tool | Fallback |
|----------|-------------|----------|
| Demo build (fast) | SN orchestrator + MCP | Manual SN config |
| Scoped app (Fluent) | Claude Code + now-sdk-explain | SDK docs via WebFetch |
| Architecture docs | Claude Code | Cascade |
| Diagrams | Claude Code (Mermaid) | Cascade |
| HTML deliverables | Cascade | Claude Code |
| Browser testing | Playwright MCP | Manual |

### Fluent SDK Project Structure
```
project-root/
├── CLAUDE.md                    # Hard rules for agents
├── spec.md                      # Build specification
├── additional_notes.md          # Freeform context
├── *-Deliverable.md             # Architecture doc
├── *-Architecture.html          # Rendered version
├── diagrams/
│   ├── diagram_N.mmd           # Mermaid source
│   ├── diagram_N.png           # Exported PNG
│   └── diagram_Na.mmd          # Variant
├── generic/                     # Anonymised version
├── archive/                     # Versioned snapshots
└── [build-dir]/                 # Per-condition build
    ├── now.config.json
    └── src/fluent/
        ├── tables/*.now.ts
        ├── flows/*.now.ts
        └── ...
```

### Context Compression (Headroom)

One experiment tested [Headroom](https://github.com/chopratejas/headroom), a context compression utility, against a baseline Fluent SDK build. The setup: same spec, same model, two conditions. Full experiment: [leojacinto/headroom-experiment](https://github.com/leojacinto/headroom-experiment).

**Finding:** Minimal quality difference between compressed and uncompressed contexts for Fluent SDK builds. The Fluent SDK output is primarily new code generation (`.now.ts` files), not refactoring existing code, so context compression has limited leverage.

**But:** The experiment itself generated the most anti-patterns in the corpus (18 corrections, 5 restart cycles). The tooling around running parallel A/B experiments with AI agents is where the real lessons were - see `session-case-studies.md` for the full narrative.

### Monorepo Context Priming (Project Moreau)

A separate experiment tested whether giving an AI build agent access to an existing codebase (monorepo) produces better ServiceNow apps. Full experiment: [leojacinto/project-moreau-test](https://github.com/leojacinto/project-moreau-test).

**Finding:** When the monorepo contains a close match to the target use case, the agent produces DRYer code with better reuse. When there is no close match, the monorepo introduces noise. Context priming helps for similar use cases and hurts for novel ones.

---

## Data Sources

| Source | Format | Coverage |
|--------|--------|----------|
| Claude Code sessions | JSONL | 74 sessions, full conversation history |
| Cascade/Devin sessions | SQLite metadata | Session IDs only - content is server-side |

---

*Pipeline version: 1.0 - June 2026. Extracted from 74 sessions across 12 ServiceNow project directories.*

---

<sup>[1]</sup> **What is an SN orchestrator?** A multi-agent system purpose-built for ServiceNow that can plan, build, configure, validate, and document against a live instance. Typical capabilities include: domain-specialist agent routing (ITSM, CSM, ITOM, HRSD, etc.), instance profiling, OOB feature intelligence, license-aware design, MCP-based execution, and browser-validated deliverables. This pipeline was developed using an internal orchestrator but is designed to be orchestrator-agnostic. Commercial alternatives include [Phyllis](https://phyllis.app) and [EchelonAI](https://echelonai.com). If you do not have an SN orchestrator, the pipeline still works - Claude Code / Cascade handle the build via Fluent SDK, and you configure the instance manually or via REST.
