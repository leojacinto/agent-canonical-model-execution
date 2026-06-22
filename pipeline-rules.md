# Pipeline Rules
## 12 Rules Distilled from 57 Corrections and 24 Decision Points

Each rule corresponds to a real failure that cost time.

---

## Rule 1: VERIFY BEFORE ACTING

Never assume a path, URL, file, or configuration exists. Check first.

**Pipeline checkpoint:** At every build step, agent must verify:
- [ ] Target paths exist before writing
- [ ] URLs resolve before embedding
- [ ] Instance is connected before querying
- [ ] Prior artifacts exist before referencing

---

## Rule 2: OWN YOUR MISTAKES

Never present a fix to something you broke as a "discovery" or "improvement."

**Pipeline checkpoint:**
- [ ] When correcting an error, state "I made an error in [X], fixing it"
- [ ] Track which agent/session introduced the error

---

## Rule 3: UPDATE, DON'T OVERWRITE

Never create v2/v3/v5 when you should update v1. Never reinvent when you should patch.

**Pipeline checkpoint:**
- [ ] Before creating a new version, confirm: is this a new variant or an update?
- [ ] Default to editing existing file unless explicitly told to create a new one
- [ ] If creating a variant, clearly name it (e.g., `_variant_a`, not `_v2`)

---

## Rule 4: VISUAL QUALITY IS NOT OPTIONAL

HTML/PPT output must be visually verified, not just structurally correct.

**Pipeline checkpoint:**
- [ ] Preview HTML in browser before declaring done
- [ ] Check font readability, contrast, aspect ratios
- [ ] First screen/card gets the most attention - design accordingly
- [ ] No fade-in animations in GIF loops

---

## Rule 5: TABLE AND DIAGRAM MUST MATCH

If you show data in a table AND a diagram, they must correspond exactly.

**Pipeline checkpoint:**
- [ ] After creating tables, verify diagrams reflect the same data
- [ ] Diagrams must show bidirectional flows where bidirectional processes exist
- [ ] Use swimlanes for multi-system interactions

---

## Rule 6: DON'T RESEARCH UNTIL READY

No SDK docs browsing, repo exploration, or API research until prerequisites are met.

**Pipeline checkpoint:**
- [ ] Instance connected and accessible? Then research.
- [ ] SDK proxy running? Then explore Fluent docs.
- [ ] User says "ready"? Then proceed.
- [ ] Never pre-fetch docs "just in case"

---

## Rule 7: SCOPE DISCIPLINE

Each build condition is isolated. No cross-reading, no cross-contamination.

**Pipeline checkpoint:**
- [ ] Confirm which directory you are working in before every write
- [ ] Never read from a sibling condition's directory
- [ ] If experiment has conditions A/B, never merge their artifacts

---

## Rule 8: SOCIAL CONTENT IS ITERATIVE

Social post copy requires 5-8 revision rounds. Budget for it.

**Pipeline checkpoint:**
- [ ] First draft is never final - expect 5+ rounds
- [ ] Remove LLMisms on every pass (hedging, "it's worth noting", "in conclusion")
- [ ] Verify platform constraints (LinkedIn char limits, image dimensions)
- [ ] Check timing sensitivity before publishing
- [ ] Cross-check claims against source data

---

## Rule 9: DIAGRAMS ARE NOT DECORATIONS

Diagrams must convey accurate, detailed process flows.

**Pipeline checkpoint:**
- [ ] Every process step in the spec must appear in the diagram
- [ ] Arrow directions must match data flow direction
- [ ] Use swimlanes for multi-system interactions
- [ ] If there are 8 steps, show 8 steps

---

## Rule 10: BROWSER TESTING HAS UNIQUE FAILURE MODES

Browser testing against ServiceNow requires specific handling.

**Pipeline checkpoint:**
- [ ] Check for existing browser instances before launching new ones
- [ ] Handle ServiceNow shadow DOM with correct selectors
- [ ] Account for SSO redirects and session timeouts
- [ ] Screenshots are evidence - save them

---

## Rule 11: SPECIFY THE CAPTURE, DON'T LET THE AGENT GUESS

HTML-to-GIF/screenshot capture is a recurring task. Agents will write a working script every time, but waste tokens reinventing dimensions, FPS, crop regions, and loop points from scratch.

**Pipeline checkpoint:**
- [ ] Provide exact spec before the agent writes the script: dimensions, FPS, duration, crop region, loop point
- [ ] Specify output format (GIF, MP4, PNG sequence)
- [ ] State the tool chain: Playwright + ffmpeg, or alternative
- [ ] If looping, define the clean loop cut point (where the animation resets seamlessly)
- [ ] Do not let the agent pick defaults  -  every project has different requirements

---

## Rule 12: PPTX AND DOCUMENT BRAND COMPLIANCE

Agents generate structurally correct documents with wrong fonts, wrong colours, and broken icons. This is not a one-time fix  -  it happens every time.

**Pipeline checkpoint:**
- [ ] After any PPTX generation, audit fonts and map to brand fonts (e.g. Calibri to ServiceNow Sans)
- [ ] Verify icon fidelity  -  icons must match the source, not be approximations
- [ ] Check colour values against brand palette, not agent defaults
- [ ] For DOCX/HTML, verify heading hierarchy, brand colours, and page dimensions
- [ ] Run the audit as a separate step  -  do not trust the agent's self-assessment of visual quality

---

## The Meta-Rule

> The agent is a tool, not a colleague. It does not have judgment, taste, or context awareness. Every output must be verified by the human before it leaves the pipeline.

The corrections cluster around a consistent theme: the agent produces structurally correct but qualitatively poor output, then presents it with false confidence. The pipeline must enforce verification gates at every phase transition.
