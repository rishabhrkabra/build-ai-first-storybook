# Quality gates

## Contents

1. Per-component gates
2. Foundation migration gates
3. Visual QA
4. Release gates
5. CI layers
6. Health metrics

## Per-component gates

Require:

- strict types and public export validation;
- unit tests for state and data logic;
- interaction tests for keyboard, pointer, focus, forms, and controlled use;
- accessibility checks;
- responsive boundary stories;
- provenance and contract completeness;
- production Storybook build;
- visual comparison to authoritative references.

Mark the item `review` until the required gates for its capabilities and scope
pass. For maintenance, run affected checks and dependency tests; full release
gates apply when releasing, not automatically to every documentation edit.

Report schema validation, repository-policy coverage, package/build tests,
browser behavior, visual acceptance and deployed verification separately.
`validate.py` checks metadata, evidence paths, hashes and optional configured
repository policy. It does not execute the tests named in a receipt, authenticate
an approver, certify semantic quality or replace a clean consumer build.

## Foundation migration gates

When changed foundations affect production component families, require a scoped foundation packet that:

- inventories the old and proposed contracts across color, type, spacing, radius, elevation, icons, motion, responsive behavior, and content where applicable;
- states which rules change, remain, or need an owner decision;
- shows every material change as foundation → component → production module → full-screen before/after evidence;
- uses the same state and viewport for comparisons;
- identifies which downstream differences should update automatically and which require component work;
- records visual, contract, lifecycle, adoption, and branch/PR authorization as separate gates.

A token table or isolated component story cannot pass this gate by itself.

## Rendered-page contracts

A class of defect can escape source-only checks: the markup is correct, the
classes resolve, the tokens are right, types pass and unit tests are green,
because the defect lives in the relationship between two files rather than in
either one. A jsdom test cannot see it either, since jsdom has no layout.

Run a small set of invariant-shaped assertions against the real page in a real
browser, at the agreed widths:

- controls intended to operate in the active interaction region are operable,
  focusable where appropriate, and exposed with the expected accessible names;
- modal background controls are excluded from interaction while the modal's own
  controls remain operable; focus returns to the appropriate location on close;
- nothing scrolls sideways unless it declares that it means to;
- control sizes/alignment match the row's declared contract, including legitimate
  mixed-size icon actions and multiline fields;
- essential truncated content remains available through the component's approved
  keyboard, pointer and touch disclosure behavior.

Two properties keep this class honest.

**Key each assertion on what the reader can perceive, never on which element
carries the attribute.** A visible decorative icon can correctly be `aria-hidden`;
a dimmed background can correctly be inert. Do not disable modal behavior or
remove decorative hiding to satisfy a blanket scanner. Test legitimate cases
as positive controls as well as sabotaged active controls as negative controls.
See [WAI modal semantics](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
and [aria-hidden guidance](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden).

**Make "could not run" a failure with its own message.** A scan that stands down
for a legitimate reason — a modal is open, so the page behind it is correctly
inert — must not report that as nothing wrong. And where a case depends on
reaching a state, assert the state was reached before asserting anything about
it, or the case passes without exercising the thing it is named for.

Sabotage-test these guards: reintroduce the defect, watch it fail, restore.
Assert state setup explicitly; a missing route or unopened overlay must not
produce an empty passing scan. Explicitly inapplicable cases are not failures,
but cannot count as executed coverage for a required state.

## Visual QA

For composed screens, also run [composition-contracts.md](composition-contracts.md)
and its measured relationship checks. Token/component validity cannot certify
peer-card heights, helper ownership, local action alignment or state paint.

For each important state:

1. Capture the authoritative reference.
2. Render at the same viewport or container size.
3. Place reference and implementation in one comparison surface.
4. Inspect geometry, typography, color, stroke, shadow, asset, truncation, and overflow.
5. Fix differences.
6. Repeat until accepted.

Do not use screenshot presence as proof. Store viewport, state, source node/version, and expected behavior with each baseline.

**Readable-scale inspection is required before handoff** (owner correction,
2026-09-24). Actually view the final rendered artifact. A zoomed-out overview
cannot certify labels, wrapping or clipping: inspect dense sections at 100%
logical size or readable close-up, including the longest content, status/metric
labels and review-board scaffolding. Use the actual background. Record inspected
regions, scale and findings; recheck repaired regions. If the rendering cannot
be read or viewed, report it unverified rather than declaring visual completion.
This applies to Figma boards, Storybook and live UI. Pair the visual inspection
with text-fit/relationship checks; box bounds alone can miss text painting
outside fixed-height containers. No extra capture is needed for unchanged,
already inspected evidence.

Test resize behavior, not only static widths. Verify the rules between fixtures.

### Labelled comparison integrity

When presenting A/B candidates or current/proposed values, the caption is a
testable claim about the compared properties—not proof those properties changed.
Before editing, list each targeted node/property (including text ranges and
nested-instance paints), its expected value per candidate, and explicit unchanged
context. A global colour heading must not silently describe an icon-only change;
name isolated-property experiments plainly. Do not broaden their scope merely to
make a checker pass.

After the final write, read the complete target list back from the native/runtime
artifact. Resolve aliases/overrides, check exact values, opacity and visibility,
require nonzero expected coverage, and match corresponding targets between
candidates. A changed-paint count, a valid token graph or identical geometry
cannot establish comparison correctness. Missing targets are failures, not
filtered-out successes. Inspect the changed context at readable scale as well.

Test the check against an identical-candidate mistake and a missing target, plus
a legitimate unchanged primary label. If the values or scope fail, correct the
artifact/caption and retain the failed receipt before claiming verification.
This gate checks labelled comparisons, not permission to recolour source screens
or to merge tokens.

## Release gates

Before publishing:

- registry has no duplicate IDs, names, or story IDs;
- every ready record has source, styles, types, docs, stories, tests, authority, responsive, and accessibility contracts;
- public API is a subset of inventory (equality is valid when everything is public);
- all local and hosted links resolve;
- static assets use authoritative files;
- no prohibited or unofficial theme leaks into canonical output;
- version and source revision match the deployed build;
- checksums match hosted artifacts;
- migration notes cover every breaking contract change;
- hosted AI endpoints return the new release;
- a fresh-agent smoke test succeeds without hidden project history;
- a clean environment can consume through the project's documented authorized interface, whether package, hosted or local;
- distributable artifact scanning finds no secret, restricted, or unapproved files.

## CI layers

Use one tool per job:

- schema/link validator for machine contracts;
- framework type checker;
- unit and interaction runner;
- accessibility runner;
- Storybook production build;
- browser-based visual regression at pinned project browser/OS/font fixtures;
- optional hosted review service for stakeholder approval.

Avoid overlapping visual-regression vendors. Keep local deterministic baselines even when using a hosted review layer.

## Health metrics

Track:

- ready versus review versus inventory-only counts;
- undocumented ready components;
- ready components without interaction tests;
- recipes without responsive fixtures;
- unresolved decisions and their age;
- active exceptions and their age or expired owner;
- repeated clones, local restyles, and component candidates awaiting semantic review;
- duplicate component families;
- hosted endpoint freshness;
- visual-regression failures;
- temporary migration-review stories whose delete condition is satisfied;
- agent tasks that required local restyling or component cloning.

The last metric is especially useful: repeated application-level fixes usually reveal a missing global rule or incomplete component contract.
