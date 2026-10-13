# Generative UI guidance and correction loop

## Authority and surfaces

Use for Figma, Storybook and live UI generation/review. Keep one project-scoped
contract owner. Figma may be the current visual-authoring source before code
exists; do not require Storybook or code merely to document a Figma system.
Behavioral production authority remains explicit and separate.

A Figma-native entry frame must link to: constitution; relevant contextual
patterns/anti-patterns; component descriptions; token purposes/aliases/status;
known gaps and retained exceptions; decision ledger; validation procedure.
Use stable rule IDs, reasons, scope, source context and approval status. Keep
experimental composition open where no established rule exists. Never infer
that approval of one element freezes the whole layout or design language.

Component descriptions identify intended use, non-goals, exposed properties,
composition, state/readiness limitations and source/entry links. Variable
descriptions identify tier, owner, purpose, permitted use and approval scope;
exact names, types and aliases come from native metadata, not copied prose.

Generate portable exports from the authoring source with capture time, source
IDs, schema/version and checksums. Never maintain the export as a competing
editable authority. A checksum proves captured bytes, not current freshness;
refresh from the source before a new task. Sensitive project content stays in
the project's authorized access boundary. Self-contained does not mean public.

## Conditional pattern contract (owner adopted 2026-09-23)

Teach decisions through conditions, not slogans. Every contextual pattern uses:

- **When:** task, user intent and relevant state that activate the pattern.
- **Use:** concrete composition/behavior and the existing component owners.
- **Avoid:** the tempting alternative that is wrong in this context.
- **Why:** the user-facing reason, not an aesthetic slogan.
- **Exception:** a bounded condition that legitimately changes the default;
  unknown exceptions remain questions, not invented permissions.

Record stable rule ID, scope, source, date and evidence/approval status. Keep
rule strength separate: **requirement** binds within scope; **recommendation**
is a reasoned default; **unexplored** is room for a labelled proposal. An
observed pattern is not automatically a requirement. Never freeze unrelated
layout choices because one element was approved.

Example: when verifying one AI observation, put relevant source beside the
focused summary; avoid unrelated observations in the same evidence card,
because they compete with verification. A separate browsing mode may show
many observations. This does not prescribe one universal column ratio.

Use this structure in Figma-native guidance and its generated Markdown export.
Apply it to contextual patterns in an existing Storybook too; adopting it is
not a claim that the Storybook has already been migrated. Do not fork a second
editable text authority.

## Trigger at work boundaries, not via an imaginary watcher

At generation review, owner correction and design finalization, compare the
actual result with the current contract. A failed generation triggers diagnosis
immediately; it does not require a second occurrence. Before closing the task,
record a passed comparison or an evidenced mismatch. Workflow-pilot routes to
this reference and its `design-system-feedback` protocol when applicable.
These are agent/hook task-boundary instructions, not a background Figma watcher.

Minimum mismatch entry:

- stable ID, project, task and source/contract revision;
- expected versus actual, exact rule/component IDs and contextual evidence;
- status: open, repaired, rule-change-proposed, resolved, retained-exception,
  superseded or not-reproduced;
- cause: retrieval, execution/tool, ambiguous rule, missing capability,
  rule conflict or unknown; distinguish evidence from hypothesis;
- repair/proposal, owner decision and scope (or explicitly pending);
- affected consumers, validation and a previously passing counterexample;
- successor/superseded link, never silent erasure of earlier decisions.

## Decision policy

1. Correct rule, wrong output: repair generation/retrieval/implementation. Do
   not relax the rule to pass. Add a regression check where repeatable.
2. Ambiguous guidance: clarify the existing owner with a scoped example and
   counterexample. No new visual/behavioral approval is inferred.
3. Missing capability: record the gap; an authorized draft stays isolated and
   non-selectable as production. Do not counterfeit a ready API.
4. Explicit owner-approved contradiction: open a rule-change proposal now.
   Same-role drift across two independent approved designs also opens review;
   this is a review threshold, not automatic promotion or an industry law.
   Multiple screenshots of one design are not independent observations.
5. Unapproved repeated output, one-off taste, or unclear cause: retain evidence
   without promoting a general rule. Ask only for material unresolved choices.

Within explicit authority, update the canonical rule/component/token owner,
retain its prior version and decision rationale, regenerate exports and run the
failed case plus a previously passing case. Otherwise leave a review proposal.
Never silently approve baselines, delete history, publish, merge or deploy.

Before implementing an approved contract change, use
[change-completion.md](change-completion.md) to register the affected closure and
decision assertions. Afterward verify consumers, Foundations, native guidance
and derived exports, as applicable. Passing graph checks or updating one guide
does not prove the whole approved decision is complete. Preserve the ledger.

## Visible ledger and evaluation

The human review surface is a contextual visual comparison, not a text-layer
inventory. Group affected examples by decision/role and show readable current
and proposed treatments with surrounding UI, status and source links. Keep
node IDs, exhaustive layer tables and machine inventories as supporting audit
evidence; never hand the owner a giant Markdown table as the place to judge a
visual change. Metadata coverage does not replace a usable review experience.

For card, field, CTA, affordance or state-colour corrections, apply
[composition-contracts.md](composition-contracts.md) and its measured checker.
Keep the failed measurement, positive exception and repaired measurement. A
correct isolated component or token graph is not proof of correct composition.

Resolved comparisons remain visible with quieter neutral framing and status/date.
Do not fade, recolor or shrink the compared artwork to imply a difference or
success. Keep source links, full relevant context and open/resolved/exception
states distinct. Archive policy is an explicit owner choice, not a cleanup habit.

Test a fresh agent with only the authorized entry and a realistic brief, no
expected component list or known-defect hints. Use an isolated draft target.
Record retrieval, correct reuse, state gaps, visual/structural checks and fixes
separately. One successful run is not universal reliability. If unavailable,
report the blocked test rather than substituting a self-review as blind success.

See [iconography.md](iconography.md), [blind-evaluation.md](blind-evaluation.md)
and [continuous-evolution.md](continuous-evolution.md). This reference owns the
cross-surface learning policy; project guides supply their own facts and rules.


## Contextual visual review standard

For Figma/Storybook design reviews, use the current project components in the review shell too. Keep the simple source links; point to the selected Figma layer and exact Storybook owner or story. Show Current / Proposed / View both, progress and a decision; technical inventories stay in supporting evidence and JSON.

Default to a contextual crop containing the whole changed element, its boundary/shadow, the containing section and the labels or adjacent controls needed to judge it. Choose semantic section bounds, not a fixed tight margin. Use the same crop, content, state and scale on both sides; include any proposed reflow. Show full screen is the escape hatch. Pair contextual crops horizontally and full-width screens vertically; locate below-fold changes automatically and provide a return-to-change action. A focus marker stays outside the visible shadow and never tints the compared artwork.

Group by the decision and affected code implementations. Different behavior can require separate decisions even when primitives are shared; repeated screenshots of one implementation are examples/state coverage, not extra implementations. Think in terms of the instance that will change in code. For example, a chat entry composer and a side-panel composer are separate decisions; other appearances of the panel are examples of its shared implementation. Keep mapped examples and known missing coverage accessible. Shared-source changes reopen affected decisions, retaining history; do not claim a watcher or CI gate exists until implemented and exercised. Incomplete coverage cannot confer global approval.

Fit actual data into the established semantic owner first, then let the designer judge the populated result. A generic story is not a replacement preview. Keep commands, persistent choices and passive statuses distinct. Notes appear only for Needs changes; Approve/Keep current export no active change note. JSON separates implementation scope, examples, exceptions, source version and prior reviews. This is a scoped review standard.
