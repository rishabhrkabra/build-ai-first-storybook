# Continuous design-system evolution

Use this reference after the first usable release, or whenever the task includes design-tool synchronization, content governance, exception handling, component mining, MCP, generative UI, or cross-repository migration.

## Contents

1. Target architecture
2. Change intake and review gates
3. Executable design constitution
4. Structured content and tone
5. Exception and component mining
6. Recipes, evaluation screens, and GenUI
7. MCP sequencing
8. Maturity order and health signals

## Target architecture

The target is not a larger Storybook. It is one structured, versioned design-language model with generated human and machine surfaces:

```text
Canonical typed registry + production code
├── Storybook for human review
├── framework packages and exports
├── selective /ai context
├── thin agent skills and MCP tools
├── lint rules and consumer validation
├── codemods and migrations
└── interaction, accessibility, visual, and blind evaluations
```

No branch of this tree may become a hand-maintained second truth. Store stable IDs, authority, lifecycle, readiness, rules, and version identity in the canonical layer; generate or validate every surface from it.

## Change intake and review gates

Use this design-tool-to-release shape:

```text
Approved library publish or code change
→ collect and deduplicate events
→ extract tokens, components, content, and assets
→ compare with canonical schemas
→ create a branch and reviewable change proposal
→ run type, interaction, accessibility, visual, and contract checks
→ owner reviews and merges
→ Storybook, packages, /ai, and migrations release from one revision
```

Design tools commonly emit more than one event for a single publish. Coalesce by source revision and a short collection window before opening a proposal. Make the collector idempotent so retries cannot create duplicate releases.

Automate when authority is exact:

- token value candidates;
- exact SVG or approved asset updates;
- inventory, provenance, and coverage changes;
- generated documentation and context shards;
- story and visual-baseline candidates;
- schema-detected breaking-change reports.

Require named human review for:

- public component APIs and behavior;
- semantic names and consolidation;
- deletions, deprecations, and replacements;
- new visual or content principles;
- unresolved authority conflicts;
- production release or cross-repository migration.

Record visual approval, contract approval, lifecycle approval, production adoption, and authorization to create a branch or pull request separately. Approval at one layer does not authorize the next.

Figma or another design library can remain visual authority while code remains behavioral authority. If the design-tool API cannot expose required variables or metadata, use a small approved exporter or plugin to create the same reviewed proposal. Code Connect may help map design and code, but it is not a substitute for change governance.

Before implementing vendor integrations, verify current plan limits, event semantics, and supported toolsets in official documentation. Do not freeze transient vendor capabilities into the design-system contract.

## Executable design constitution

Turn repeated design judgment into scoped, testable records. A useful rule shape is:

```text
id
principle
appliesWhen
requires
forbids
rationale
severity
validator
evidence
exceptionOwner
exceptionExpiry
```

Keep rules intent-specific. “Use selection roles for persistent choice states” is enforceable; “make it feel clear” is not. Render the same rule in Storybook, return it through selective agent context, and execute its validator where possible.

Keep exceptions in an expiring ledger with a reason, owner, affected surface, and expiry. A global waiver is a missing rule disguised as convenience. When the same exception recurs, open a rule, token, recipe, or component candidate.

## Structured content and tone

Treat content as a foundation when the design system governs labels, UI messages, agent responses, or AI states. Store structured records rather than prose-only guidance. A useful entry shape is:

```json
{
  "id": "generation-error",
  "context": "generation-error",
  "userState": "blocked",
  "intent": "explain and recover",
  "tone": ["direct", "calm", "non-blaming"],
  "requires": ["what failed", "what remains safe", "next action"],
  "forbids": ["hype", "false certainty", "stack traces"],
  "terminology": {},
  "examples": [],
  "counterexamples": []
}
```

Cover at least voice invariants, tone by user moment, buttons and fields, empty/loading/success/error states, destructive confirmations, AI uncertainty, tooltips, agent responses, and preferred or forbidden terminology. Generate Storybook guidance, `/ai/content.json`, content lint, and MCP results from the same records.

