---
name: build-ai-first-storybook
description: Build, audit, migrate, or maintain design-system contracts and Storybook. Use for creating, renaming, merging or binding design tokens/variables in Figma or code, component ownership, reusable APIs, authority, lifecycle and validation. Ordinary screen work should consume existing contracts, not restart the whole system.
---

# Build an AI-first Storybook

**Route:** mid-tier for construction, migration and validation runs; scripts
do the exact checks. Escalate to the best model for authority, ownership and
token-architecture decisions, and for any audit verdict that changes a
contract.

Storybook is the human review surface, not an independent source of truth. Keep
one versioned contract with production code; generate documentation, discovery,
agent context and validation from it where practical. An unfamiliar agent must
know what it may use, how it behaves, how it composes, and what was verified.

## Select the task boundary

Infer mode from the explicit request and repository evidence. State material
assumptions; ask only when they change the result. Record mode in project task
metadata when CI needs it; do not demand a sidecar to understand a clear request.

| Mode | Required scope | Do not silently do |
|---|---|---|
| Audit | Read sources, reproduce findings, report evidence and suggested fixes | Edit components, deploy, or reorganize stories |
| Greenfield | Establish authority, foundations, primitives and discovery | Import another project's identity or governance rituals |
| Migration | Map consumers and replacements, preserve behavior, compare affected before/after states | Treat renaming as migration or zero imports as deletion authority |
| Maintenance | Change the requested contract and affected dependencies; reuse approved foundations | Reopen the whole system or require unrelated recipes |

Implementation approval does not authorize unrelated application changes, new
PRs, merge or deployment. Reuse granted decisions at their stated scope.
Escalate unresolved semantic/authority choices to the named owner, not merely a
more capable model. Bound repair attempts; stop when further work needs a new
decision or repeats the same uninformative failure.

## Essential rules

- One visual owner per semantic capability. Prefer an existing primitive or
  composition, then a justified screen-neutral extension, then an app adapter.
  Create a new family only for a genuinely different contract. Naming or moving
  a component does not make it coherent with the system.
- Composed DS components use canonical primitives/tokens for the capabilities
  those primitives own. Foundational primitives may use native/headless bases;
  this rule must not create circular dependencies.
- App adapters retain routing, permissions, parsing, business state, network
  and asynchronous behavior. They translate data and callbacks, not duplicate
  borders, padding, focus, overlays or selection styling.
- Similar geometry is not semantic equivalence. A badge differs from a choice;
  chat generation progress can differ from center-canvas loading.
- Inventory, lifecycle, readiness, placement and distribution are separate.
  A missing replacement is not evidence of legacy. Candidates remain private
  and non-selectable. Recurrence opens review, not promotion.
- Zero observed consumers opens retirement review only. Check dynamic loading,
  routes, registries, downstream packages and unobserved states before an owner
  approves deprecation or deletion.
- Keep private records physically outside published output. Publish only
  reviewed artifacts. Agent access can be local, authenticated team access or
  public; self-contained does not mean publicly exposing code.
- Automation may detect, diagnose, repair and propose. It must not silently
  promote, retire, accept visual baselines, merge, deploy or rewrite approvals.
- Separate schema validity, repository-policy checks, build/test evidence,
  visual acceptance and deployed verification. A skipped required gate is not
  a pass. A metadata receipt is not proof its assertions are true.

## Establish project authority once

Resolve only what the task needs: frameworks/package boundaries, visual and
behavioral sources, themes/containers, accessibility policy, review ownership,
distribution rights and access model. Do not import colours, sizes, categories,
props, approval dates or exemptions from another project. Thresholds and story
taxonomy are project choices, not universal laws.

For each decision record concern, scope, source/version, approver and what it
supersedes. Check a proposed source's rules and scale for internal contradictions
**before** comparing it with code or propagating token changes. Later explicit
corrections supersede earlier rulings only within their scope. Never invent an
owner or approval timestamp.

Read [operating-model.md](references/operating-model.md) for authority/migration
choices. Review changed foundation roles before dependent component migration;
unchanged approved foundations need not be re-approved for routine maintenance.

## Build or repair the contract

Before an authorized contract change, read
[change-completion.md](references/change-completion.md) and register its approved
outcome, assertions and affected dependency closure. Completion uses that same
scope; do not reduce it afterward to the surfaces that happened to get fixed.

For Figma-native agent guidance, generative UI failures, owner corrections or
finalized-design drift, read [generative-feedback.md](references/generative-feedback.md).
Diagnose each observed failure; change approved rules only within owner authority.
Keep resolved comparisons visible as a quiet ledger. Do not build Storybook just
to make a Figma-authored contract usable by an agent.

When selecting an icon family for a new system or defining direct vendor-icon
use in generated UI, read [iconography.md](references/iconography.md). It carries
the personal greenfield preference and the lightweight usage contract; established
project choices and explicit exclusions override it. No automatic migration.

