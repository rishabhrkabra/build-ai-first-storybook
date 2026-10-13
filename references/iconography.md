# Iconography for generated UI

## Personal installation default — 2026-09-23

For a **new AI-native design system with no established icon-family decision**,
choose one maintained outline family and record it as a project decision. There is
no industry-standard default, and a choice here is not authority to migrate an
existing system. Explicit project, brand or platform constraints take precedence.

Use the family's framework-appropriate official package (for example
`@tabler/icons-react` or `lucide-react`).
Pin the dependency through the project's package/lockfile policy and verify its
actual exports. Do not install or upgrade merely because this reference was read.
Stroke, size and colour follow the target project, not another project's values.

Candidates: Tabler offers broad outline coverage, typed components and searchable
catalogue metadata. Lucide suits focused implementation documentation or an
existing Lucide stack. Phosphor is preferable when authored multiple weights or
duotone are needed. This is source-based judgment, not a measured model accuracy
or performance advantage. Review dated technical claims before a new integration;
do not silently replace a recorded project choice with a fashionable one.

## Keep the glyph vendor separate from the usage contract

This approach applies equally to Figma
design systems, Storybook and live website implementation. In Figma, retain only
the working glyph subset needed by nested slots and retrieve additional official
vendor assets on demand, recording exact name/revision. The subset is not an
allowlist of every icon the product may ever use. Stories illustrate the usage
contract in real controls; production uses verified vendor exports directly.

Direct vendor imports are allowed when approved by the project; do not create
thousands of DS wrappers, Figma masters or stories just to make icons selectable.
The DS still specifies:

- family/package and version policy;
- permitted sizes, stroke/weight, semantic colour and alignment;
- accessible naming versus decoration, focus/target behaviour on the control;
- stable meaning for recurring actions and directional/RTL rules;
- permitted exceptions, unknown-name fallback and loading strategy.

An optional thin adapter can enforce defaults; it must not duplicate SVG paths or
force every glyph through a manual registration ceremony. DS buttons/controls own
interaction. Vendor glyphs fill their supported slots rather than bypassing them.
Show representative use in foundations and component stories, not every glyph.

## Functional glyph handoff gate — owner correction, 24 September 2026

A functional icon is a verified vendor asset, not a font character, emoji or
hand-drawn approximation. This covers close/cross, check/tick, directional
arrows, warning/error, plus/minus and overflow marks—not just Back arrows.
Choose by meaning, verify the exact SVG/package export, then preserve the
project's size, actual stroke and semantic colour. Do not import the whole pack.

Before marking generated UI complete:

1. Scan text nodes in the delivered scope, including hidden/alternate component
   states, for symbol candidates: arrows, ticks/crosses, warning/error emoji and
   standalone x/X, +, −/-, ! or ellipsis. In code inspect rendered JSX/text and
   CSS generated content; comments and arbitrary source strings are not UI.
2. Inspect each candidate's parent control/status context. Record node/file,
   meaning, vendor replacement or justified non-icon exception. Typography used
   as a close, success/error or navigation glyph fails even if it looks close.
   Prose, mathematics, quotations and user-authored content are not automatically
   defects. Never bulk-replace characters without context.
3. Require zero unresolved functional substitutes, verify actual vendor
   provenance/stroke after sizing, and visually inspect the affected states.
   Missing access/state coverage is unverified, never an empty passing scan.
4. Re-test both a known failure (e.g. a typed close x or a success tick) and a
   legitimate exception (e.g. a multiplication sign in a quotation). Preserve
   existing correct vendor icons as a positive control.

A symbol regex generates candidates; it cannot establish meaning or catch a
wrong-pack SVG. A separate asset/stroke check is still required. These are
task-boundary gates for agents reading this skill, not a global background
watcher or a guarantee that unrelated tools enforce them.

## Two generation paths

### Personal interface rule — 28 September 2026

The owner explicitly bans solid filled disclosure triangles across interfaces
we build, alongside the existing emoji-as-interface-icon prohibition. Use an
outline chevron from the project's approved icon family for accordion/disclosure
state. Suppress the browser's default summary marker in delivered UI; preserve
native details/summary semantics or an equivalent keyboard-accessible owner.
Inspect collapsed and expanded states, including nested disclosures and docs.
This is an owner preference, not authority to rewrite unrelated live products.

**Build-time code generation:** search version-matched vendor metadata, confirm
the exact named export, then emit static imports. Typecheck/build the actual
consumer and inspect at intended sizes. Never guess that kebab-to-PascalCase
conversion is an export contract. Do not use a whole-library namespace solely to
resolve arbitrary strings.

**Runtime data-driven generation:** accept validated identifiers, not import paths
or executable SVG. Generate a version-bound typed registry from real exports; it
may cover the family without manually authored per-glyph DS components. Retrieve
only relevant catalogue entries for the model. Use a bounded product subset or
explicit lazy chunks, measure first-render/SSR/loading behaviour, and provide an
approved fallback for unknown names. Unlimited eager loading is not modularity.

For decorative icons set appropriate hidden semantics; for icon-only actions put
the accessible action name on the control. Avoid family/weight mixing by accident.
Keep any copied/distributed upstream license notices. Brand marks retain separate
trademark constraints. No external runtime fetch is required merely to draw icons.

## Authoritative lookup

- [Tabler framework docs](https://docs.tabler.io/icons/libraries/react) and
  [Markdown](https://docs.tabler.io/icons/libraries/react.md): named components,
  size, colour, stroke; confirm the target framework rather than assuming React.
- [Tabler source](https://github.com/tabler/tabler-icons) and
  [package metadata](https://www.npmjs.com/package/@tabler/icons): catalogue tags
  and categories support retrieval; installed exports remain the import authority.
- [Lucide React](https://lucide.dev/guide/react),
  [dynamic loading limitations](https://lucide.dev/guide/react/advanced/dynamic-icon-component).
- [Phosphor React](https://github.com/phosphor-icons/react) and
  [typed catalogue](https://github.com/phosphor-icons/core).

Primary research was checked23September2026. Both Tabler and Lucide have
machine-readable documentation; this alone is not evidence of superior AI output.