## Exception and component mining

Mine evidence; do not auto-promote components. Useful signals include:

- repeated JSX or DOM structure;
- similar prop, state, or event models;
- repeated local CSS or token combinations;
- visually similar screenshots;
- recurring lint suppressions;
- multiple custom implementations solving the same intent.

Choose a threshold appropriate to the codebase. Three occurrences across two independent modules is a reasonable investigation trigger, not a universal law.

Create a candidate report containing:

- every occurrence and owning module;
- same-state screenshots at named viewports;
- behavioral and semantic differences;
- proposed purpose, non-goals, API, variants, and content model;
- accessibility and responsive contracts;
- adoption, migration, and codemod impact;
- evidence for and against consolidation.

The owner answers one hard question: are these genuinely the same semantic concept? Visual similarity cannot answer it. After approval, create the component, stories, tests, package change, codemod, migration entry, and consumer PRs as one versioned operation. Never silently mutate all consumers.

## Recipes, evaluation screens, and GenUI

Prefer a component-light system, not a component-free one. Keep accessible behavior such as focus management, overlays, keyboard navigation, dragging, resizing, and conversation scrolling inside typed components or proven headless primitives.

Use polished full screens as:

- composition and responsive evaluation targets;
- visual-regression fixtures;
- provenance and rehabilitation evidence;
- sources for small reusable recipes.

Do not export product-specific “module starters” as public design-system components. They freeze one information architecture and teach agents to copy examples as standards.

For generative UI, let the model emit structured blocks mapped to an approved registry. Allow domain content such as cards, status, progress, metrics, tables, summaries, recommendations, and approved actions when contracts exist. Keep application shells, global navigation, conversation framing, and arbitrary CSS outside unconstrained generation.

## MCP sequencing

MCP improves selective retrieval and operations; it does not create design quality. Build it only after the canonical registry, public allow-list, descriptions, tests, and version identity are correct.

Prefer a thin, read-only facade with operations such as:

```text
get_current_release
plan_ui
find_components
get_rules_for_intent
get_content_rules
validate_consumer
find_migration
report_design_system_gap
propose_component_candidate
```

Each operation must read the same registry used by Storybook and `/ai`. Add authentication, cache identity, observability, permissions, and backwards compatibility before calling the MCP production-ready.

Enable vendor-provided documentation, development, or test tools only after curating their manifests. More tools over a noisy catalogue make agents confidently wrong faster.

## Maturity order and health signals

Build in this order unless evidence justifies a change:

1. Curate authority, inventory, public API, foundations, content, composition, lifecycle, and migrations in one schema layer.
2. Repair Storybook and agent manifests; exclude review, anti-pattern, inventory, and evaluation-only material from selection.
3. Add executable interaction, browser accessibility, responsive, visual, and blind tests.
4. Add safe source-publish-to-PR automation.
5. Add intent-first planning and design-system review to consumer PRs.
6. Add adoption markers, clone detection, exception ageing, component mining, and codemods.
7. Add constrained GenUI, then a thin MCP when retrieval or operations justify it.
8. Add automated cross-repository migration proposals only after one-repository migrations are reliable.

For an existing design-system migration, treat foundations as batch zero. Review their effect at foundation, component, production-module, and full-screen levels before continuing component-by-component. Remove temporary Migration Review stories after adopted changes are merged, deployed, and verified; keep canonical docs and versioned provenance.

Track readiness by more than component count:

- age of open authority decisions and exceptions;
- repeated clones and local restyles;
- candidates accepted, rejected, or left unresolved;
- ready components without interaction or responsive evidence;
- migrations without codemods or consumer proof;
- stale hosted endpoints or mismatched revisions;
- blind tasks that required guessing or private context.

The operating test is simple: recurring taste becomes structured rules, tests, and examples; human judgment remains for genuinely new semantics, product trade-offs, and final optical review.
