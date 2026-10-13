# Whole-change completion gate

Owner-adopted, 24 September 2026. Applies across projects to authorized changes
to design tokens, styles, component contracts and design-system guidance in
Figma, Storybook and live implementations. This is a completion obligation,
not permission to change additional products, publish, deploy or accept designs.
An audit remains read-only. Consuming an unchanged component is not a migration.

## 1. Define the decision before changing its implementation

Record the approved outcome, scope, authority and observable acceptance checks.
Separate structural validity from the decision's meaning. For example, if an
owner approves one neutral family, correct hex values and resolving aliases do
not prove the naming/grouping decision is complete. Preserve distinct semantic
roles when merging raw values. This example does not impose one neutral family,
a palette, a tier count or a spacing scale on other projects.

Turn each material approved requirement into a check: exact retained/retired
values and IDs, names, grouping/order, roles preserved, state coverage, or source
parity as appropriate. Aesthetic acceptance still needs actual visual review;
do not replace it with a `passed: true` field. Unresolved decisions are blockers,
not opportunities to invent approval. Capture before evidence when needed.

## 2. Maintain one dependency register, not another source of truth

Reuse a project's existing inventory/manifest. At setup, or on first relevant
maintenance, register actual IDs/paths, authority, dependencies, verification
method and whether a surface is current, historical or not present. Review:

| Surface class | Examples to inspect when applicable |
|---|---|
| Authoritative definitions | Figma variables/styles, code tokens, modes |
| Aliases and consumers | Semantic/component aliases, masters, overrides, raw paints, screens, themes |
| Foundations and catalogue | Swatches, names, values, scales, ordering, counts, examples |
| Native guidance | Constitution, component descriptions, usage contracts, contextual patterns |
| Portable guidance | Markdown/JSON exports, agent entry point, image-generation guide |
| Implementation and tests | Packages, Storybook, application consumers, snapshots and contract tests |
| Review and discovery | Decision ledger, follow-up/status report, current pointers and installed skill copies |

Follow transitive dependants, not only directly bound instances. Give an explicit
reason for unaffected or absent classes. Do not create Storybook or code merely
to populate a Figma-only register. Stable IDs survive renames. Check live sources
for concurrent edits before writes; stale exports must not overwrite them.

Historical evidence is separate: preserve old designs and resolved comparisons,
label their revision and update current pointers. "Remove stale information"
does not mean rewrite history. Scope adapters must exclude history deliberately,
not silently drop it. Unknown inventory coverage stays unknown.

## 3. Generate mechanical documentation, review authored meaning

Derive names, swatches, values, aliases, types, counts and IDs from the current
authoritative export. Store its revision/digest and the generating path with the
derived artifact. Order/group specimens according to the approved decision, not
an accidental alphabetical sort. Never maintain a second editable token truth.
Review usage prose and exceptions for meaning; a find-and-replace is not enough.
An adapter should export measured document values/paints and visible labels so
they can be compared with the source, not copy expected answers into the report.

## 4. Close only the verified dependency closure

After authorized edits, retrieve fresh authoritative and consumer data. Run the
existing architecture/contract checks **and** the decision assertions. For each
affected surface record verified, evidenced-unaffected, preserved-history,
pending or blocked. Pending, missing or blocked required work prevents a
complete claim. Report partial work honestly when another owner/action is needed.

Inspect affected visual outputs at readable scale, with their surrounding
context and matched states. Check wrapping, sizing modes, clipping, row/action
alignment, density and whether labelled comparisons really differ. Retain capture
references and what was inspected. An export existing is not visual inspection.
Recheck the original failure and a previously valid case; unrelated exceptions
must remain valid. Run checks again after fixes rather than restamping receipts.

## Portable executable support

`python3 <skill>/scripts/validate_change_sync.py <receipt.json>` checks a small
project-authored dependency/evidence receipt. Use it alongside, not instead of,
`validate_token_graph.py` or the project's existing validators. Do not introduce
a parallel register if an adapter can emit this view from the current one.

Schema version 1 has these fields (paths are relative to the receipt):

- `change`: nonempty `id`, `decision`, `approvalSource`, and `roots` surface IDs.
- `surfaces`: unique `id`, `source` (native ID/URL or file), `path` (actual file or
  fresh exported JSON/text), `sha256`, `dependsOn` IDs, and boolean `visual`.
  A remote snapshot must retain the native revision/read time in its data;
  freshness against the live app is the collector's responsibility.
- `checks`: unique `id`, `actual: {surface, pointer}` (RFC 6901 JSON pointer;
  empty string reads the whole JSON or text file), `op`, and `expected` literal.
  Instead of `expected`, `expectedFrom: {surface, pointer}` compares two measured
  artifacts. Supported operations: `equals`, `contains`, `not_contains`,
  `every_match` (nonempty string array against a full-match regular expression).
- `requirements`: unique `id`, nonempty approved `statement`, and nonempty
  `checks` IDs. Every material decision needs an assertion or an explicitly
  unresolved visual/owner decision; do not shrink requirements to get green.
- `coverage`: one entry per affected surface, `id`, `status`, `reason`, and
  `inputs` mapping each direct dependency to its freshly observed SHA-256.
  `verified` and `unaffected` require nonempty `checks` that inspect that surface.
  `historical-preserved` requires `beforeSha256` equal to the current file digest.
  Visual surfaces also require `review: {reviewer, result: "pass", notes,
  sourceSha256, capture: {path, sha256}}`. This validates a bound review record,
  **not** whether the reviewer actually looked or judged correctly.

The checker rejects stale file digests, missing/cyclic dependencies, uncovered
transitive dependants, absent/failed requirements, stale upstream receipts,
missing visual evidence and pending/blocked work. Unit fixtures show the complete
schema. Intent checks operate on actual exported data, not supplied pass flags.

Limits: a fabricated snapshot/receipt, omitted dependency, wrong approval or
inadequate assertion can still mislead a local validator. Review the register
and assertions; record collector coverage. This is not a live watcher, authority
authenticator, accessibility certification or a guarantee that every future
agent loads the skill. Installing a CI/native hook needs its own scoped approval.

## Handoff and future projects

This reference belongs in the shared skill and its installed copies. Project
entry points should route here; project registers hold project facts. Workflow
Pilot should activate it at contract-change/correction/finalization boundaries,
without promoting advisory research into policy. New repositories bootstrap the
small register when a design system exists; they do not inherit another system's
token values or process history. Report changed surfaces, verified decisions,
evidence and explicit gaps before using "complete" or "in sync".
