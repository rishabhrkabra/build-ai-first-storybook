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

Mark the item `review` until every required gate passes.

## Foundation migration gates

Before migrating production component families, require one foundation packet that:

- inventories the old and proposed contracts across color, type, spacing, radius, elevation, icons, motion, responsive behavior, and content where applicable;
- states which rules change, remain, or need an owner decision;
- shows every material change as foundation → component → production module → full-screen before/after evidence;
- uses the same state and viewport for comparisons;
- identifies which downstream differences should update automatically and which require component work;
- records visual, contract, lifecycle, adoption, and branch/PR authorization as separate gates.

A token table or isolated component story cannot pass this gate by itself.

## Rendered-page contracts

A class of defect is invisible to every check above: the markup is correct, the
classes resolve, the tokens are right, types pass and unit tests are green,
because the defect lives in the relationship between two files rather than in
either one. A jsdom test cannot see it either, since jsdom has no layout.

Run a small set of invariant-shaped assertions against the real page in a real
browser, at the agreed widths:

- no element a reader can see sits inside an `inert` or `aria-hidden` subtree;
- nothing scrolls sideways unless it declares that it means to;
- the controls in one row share one height;
- text that is clipped reveals itself on hover and focus.

Two properties keep this class honest.

**Key each assertion on what the reader can perceive, never on which element
carries the attribute.** "The canvas wrapper is inert" is a description of
today's markup; "nothing visible is inert" survives the next refactor and fails
it if it regresses.

**Make "could not run" a failure with its own message.** A scan that stands down
for a legitimate reason — a modal is open, so the page behind it is correctly
inert — must not report that as nothing wrong. And where a case depends on
reaching a state, assert the state was reached before asserting anything about
it, or the case passes without exercising the thing it is named for.

Sabotage-test every one of these: reintroduce the defect, watch it fail,
restore. Two of the four above passed on the exact bug they were written for
until they were run against it.

## Visual QA

For each important state:

1. Capture the authoritative reference.
2. Render at the same viewport or container size.
3. Place reference and implementation in one comparison surface.
4. Inspect geometry, typography, color, stroke, shadow, asset, truncation, and overflow.
5. Fix differences.
6. Repeat until accepted.

Do not use screenshot presence as proof. Store viewport, state, source node/version, and expected behavior with each baseline.

Test resize behavior, not only static widths. Verify the rules between fixtures.

## Release gates

Before publishing:

- registry has no duplicate IDs, names, or story IDs;
- every ready record has source, styles, types, docs, stories, tests, authority, responsive, and accessibility contracts;
- public API is a strict subset of inventory;
- all local and hosted links resolve;
- static assets use authoritative files;
- no prohibited or unofficial theme leaks into canonical output;
- version and source revision match the deployed build;
- checksums match hosted artifacts;
- migration notes cover every breaking contract change;
- hosted AI endpoints return the new release;
- a fresh-agent smoke test succeeds without private context.
- a clean environment can consume the site without the repository or a downloaded archive;
- distributable artifact scanning finds no secret, restricted, or unapproved files.

## CI layers

Use one tool per job:

- schema/link validator for machine contracts;
- framework type checker;
- unit and interaction runner;
- accessibility runner;
- Storybook production build;
- browser-based visual regression at fixed Linux fixtures;
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
