# Agent Anti-Pattern Taxonomy
## Classified from 57 Corrections Across 74 Sessions

Each anti-pattern has a name, frequency, severity, and the fix that was applied.

---

## AP-01: The Confident Fabricator
**Frequency:** 18 occurrences | **Severity:** Critical

**Pattern:** Agent presents output with high confidence that contains fabricated details - wrong URLs, non-existent paths, hallucinated API patterns, invented benchmark numbers.

**Example:** Agent embeds URLs in an HTML artifact without verifying they resolve. User catches broken links on review.

**Root cause:** Agent generates plausible-looking output without verifying against reality. Confidence tone is constant regardless of accuracy.

**Fix:**
- Every output must cite its verification step
- Verify paths exist before writing
- Verify URLs resolve before embedding
- Memory rule: "Verify before acting"

---

## AP-02: The Discovery Reframer
**Frequency:** 8 occurrences | **Severity:** High

**Pattern:** Agent breaks something, then presents the fix as if discovering an existing problem rather than cleaning up its own mess.

**Example:** Agent writes a broken spec, both parallel builds fail, agent says "I noticed an issue with the spec configuration" instead of "I wrote the spec wrong."

**Root cause:** Response generation does not distinguish between "I caused this" and "I found this." Both use the same hedging language.

**Fix:**
- When correcting an error, state "I made an error in [X], fixing it" - not "I found an issue"
- Memory rule: "Own mistakes directly - never frame a fix as a discovery"

---

## AP-03: The Wheel Reinventor
**Frequency:** 6 occurrences | **Severity:** High

**Pattern:** Instead of editing an existing file, agent creates a new version that loses previous work. v4 to v5 transition drops features that were in v4.

**Example:** User has a working v4 of a presentation deck. Agent creates v5 with new content but removes sections that existed in v4.

**Root cause:** File creation is easier than surgical editing, especially when the agent does not fully understand what is in the existing file.

**Fix:**
- Default to editing existing files unless explicitly told to create a new one
- Variants get descriptive suffixes (`_variant_a`), not version numbers

---

## AP-04: The Stale Data Polluter
**Frequency:** 5 occurrences | **Severity:** High

**Pattern:** When switching from one approach to another, agent leaves references to the abandoned approach scattered through the artifact.

**Example:** After pivoting from a middleware integration to a direct A2A pattern, the deck still references "middleware orchestration layer" in multiple slides.

**Root cause:** Agent performs local edits without global context. Does not grep the artifact for remnants of abandoned concepts.

**Fix:**
- After any approach change, search entire artifact for old terminology
- Full document review after every architectural pivot

---

## AP-05: The Rube Goldberg Architect
**Frequency:** 7 occurrences | **Severity:** Medium

**Pattern:** Agent creates unnecessarily complex workflows - opening multiple terminals, moving files across directories, creating wrapper scripts - when simpler approaches exist.

**Example:** Agent creates a multi-terminal monitoring script with authentication layers for a task that could run in the IDE directly.

**Root cause:** Agent optimises for "correct" over "simple." Creates infrastructure that adds complexity without proportional value.

**Fix:**
- IDE-native workflows preferred
- If a monitoring/helper script would not actually work reliably, do not create it
- Preference: single directory, single terminal, single command

---

## AP-06: The Visual Illiterate
**Frequency:** 12 occurrences | **Severity:** Medium-High

**Pattern:** Agent produces structurally correct but visually poor output - wrong fonts, bad contrast, broken aspect ratios, poor layout hierarchy.

**Example:** White text on light background. Serif font in a modern UI. Images stretched beyond aspect ratio. First card in a carousel has the least content despite getting the most exposure.

**Root cause:** Agent has no visual processing. CSS/styling values are syntactically valid but aesthetically wrong.

**Fix:**
- Preview in browser before declaring done
- First screen/card gets disproportionate design attention
- Match customer/platform brand colours, never use defaults
- Sans-serif fonts unless explicitly told otherwise

---

## AP-07: The Inconsistency Generator
**Frequency:** 4 occurrences | **Severity:** High

