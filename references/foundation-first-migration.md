# Foundation migration: optional production integration detail

Read for a substantial foundation/package migration, not a routine component fix.
The governing scope and approvals remain in `operating-model.md`.

## Package and baseline

Pin the real production baseline and preserve its source state. Keep integration
work separate from the reference being measured. Follow the user's branch/PR
policy; do not create another PR or rebase merely to follow a preferred topology.

If the app consumes a package, test the final package after both library and site
builds. Keep their outputs separate. Verify exports, styles, assets, types,
peer dependencies, licences and a clean consumer install. Use token-only or
scoped foundation exports if the project needs side-by-side adoption; they are
not mandatory for a project without that migration topology.

Temporary local package links must not accidentally become a published dependency.
Record the final immutable version and artifact digest. A bridge should map
approved semantic equivalents, opt in only the affected surfaces, and leave app
handlers/data unchanged. Check unresolved variables and dormant themes before
removing compatibility code.

## Contextual evidence

Pin consumer/story ID, route/query, data/persona, state, theme, fonts, viewport or
container size, source revision and build artifact. Compare the same state on
both sides. Review changed roles as foundation → component → production module
→ full screen when those changes reach all four levels.

Distinguish:

- Production before: actual pinned running code.
- Design reference: visual authority, not proof of production behavior.
- Candidate after: actual candidate code.
- Code-contract difference: values differ, visual verification still pending.
- Before unavailable: no matched state; do not manufacture a legacy specimen.
- Behavior evidence: interactions/tests of callbacks, routes, focus and async state.

For typography, group by the shared DS type-scale roles, with varied component
uses as examples. A usage such as a launcher is not itself a scale step. Show the
full type specification and identify proposed new steps; size alone is not a
match. Crop to the focused component and nearby hierarchy, retaining focus
corners through scrolling. Keep avatar sizing separate.

Show the visual comparison before long rationale. Fixture styling can arrange
frames and labels; it must not override component internals to fake parity.
Measure typography hierarchy, semantic colour roles, spacing relationships,
icon optics, layering and containment in context—not only swatches or token bars.

## Residuals and teardown

Record what the foundation graph reaches: token-connected consumers,
compatibility aliases, hard-coded visual debt, product/data colours, exact
artwork, behavior-dependent geometry and unresolved mappings. Do not claim a
migration percentage without a denominator and measured reachability.

Semantic consolidation follows the admission rule in `component-contracts.md`.
Sharing a progress primitive does not make a loading canvas a chat card.
After authorized adoption, remove temporary bridges/flags when their conditions
are satisfied. Exclude temporary review evidence from production publication
before release, retaining private proof and reusable tests according to policy.
Keep canonical docs and versioned migration provenance. The portable scaffold
does not require or publish a second foundation-migration catalogue.
