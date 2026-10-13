# Operating model

## Contents

1. Authority model
2. Evidence hierarchy
3. Greenfield versus rehabilitation
4. Foundation-first migration
5. Lifecycle and publication
6. Headless primitive decisions
7. Migration safety

## Authority model

Record authority by concern instead of naming one source “the truth” for everything.

| Concern | Typical authority | Required evidence |
|---|---|---|
| Visual geometry | Current design library | Exact node, version, screenshot, measured dimensions |
| Interaction and data | Production code or approved prototype | Source revision, tests, event/data model |
| Content | Product requirements or production | Source and owner |
| Accessibility | Standards plus approved product policy | Required semantics and any visual exceptions |
| Responsive behavior | Approved layouts plus production constraints | Viewport/container fixtures and min/max rules |
| Lifecycle | Design-system owner | Explicit status and replacement |

Write conflict rules before implementation. A common rule is “design wins visual presentation; production wins behavior,” but never assume it.

Each ruling needs concern, scope, source/version, approver and superseded ruling
IDs. Resolve contradictions within the proposed source (including scale tables
versus written rules) before comparing with code. Later explicit corrections
override earlier ones only in scope. Never apply a sidebar-only change to toasts,
or reinterpret a live-presence indicator as an invitation action.

## Evidence hierarchy

Prefer evidence in this order unless the recorded authority model says otherwise:

1. Exact current component node and approved polished screens.
2. Current production behavior and data contracts.
3. Current design-system extraction or handoff bundle.
4. Existing Storybook.
5. Historical screens and version history.
6. Agent inference.

An extraction bundle is an index of states and assets, not automatically production code. Generated files often contain fixed dimensions, duplicated subtrees, hard-coded content, missing events, and invalid responsive expressions.

## Greenfield versus rehabilitation

### Choose greenfield when

- the existing catalogue is mostly drifted or unclassified;
- foundational tokens conflict;
- canonical components are a small minority;
- legacy namespaces would mislead agents;
- build/runtime modernization is cheaper than safe cleanup.

Reuse infrastructure only after proving it is neutral: build tool, test runner, hosting, and CI may survive while visual components and stories do not.

### Choose rehabilitation when

- production behavior is substantial and trusted;
- component APIs have many consumers;
- existing stories provide reliable interaction evidence;
- foundations can be replaced incrementally;
- migration adapters can prevent consumer breakage.

Do not let reuse become an excuse to preserve wrong foundations. Create a clean canonical namespace and migrate deliberately.

## Foundation-first migration

When foundations change, review their delta before dependent components. Reuse
unchanged approved foundations in maintenance; do not impose a whole-system
migration on an isolated fix. A pilot can prove mechanics without approving a
new global visual direction.

Use this order:

1. inventory the complete legacy and target foundation contracts;
2. prepare one before/after matrix for color, type, spacing, radius, elevation, iconography, motion, responsive behavior, and content when applicable;
3. show each proposed foundation change at four linked levels: foundation primitive, reusable component, representative production module, and full screen;
4. approve or block foundation roles and exceptions;
5. migrate components in dependency order, then modules and screens;
6. verify adoption and remove temporary review surfaces.

Use real production modules and screens as evaluation fixtures. They demonstrate whether foundations work holistically, but they do not become public design-system modules.

Keep approval states separate:

- visual direction approved;
- component contract approved;
- lifecycle and replacement approved;
- production adoption approved;
- branch or pull-request action authorized.

Never infer a later gate from an earlier one.

## Lifecycle and publication

Keep lifecycle separate from publication.

Lifecycle values:

- `current`: intended direction;
- `legacy`: supported temporarily but replaced;
- `deprecated`: scheduled for removal;
- `internal`: authoring or implementation detail;
- `unknown`: insufficient evidence.

Publication values:

- `public`: independently reusable;
- `internal`: only nested inside another public component;
- `documentation-only`: visible for migration evidence;
- `hidden`: omitted from consumer surfaces.

Readiness values:

- `ready`: safe for production selection;
- `review`: visible but blocked;
- `inventory-only`: evidence captured, not implemented;
- `blocked`: known missing decision;

Never collapse these axes. A current design can be review-only; a deprecated component can remain documentation-only; an internal subcomponent can be complete but non-public.

## Headless primitive decisions

Use a headless base when it materially reduces behavioral risk for dialogs, menus, popovers, tooltips, comboboxes, selects, tabs, roving focus, or form controls.

Evaluate:

1. Can it express required semantics and state without DOM workarounds?
2. Can it be styled to exact visual authority?
3. Does it support controlled and uncontrolled use?
4. Does it preserve required keyboard, focus, collision, and portal behavior?
5. Is its dependency and bundle cost acceptable?
6. Can the team test and upgrade it?

Do not assume a headless library supplies hover styling, design tokens, component composition, or product-specific behavior. It supplies interaction machinery.

## Migration safety

- Inventory production reachability before retirement.
- Treat static zero-import results as a clue, not proof.
- Keep replacements API-compatible when consumers must not be manually updated.
- Prefer adapters and codemods over silent breaking changes.
- Mark review evidence visibly instead of deleting it prematurely.
- Give temporary evidence a retention policy separating source fixtures, private
  CI/PR artifacts and production output. Exclude temporary review/engineering
  evidence from production publication before release. Delete source fixtures
  only when authorized retention conditions are met; preserve reusable tests,
  canonical documentation and required provenance. A renamed group is not deletion.
- Record every breaking field or prop change in a machine-readable migration entry.
- Never reuse a canonical component name for a materially different contract without a major version.
