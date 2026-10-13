# Composition relationships — cross-surface generation gate

Owner-adopted default, 24 September 2026. Applies to Figma, Storybook and live
UI work. These checks supplement component/token checks; correct isolated
components can still form a broken page.

## Conditional rules

- **Peer cards.** When comparable cards share a row, use equal outer heights
  and aligned action footers, determined by the largest supported content.
  Avoid independent hugging heights or clipping text to fake equality. This
  supports scanning and comparison. Deliberate masonry/editorial feeds are the
  exception, not an accidental default. Stacked cards need not share a height.
- **Field ownership.** When a helper/status/error belongs to one field, nest
  label, control and helper in one group. Its control-to-helper gap must be
  smaller than the gap to the next field. Avoid orphan messages at equal gaps.
  Form-wide summaries are an explicit exception. Use project spacing tokens,
  not universal hardcoded 8/24 values.
- **Action rows.** Related sibling buttons follow a declared shared size and
  alignment. A smaller icon action may be intentional and centred; an embedded
  compact action is not automatically appropriate outside its control. Measure
  the relationship, not just each button's valid variant.
- **Repeated management.** Keep the primary task visible. When cards repeat
  several occasional management actions, propose a per-card contextual menu;
  preserve names, capabilities, discovery and accessibility. Frequent essential
  actions may remain exposed. No universal maximum button count, and no claim
  that fewer buttons by itself proves a faster decision.
- **Affordance and state.** Follow the project's URL-only icon convention,
  without applying it to mixed/file/free-text inputs. After an icon swap, verify
  its resolved semantic foreground AND state background, plus final stroke.
  Generic icon colour must not erase selected/error/disabled semantics.

## Required evidence at handoff

Record current source IDs, viewport/container widths and inspected subjects.
At source, mid and declared minimum widths, check same-row heights/footer
baselines, action centres/sizes, helper proximity and ancestor membership,
resolved state colour, URL affordances, horizontal AND vertical overflow,
sibling overlaps, clipping and content bounds inside component instances.
Inspect the longest current copy and a changed-copy case when the task includes
content growth. Report untested arbitrary copy/mobile/runtime separately.

Figma FILL children inside a wrapping HUG row can shrink to an invalid height.
Protect content minima and let ancestors grow; then measure the placed consumer.
A pixel minimum is scoped to that content contract, not a global card-height
token. Content or breakpoint changes require renewed measurement. Do not infer
responsive success from Auto Layout labels alone.

Use `scripts/validate_composition.py` with measured observations. It is a
portable relationship checker, not a Figma connection or browser crawler.
The collector must identify the actual subjects and all relevant observations;
missing subjects and zero checks are failures. Geometric checks do not replace
visual review, accessibility or runtime interaction tests. Run a negative
fixture that reproduces each repaired defect and a legitimate positive case.
Unresolved required failures block a completion claim.
