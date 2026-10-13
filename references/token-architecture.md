# Token architecture and variable-work gate

Apply when creating, renaming, merging, migrating or rebinding design tokens in
Figma or code. This is shared with the Storybook contract workflow. Consuming an
unchanged approved component does not require re-auditing its foundations.

## Before writes

Read [change-completion.md](change-completion.md) and identify the approved
decision plus affected documentation/consumer closure before changing tokens.
Graph validity alone cannot close a naming, consolidation or synchronization
decision. Reuse the project register and validate fresh measured artifacts.

1. Read live values, modes, names, aliases, scopes and affected consumers. Never
   replay a stale export over owner edits. Inspect merge markers and compare
   current values before consolidation; they are not final token names.
2. Separate raw value, shared purpose and component ownership. Primitives cannot
   encode heading, surface, action, navigation, avatar or disabled roles.
   `color/purple/700` is raw; `color/text/primary` is semantic; `avatar/background`
   is component-owned. Descriptive hue names are not inherently invalid. Numbered
   palettes are a project convention, not a DTCG mandate. Do not invent shades.
3. Use two tiers if shared roles suffice; add a selective component tier for
   independent component decisions. Do not add a third alias to every property.
   Shared semantic roles must not depend on component tokens.
4. Screen builders reuse approved components first. Component colours route
   through shared semantic roles; independently owned geometry may alias raw
   dimensions directly. No screen-level palette selection.
5. Record purpose, permitted uses, owner/tier, type, source and status. Observed,
   draft, approved and accepted accessibility exception are different. Owner
   preference is not WCAG certification. Missing states remain explicit gaps.
6. Preview the proposed graph and consumer map. Preserve IDs for safe renames;
   rebind and verify consumers before deleting duplicates. Renaming does not
   authorize a value change. Check references, types, cycles, ownership, naming
   and raw-value use—not just alias resolution.

## Executable gate

Run `python3 <skill>/scripts/validate_token_graph.py <manifest.json>` on the
proposed graph before mutation, then on the fresh live export after mutation.
Label proposed versus actual evidence. Nonzero exit blocks a completion claim.

Normalized export: `tokens` plus optional `bindings`. Each token has `id`, `name`,
`tier` (`primitive|semantic|component`), `type`, `values` keyed by mode, `purpose`,
`permittedUses`, `status`, `source`, and component `owner`. Aliases are
`{"type":"VARIABLE_ALIAS","id":"..."}`. Policy `numberedColorPrimitives`
enables numerical palette naming. Bindings have `nodeId`, `field`, `tokenId`,
`context`, and the owning component's `owner` where relevant.

The checker covers role-name leakage, numeric scale/value mismatch, merge
markers, duplicate identifiers/names, missing/type-invalid aliases, cycles,
upward dependencies, component ownership and exported direct-primitive bindings.
Equal values alone never justify merging different semantic roles.

It does not extract Figma, infer intent, authenticate approval, inspect unexported
raw paints or certify accessibility. State binding coverage. Inspect affected
live components for raw-value drift and test bad fixtures plus legitimate
counterexamples. Then verify visual/state/layout/theme behavior in context.

## Handoff

Name the current authority: Figma may author design before code owns implementation.
Generate the versioned ID/name/type/alias/status manifest from that authority;
never maintain a second independently editable token truth.

Completion includes visible foundation specimens, actual variable/effect
definitions, affected bindings, contextual comparisons and a refreshed ledger.
Footer separation is not generic card elevation. A valid radius is not the
radius for every rectangle. AI-facing contracts belong here rather than in a
parallel Figma governance skill.

These are repeatable workflow gates, not a global Figma mutation hook or a
promise that every future agent will comply. Test and report their real coverage.