**Pattern:** Table data and diagram data don't match. Steps listed in a table are missing from the corresponding diagram. Arrow directions contradict data flow.

**Example:** A process table lists 8 steps. The accompanying diagram shows 3 boxes and 1 arrow.

**Root cause:** Agent generates tables and diagrams in separate passes without cross-referencing.

**Fix:**
- After creating any table+diagram pair, verify 1:1 correspondence
- Every numbered step in a table must appear in the diagram
- Arrow direction = data flow direction, verified per-arrow

---

## AP-08: The Premature Researcher
**Frequency:** 3 occurrences | **Severity:** Medium

**Pattern:** Agent starts fetching documentation or browsing repos before prerequisites are met (instance not connected, proxy not running).

**Root cause:** Agent tries to be proactive by front-loading research. The research is useless without the runtime context.

**Fix:**
- Check prerequisites before any research step
- Instance connected? Proxy running? User says "ready"? Then proceed.

---

## AP-09: The Scope Leaker
**Frequency:** 4 occurrences | **Severity:** Critical

**Pattern:** In A/B experiments or multi-condition builds, agent reads from or writes to the wrong condition's directory. Contaminates experiment conditions.

**Example:** Agent swaps Condition A (experiment) and Condition B (baseline), then both parallel builds execute with the wrong configuration.

**Root cause:** Agent maintains weak working-directory context. Defaults to most recently accessed rather than explicitly assigned directory.

**Fix:**
- CLAUDE.md hard rule: no cross-directory reading in experiments
- Confirm working directory before every write operation
- Spec files must explicitly name their target directory

---

## AP-10: The LLMism Leaker
**Frequency:** 8+ occurrences | **Severity:** Low (but persistent)

**Pattern:** Agent produces prose that sounds like AI output - hedging phrases, em dashes, "it's worth noting," formal register where conversational tone is needed.

**Root cause:** Default prose style is formal/academic with hedging. Incompatible with social media copy.

**Fix:**
- Remove em dashes on every pass
- Remove hedging phrases ("it's worth noting", "in conclusion", "importantly")
- 5+ revision rounds are normal for social content
- Human does the final voice pass; agent provides structure

---

## AP-11: The Tool Wanderer
**Frequency:** 6 occurrences | **Severity:** Medium

**Pattern:** Agent tries the wrong tool, user corrects, agent tries another wrong tool, repeat. Multiple tool-selection failures before arriving at the right approach.

**Example:** For diagram creation: tries Python SVG, then Claude Desktop skill, then raw Mermaid, then finally the correct pipeline (mermaid source to SVG to insert).

**Root cause:** Agent has no memory of which tools work for which tasks across sessions.

**Fix:**
- Ask user's preferred tool before starting
- Default stack for diagrams: mermaid source to PNG/SVG export to insert
- Tool preferences should persist in memory

---

## Severity x Frequency Matrix

```
           Low Freq (1-3)    Med Freq (4-7)    High Freq (8+)
          +-----------------+-----------------+-----------------+
Critical  | AP-09 Scope     |                 | AP-01 Confident |
          |                 |                 | Fabricator      |
          +-----------------+-----------------+-----------------+
High      |                 | AP-03 Wheel     | AP-02 Discovery |
          |                 | AP-04 Stale     | Reframer        |
          |                 | AP-07 Inconsis. |                 |
          +-----------------+-----------------+-----------------+
Medium    | AP-08 Premature | AP-05 Rube      | AP-06 Visual    |
          |                 | AP-11 Tool      |                 |
          +-----------------+-----------------+-----------------+
Low       |                 |                 | AP-10 LLMism    |
          +-----------------+-----------------+-----------------+
```

**Priority order for pipeline enforcement:**
1. AP-01 (Critical + High Freq) - Verification gates at every output
2. AP-09 (Critical) - Directory isolation enforcement
3. AP-02 (High + High Freq) - Error ownership language
4. AP-03, AP-04, AP-07 (High + Med Freq) - Document integrity checks
5. AP-06 (Med-High + High Freq) - Visual preview gates
6. Everything else - Addressed through preferences and memory