For any design-token/variable work, including Figma-only work without Storybook,
first read [token-architecture.md](references/token-architecture.md). Validate the
proposed graph before mutation and a fresh authoritative export afterward with
`scripts/validate_token_graph.py`. Alias resolution alone is not architecture
validation. This gate does not require building Storybook or changing authority.

1. Inventory in-scope families, actual consumers, exports, stories, replacements
   and gaps. Full migrations need full inventory; repairs need affected dependencies.
2. Apply the admission rule in [component-contracts.md](references/component-contracts.md).
   Keep workflow logic feature-local and document missing primitive capabilities.
3. Implement typed state, content, overflow, keyboard/focus and composition
   contracts. Do not expose screen-name props to conceal a clone.
4. Use real production components in stories. Domain-specific example text
   does not create a separate visual family.
5. Capture real before states before migration edits. Preserve behavior through
   adapters; compare identical data, fonts, themes, states and viewports. Record
   unavailable baselines honestly.

Read [rehabilitating-existing-interfaces.md](references/rehabilitating-existing-interfaces.md)
when replacing existing UI, and [foundation-first-migration.md](references/foundation-first-migration.md)
for package boundaries, contextual evidence and temporary bridge teardown.

## Organize and distribute

Choose discoverable categories for the project. Foundations, Components,
Patterns and Brand are examples, not mandatory taxonomy. A branded component
may still be a component. Keep one canonical story identity per capability;
variants and examples belong with that owner.

Read [storybook-information-architecture.md](references/storybook-information-architecture.md)
before navigation/story removal. Track runtime migration, story classification
and evidence retention separately. Temporary prefixes do not complete migration.
Exclude temporary audit/visual evidence from production publication before
release; retain private review material per policy and preserve reusable tests.

Read [agent-interface.md](references/agent-interface.md) and
[portable-contract.md](references/portable-contract.md) before bootstrapping,
publishing or changing scripts. The v2 scaffold is **private authoring data**,
never a Storybook static directory:

```bash
python3 <skill-dir>/scripts/scaffold.py --target <repo> --name "<System>"
python3 <skill-dir>/scripts/validate.py --root <repo>
```

These commands validate structure, not project readiness. Configure project
source ownership/review rules, scanning scope and framework checks before
claiming enforcement. Refresh authoring checksums after authorized changes,
validate against the CI-selected trusted base, and export to a fresh directory:

```bash
python3 <skill-dir>/scripts/update_checksums.py --root <repo>
python3 <skill-dir>/scripts/validate.py --root <repo> --base-ref <trusted-full-sha>
python3 <skill-dir>/scripts/export_public.py --root <repo> --output <fresh-dir> --base-ref <trusted-full-sha>
```

Only the export belongs in Storybook static assets. Generation is not deployment
or permission to publish. Migrate v1 explicitly as described in
`portable-contract.md`; never silently overwrite it.

## Verify at the right layer

Read [quality-gates.md](references/quality-gates.md). Measure the actual package/app
artifact, not just source, and run exact CI commands. Scope row heights,
truncation, radii and interaction geometry to approved contracts. Test known
defects and legitimate counterexamples; do not ban decorative `aria-hidden` or
correctly inert modal backgrounds. Assert the intended test state was reached.

For visual changes show reference/before/after at matched states and widths,
including contained/modal and boundary content. Explain the visible outcome
first. An unchanged screenshot alone does not prove behavior. Verify deployed
revision only when deployment is in scope.

Read [framework-adapters.md](references/framework-adapters.md) for framework
readiness and [blind-evaluation.md](references/blind-evaluation.md) when validating
agent consumption or portability. A full fresh-agent evaluation belongs to
release/major-contract work, not every small fix. Synthetic script tests do not
prove real-project portability.

## Evolve without inventing authority

Read [continuous-evolution.md](references/continuous-evolution.md) for candidates,
developer warnings, exceptions and self-healing. Track MCP retrieval,
development/test operations and repair separately as absent, configured or
exercised. Make a real safe tool call and run a representative test before
claiming they work. Mutation/test tools require authorized, authenticated
environments; never enable hosted mutation by default.

Use [failure-modes.md](references/failure-modes.md) and
[implementation-lessons.md](references/implementation-lessons.md) when diagnosing
recurrence. Historical incidents support scoped rules, not universal workarounds.

## Completion

For authorized token, style, component or guidance changes, read
[change-completion.md](references/change-completion.md). Register affected
dependencies, generate mechanical documentation from the authority, test the
approved intent as well as structural validity, and verify every affected
surface. Run `scripts/validate_change_sync.py` on the scoped evidence receipt;
missing coverage, stale derivatives or an unmet decision block a complete claim.
Preserve historical evidence and inspect actual affected renders. This applies
to Figma-only and live-code work too, not only Storybook. New projects
register their own sources; do not inherit another project's palette or policy.

Report the requested outcome, changed scope, verified layers, unrun checks and
remaining decisions. An audit ends with findings. Maintenance ends with affected
consumers and checks. A release also proves safe distribution, artifact identity
and clean consumer use. Do not declare universal readiness from schema tests.
