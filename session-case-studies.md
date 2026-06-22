# Session Case Studies
## What Actually Happened in the 3 Highest-Signal Sessions

---

## Case Study 1: The Headroom Experiment
**Project:** Government Debt Management | **Repo:** [leojacinto/headroom-experiment](https://github.com/leojacinto/headroom-experiment)  
**Scope:** 2606 lines | 18 corrections | 2 decisions  

### Objective

Build the same ServiceNow Debt Management app twice using Fluent SDK. Condition A gets Headroom (a context compression tool). Condition B is baseline. Compare token cost and artifact quality.

### What Went Right

**Architecture phase (0 corrections):** Agent reads memory files, whitepaper, and additional notes. Maps CSM/PSDS flows to debt management steps. Identifies which OOB tables to reuse. Clean, structured, data-driven work.

**Experiment design:** User drives key decisions. Agent adjusts. "Can we just have Condition A ignore headroom? What is the point of having headroom compress available if it does not call it?" - valid design question, properly handled.

**Social content strategy:** User applies cross-project learning: "I led with the experimental group [in a prior project]. It gained abysmal engagement because I did not start with the hype finding." Agent incorporates this into the card design.

### What Went Wrong

**Spec generation (catastrophe):** Agent writes spec files for both conditions. Both contain errors. User triggers both in parallel in separate Claude Code sessions. Both parallel builds execute broken specs. Hours of compute wasted.

**The recursion loop:** After the reset, five restart cycles:
1. Start measurement is wrong - agent did not establish clean baseline
2. Condition A does not actually invoke Headroom
3. Monitor build script is non-functional
4. Terminal management adds friction instead of reducing it
5. Agent presents each fix with the same confidence that produced the original error

**The meta-correction:** User identifies the root pattern: the agent presents fixes to its own errors as new discoveries rather than owning the mistake. This becomes a permanent memory rule.

### Outcome

Both conditions eventually run. Finding: "It does not look like there is significant difference given the progress. Which is fine. That is why we experiment." The experiment succeeds despite the tooling failures. Social card and LinkedIn post are produced after 8+ revision rounds.

### Rules Generated
- Spec review before parallel launch - never start parallel builds until specs are verified
- Clean baseline verification - measurement must start verified at zero
- Admit errors immediately - "I broke this" not "I discovered an issue"
- Monitor scripts must work or should not exist - false safety nets are worse than none
- IDE-native workflows only - do not force terminal workflows

---

## Case Study 2: The Integration Deck
**Project:** Customer Engagement  
**Scope:** 1159 lines | 12 corrections | 11 decisions  

### Objective

Build a PowerPoint deck presenting 4 integration options for SAP-ServiceNow offboarding workflows. Each option needs a table AND a diagram.

### What Went Right

**Content architecture:** Agent creates 4 integration options: direct API, middleware, orchestration layer, agent-to-agent (A2A). User drives architecture with sharp questions: "Should Option 4 lead with the policy angle - least surface area, strongest policy position?" Decision-making quality is high.

### What Went Wrong

**Version control:** Agent creates v4. Then creates v5 that removes features from v4 instead of updating it. User catches the regression. Agent does it again on the next revision.

**Stale data contamination:** After pivoting from middleware to A2A for Option 4, middleware references remain scattered through the Option 4 content. Agent then contradicts itself about whether a specific concern is relevant, editing it in and out across passes.

**The diagram saga (6 tool failures):**
1. Python SVG generation - wrong tool choice
2. Claude Desktop diagram skill - wrong tool
3. Raw Mermaid - user did not request this format
4. PPT native shapes - poor quality output
5. Multiple mermaid variants with wrong styling
6. Finally: mermaid source to SVG to PPT insert - works but every diagram needs manual correction for fonts (serif instead of sans-serif), colours (dark text on dark background), layout (vertical instead of horizontal swimlanes), arrow directions (one-way for bidirectional processes), and table-to-chart consistency.

**Full deck review never happened:** User repeatedly asks agent to review the entire deck. Agent performs local edits only. Stale entries persist across slides.

### Outcome

Deck is eventually completed with all options and diagrams, but required significant manual correction on visual elements and consistency.

### Rules Generated
- Default: edit existing file, never create new versions
- Full deck/document review after every edit, not just the changed section
- After any approach change, grep entire artifact for old terminology
- Ask user's preferred diagram tool before starting
- Visual checklist: font family, colour contrast, aspect ratio, arrow directions, table-to-chart consistency
- Use customer/platform brand colours, never use defaults

---

## Case Study 3: The Controlled Comparison
**Project:** Project Moreau | **Repo:** [leojacinto/project-moreau-test](https://github.com/leojacinto/project-moreau-test)  
**Scope:** 1062 lines | 12 corrections | 8 decisions  

### Objective

Scientific comparison: does giving an AI build agent access to an existing codebase (monorepo) make it produce better code? Two conditions, two ServiceNow apps (Travel, Equipment MDM), same spec.

### What Went Right (Analysis Phase - 0 corrections)

This is the model for good agent interaction:
- User provides data
- Agent analyses (ACLs, business rules, data model comparisons)
- User asks pointed questions: "Did the spec actually help in creating DRY? Or is there a chance that is just coincidence?"
- Agent responds with evidence
- User synthesises the insight

Key findings emerged from this structured dialogue:
- "It is almost having a test whether the same use case exists. If there is no match, ditch the monorepo."
- Travel (exact reference in monorepo) benefited. Equipment MDM (no exact match) showed noise from irrelevant reference code.
- Context-primed builds were more expensive in tokens but not necessarily better in quality for novel use cases.

### What Went Wrong (Social Phase)

All 12 corrections appear in the social content creation phase:
- GIF dimensions, frame timing, colour scheme
- LinkedIn post copy: 8 rounds of revision to remove AI-sounding language
- Platform constraints the agent did not know (LinkedIn has no title field)
- Competitive sensitivity: "Do not add inputs which can be screenshot by competitors"
- External timing: awareness of industry events that affect posting timing

### Outcome

Published to GitHub with README, comparison GIF, and LinkedIn post. The analysis was solid. The packaging required extensive human iteration.

### The Lesson

**Agents excel at structured analysis and fail at aesthetic judgment.** The pipeline should route accordingly. Data retrieval, structured comparison, and evidence synthesis are agent strengths. Visual design, copy voice, and platform-aware content creation require human iteration.

---

## Cross-Session Patterns

### The Frustration Escalation Curve

Every high-correction session follows the same pattern:

```
1. Polite redirection     - "Can we do X instead?"
2. Firm correction        - "I said X. Do X."
3. Pointed feedback       - "Check the artifact first and stop guessing"
4. Explicit rule          - "Stop presenting fixes to your own errors as discoveries"
5. Permanent guardrail    - Memory file or CLAUDE.md rule created
```

Step 4 is where the transferable rule is articulated. Step 5 is where it becomes permanent.

### Time Sink Distribution

| Activity | % of correction time | Root cause |
|----------|---------------------|------------|
| Spec/config errors cascading into parallel builds | 35% | Agent did not verify before launch |
| Visual formatting (fonts, colours, layout) | 25% | Agent has no visual judgment |
| Stale data from abandoned approaches | 15% | Agent does not scrub after pivots |
| Version management confusion | 10% | Agent creates instead of updates |
| Tool selection failures | 10% | Agent does not ask preference |
| False confidence masking errors | 5% | Agent presents fixes as discoveries |

### The Session That Went Right

The Project Moreau analysis phase is the template:
- User provides data, agent analyses, user asks pointed questions, agent responds with evidence, user synthesises the insight
- Zero corrections in the analysis phase
- Agent stays in its lane (data retrieval + structured comparison)
- All corrections appear only when shifting to creative/visual work

**The lesson:** Agents excel at structured analysis and fail at aesthetic judgment. The pipeline should route accordingly.
