---
name: build-ai-first-storybook
description: Build, rehabilitate, audit, or continuously evolve a design-system Storybook and agent interface so coding agents can safely discover, select, implement, and validate components without private context or a separately downloaded bundle. Use for greenfield design systems, Figma-to-code libraries, Storybook or Chromatic rehabilitation, design-system adherence, agent-facing documentation, machine-readable registries, lifecycle cleanup, public API design, structured content and tone rules, design constitutions, Figma-publish-to-PR automation, component or exception mining, MCP or constrained GenUI planning, responsive and behavioral contracts, visual regression, or Codex/Claude consumption workflows.
---

# Build an AI-first Storybook

**Route:** Mid-tier execution for inventory, schema, implementation, and audit work. Escalate unresolved authority conflicts, destructive lifecycle changes, public API consolidation, and new semantic component decisions to the best available model and the named human owner.

Treat the design system as one structured, versioned design-language model. Storybook is its human review surface, not its sole source of truth. Generate Storybook, agent context, package exports, lint rules, codemods, migrations, and tests from the canonical registry and production code wherever practical. Make the hosted interface sufficient for a fresh coding agent to answer four questions without guessing:

1. What may I use?
2. How must it look and behave?
3. How do components compose into real screens?
4. How do I prove my result still complies?

## Non-negotiable rules

- Separate exhaustive source inventory from the production-selectable public API.
- Generate human documentation, agent contracts, exports, and validation expectations from one canonical registry wherever practical; do not maintain parallel truths.
- Keep Storybook, `/ai`, skills, MCP tools, lint rules, and codemods as generated views or thin operations over that registry; none may become an independent authority.
- Make every selection rule fail closed. Unknown, legacy, deprecated, inventory-only, or unverified items are not production choices.
- Keep visual authority, behavioral authority, and conflict decisions explicit and machine-readable.
- In a migration, make foundations batch zero and the migration unit. Do not migrate component families one by one before the foundation delta is reviewed, because most component changes should inherit from approved foundations.
- Prove each foundation change through one evidence chain: foundation primitive → reusable component → production module → full screen. Token swatches alone cannot establish holistic improvement.
- Rebuild extracted design markup as typed, responsive, semantic components. Do not publish generated extraction JSX as production code.
- Publish the code, styles, assets, contracts, and version metadata through the hosted site. Do not require an agent to remember to redownload a mutable archive.
- Publish only an explicit allow-list of distributable source and assets. Self-contained must never expose secrets, restricted fonts, or proprietary files unintentionally.
- Use one stable site URL and immutable version/revision identifiers inside it.
- Keep internal subset components private unless they have an independent consumer use case.
- Represent interaction, content, responsive behavior, and composition as first-class contracts, not visual notes.
- Route automated source changes through a branch and reviewable proposal. Never let a design-tool event silently change public APIs, behavior, semantics, deletions, or production.
- Treat repeated consumer exceptions as evidence of a missing rule, token, recipe, or component. Require a human decision before merging visually similar instances into one semantic concept.
- Do not claim readiness until automated checks and measured visual QA pass.

## Choose the path

### Greenfield

Create a clean Storybook and import only authoritative sources. Do not seed it with a noisy production Storybook merely to save setup time.

### Rehabilitation

Preserve production-reachable behavior while rebuilding the canonical catalogue. Classify existing stories as canonical, candidate, live-only, legacy, deprecated, internal, or review evidence before hiding or retiring anything.

Never infer deprecation from absence in design files or zero static imports. Require explicit evidence or owner confirmation.

When the Storybook will also be used to repair an existing off-brand interface, treat that as a separate consumer mode from greenfield creation. A catalogue that can generate a new screen is not automatically authoritative enough to rehabilitate an old one. Require an explicit screen recipe, preserved-behavior inventory, atomic shell replacement, before/after evidence, and a fail-closed consumer sidecar. Read [rehabilitating-existing-interfaces.md](references/rehabilitating-existing-interfaces.md) before claiming the system can rehabilitate existing UI.

Read [operating-model.md](references/operating-model.md) before choosing architecture, source precedence, headless primitives, or migration strategy.

## Lock the minimum intake once

Resolve in one pass before implementation:

- target frameworks, runtime, package boundary, and supported browsers;
- visual, behavioral, content, and lifecycle authorities;
- supported themes, platforms, viewports, and container rules;
- accessibility changes that may proceed automatically versus those needing visual approval;
- source/package distribution and hosted access model;
- versioning, release ownership, and migration expectations;
- change-intake surfaces, proposal thresholds, and merge authority;
- who decides contradictions and retirements.

Write unknowns as blockers. Do not rediscover these decisions component by component.

## Execute the workflow

### 1. Establish authority

Record:

- the visual source and its exact version, timestamp, or revision;
- the behavioral source and revision;
- the content/data source when it differs;
- precedence rules for conflicts;
- unresolved decisions and their owner.

Capture real component nodes, polished screens, live behavior, and production-only patterns before implementation. Use screen compositions to validate components; do not use screens as substitutes for reusable components.

### 2. Build an exhaustive inventory

Inventory every known family before selecting what to build. Give each record:

- a stable ID;
- a canonical product-language name;
- original source name and source locator;
- lifecycle and publication status;
- implementation, story, test, documentation, responsive, accessibility, and provenance status;
- duplication or replacement relationships;
- explicit blockers.

Do not expose raw numbered extraction names as display names. Preserve them only for traceability.

### 3. Define the public API

Create a separate allow-list containing only components an agent may select. Use at least:

- `ready`: production-selectable and fully contracted;
- `review`: inspectable but blocked from production selection.

Keep deprecated, legacy, internal, inventory-only, and incomplete families out of the ready catalogue even if their stories remain visible for audit.

### 4. Stabilize foundations

Resolve before any production component migration:

- color roles and prohibited colors;
- typography roles and font delivery;
- spacing, sizing, radii, shadows, borders, and icon geometry;
- light/dark/theme scope;
- desktop/mobile/container breakpoints;
- motion and accessibility rules;
- voice invariants, tone by user moment, terminology, and content-state rules;
- asset identity and source provenance.

Create one before/after foundation matrix before opening component batches. For every changed role, show the legacy and proposed contract, affected components, at least one representative production module, and at least one full screen at the same viewport and state. Keep modules and screens as evaluation fixtures rather than public design-system artifacts.

Turn repeated corrections into global tokens or contracts. Prefer one governing rule over component-specific exceptions. Treat visual approval, lifecycle approval, production adoption, and permission to create a branch or PR as separate gates; one never implies the others.

### 5. Implement component contracts

For every public family, specify:

- semantic purpose and non-goals;
- typed props and controlled/uncontrolled behavior;
- complete state model;
- content and data model;
- responsive and overflow behavior;
- keyboard, focus, form, and assistive-technology behavior;
- composition rules and private subcomponents;
- source evidence and unresolved gaps;
- migration guidance.

Prefer a mature headless primitive for complex interaction when it matches the required semantics and can be styled without visual drift. Headless code supplies behavior, not design authority.

Read [component-contracts.md](references/component-contracts.md) before implementing interactive controls, shells, overlays, navigation, or data-rich patterns.

### 6. Design Storybook for two audiences

Humans need visual review and guidance. Agents need stable identifiers, concise rules, typed APIs, source files, and deterministic data.

Use a small information architecture:

1. Get Started
2. Foundations
3. Components
4. Patterns and Recipes
5. Brand
6. Governance

**Name sections after categories the design world already recognises.** A section invented for the system's own convenience reads as a filing decision rather than a place to look, and every reader has to learn it. Three were removed on exactly that test: `Containment` (nobody groups accordions and cards that way), `Identity` (it held third-party platform marks, which is not what the word means to anyone else), and a `Start Here` sitting beside a `Get Started` that already existed and held the same thing.

**Brand is the section for what could belong to no one else.** Everything in Components and Foundations is a good version of something every product has; the mascot artwork, the wordmark, the proprietary marks are the part that could not be lifted. Interface icons are Foundations — that is where every mature system puts them. An avatar is a component. Test each candidate by asking whether a competitor could ship the same thing: if yes, it is not Brand.

Keep legacy and audit evidence visibly separated from canonical stories. Never place a review component under a generic canonical namespace.

**Prefix the legacy layer in the Storybook config, not in the story files.** A `titlePrefix` on the directory entry ("Old", "Legacy") moves a whole layer in the sidebar without touching a single `title:`, so the diff stays about the migration instead of sweeping 200 unrelated files. Two consequences to write down where the next reader will find them: grepping story sources for that prefix finds nothing, which reads as a phantom build until someone opens the config; and the prefix is the only thing keeping the two layers apart, so anyone reading the sidebar as evidence of what is canonical is reading a config value.

**Storybook's `stories` array does not honour `!` negation globs.** A pattern meant to exclude a directory silently includes everything, and the story count is the only symptom. Name the directories to include instead, and verify against a real build rather than the dev server.

Read [storybook-information-architecture.md](references/storybook-information-architecture.md) before creating or reorganizing stories.

### 7. Publish a self-contained agent interface

Serve stable, cache-safe endpoints from the same deployment as Storybook:

- `/ai/current.json` — version, revision, checksums, and endpoint index;
- `/ai/catalog.json` — production selection allow-list;
- `/ai/inventory.json` — exhaustive evidence, never a selection source;
- `/ai/context/index.json` and `/ai/context/<id>.json` — selective per-component context;
- `/ai/tokens.json` — typed tokens and platform bindings;
- `/ai/content.json` — structured voice, tone, terminology, and UI-message contracts;
- `/ai/rules.json` — enforceable consumer rules;
- `/ai/migrations.json` — structured release migrations;
- `/ai/recipes.json` — validated compositions and screen-shell rules;
- `/ai/decisions.json` — resolved conflicts and open blockers;
- `/ai/llms.txt` — short agent entry point;
- source, CSS, types, and assets for every ready component.

Tell agents to fetch `current.json` at the start of every task and not trust a previously cached copy. Keep one stable URL; put change identity in the response data.

Read [agent-interface.md](references/agent-interface.md) before publishing or documenting consumption.

### 8. Validate and release

Require, in order:

1. registry and link validation;
2. type checking;
3. unit and interaction tests;
4. accessibility checks that do not introduce unapproved visual drift;
5. Storybook production build;
6. responsive fixtures at agreed widths;
7. rendered-page contracts measured in a real browser ([quality-gates.md](references/quality-gates.md));
8. measured reference-versus-render comparison;
9. visual regression baselines;
10. version, migration, checksums, and hosted endpoint verification;
11. a blind cold-start task using only the hosted bootstrap.

Never approve visual parity from memory or a screenshot alone. Compare reference and implementation at the same viewport and state, fix visible mismatches, then compare again.

Read [quality-gates.md](references/quality-gates.md) before declaring a component or release ready.

Read [framework-adapters.md](references/framework-adapters.md) when more than one framework is supported. Read [blind-evaluation.md](references/blind-evaluation.md) before claiming the documentation works for unfamiliar coding agents.

### 9. Operate the learning loop

After release, turn design-tool publishes, application clones, lint exceptions, agent failures, and migration pain into reviewable registry changes:

- coalesce source events and open one evidence-backed branch or PR instead of mutating the main branch;
- automate token values, exact assets, inventory, provenance, documentation, and test candidates when authority is clear;
- require owner approval for semantic naming, public APIs, behavior, consolidation, deletion, and lifecycle changes;
- mine repeated implementations and exceptions into candidates with occurrences, screenshots, behavioral differences, proposed contracts, and migration impact;
- after semantic approval, generate the component or rule, stories, tests, codemod, and versioned migration together;
- keep polished full screens as recipes, evaluation fixtures, and provenance—not exported product modules;
- add MCP only as a thin retrieval or validation facade over the registry; constrain generative UI to approved structured blocks rather than arbitrary JSX or CSS.

Read [continuous-evolution.md](references/continuous-evolution.md) before building Figma-to-PR automation, content schemas, exception governance, component mining, MCP tools, cross-repository migrations, or generative UI.

## Bootstrap reusable contracts

For a new repository, run:

```bash
python3 <skill-dir>/scripts/scaffold.py --target <repo> --name "<Design System Name>" --version 0.1.0
python3 <skill-dir>/scripts/validate.py --root <repo>
```

The scaffold is intentionally framework-neutral and refuses to overwrite an existing contract. Adapt paths, then wire the generated `ai-design-system/` directory into Storybook static assets.

After changing machine artifacts, refresh integrity data before validation:

```bash
python3 <skill-dir>/scripts/update_checksums.py --root <repo>
```

## Definition of done

Finish only when a fresh agent with no conversation history can:

- discover the current release from one stable URL;
- select only ready components;
- distinguish canonical, review, legacy, deprecated, and internal evidence;
- obtain exact source, styles, types, assets, and usage rules;
- choose an approved recipe for a representative screen;
- implement behavior and responsive rules without guessing;
- run the documented validation gates;
- identify unresolved design conflicts rather than inventing answers;
- turn recurring consumer workarounds into owned, evidence-backed system candidates.

Use [failure-modes.md](references/failure-modes.md) when an implementation repeatedly needs manual correction or agents keep making the same mistake.

## Operating rules the first consumers taught

Earned by running a full proposal-grade module through a live system (2026-08), each one the
residue of a real failure:

- **A rule whose only validator is a human is a note, not a guard.** Write the executable check,
  or put the rule in the skill a builder reads before building — ideally both. Audit the registry
  for validators that are named but never implemented; they read as enforcement and enforce
  nothing.
- **Sabotage-test guards**: reintroduce the defect, watch the check fail, restore. A guard that
  has never failed has never been proven.
- **Fences have twins.** Before amending any validator rule, grep for its copies in other
  validators; they drift apart silently and the second one fails you an hour later.
- **Settled and staged never share a file.** The selectable registry holds only approved,
  selectable entries (enforce by schema); drafts live in a separate validated registry that names
  who each awaits, and approvals are receipts — who ruled, when, where.
- **Commission a full fake-data consumer early.** One complete module built only from the public
  contract surfaces the gaps no component test finds — missing primitives, duplicate token
  values, clipped focus rings, scroll regions that should not exist. Its findings ledger is the
  system's best backlog.
- **Prototypes have no dead controls.** A missing backend fakes the data, never the product:
  every control works against an in-memory store, and derived figures (computed, not asserted)
  are what let one action move everything that depends on it.
- **Measure in the browser.** Element widths, scrollHeight vs clientHeight, computed centres.
  Screenshots hide 1px overflows, invisible fills, and reservations for absent siblings.
- **Re-derive process rules when their cost structure collapses.** A review ritual designed for
  week-long manual builds actively harms hour-long agent builds; the rule's justification is the
  part to check, not the rule.

## What a migration into a live product taught (2026-09)

Earned across a fortnight of merging a design-system migration into a moving
application. Each one shipped through green checks first.

### The gap every static check shares

- **A defect can live in the relationship between two files rather than in
  either one.** An `inert` meant to seal a hidden canvas, and a migration that
  moved the covering screen inside it, were each correct alone. Together they
  shipped a screen fully drawn and completely unclickable, through a green
  type-check, zero ownership findings and 8,548 green unit tests. Nothing that
  reads one file at a time can see this. Add a **rendered-page contract** class
  to the gates and keep it small and invariant-shaped: *no element a reader can
  see may sit inside an `inert` or `aria-hidden` subtree*; *nothing scrolls
  sideways unless it says it means to*; *a control row shares one height*;
  *clipped text reveals itself*. Key them on what the reader can perceive, never
  on which element holds the attribute — then any future arrangement fails them
  without anyone predicting the arrangement.
- **A test double must keep the one behaviour the system reacts to.** The screen
  above was stubbed to `() => null` in the only test that rendered it. The real
  component did exactly two things the shell responded to — report that it was
  blocking, and render controls into the shell's main region — and the stub
  removed both, deleting the one arrangement in which the defect exists. Two
  neighbouring tests then asserted the buggy attribute placement and passed,
  writing the bug down as the contract. When you stub, ask what the parent
  reacts to and keep that.
- **jsdom has no layout, and some correct components are invisible in it.** A
  headless slider that hides each thumb until it has measured the track has no
  thumb in jsdom, so its control is outside the accessibility tree and every
  query for it fails. That is a design-system testability property worth
  recording next to the component, not a bug in the consumer's tests.

### Checks that report success without having looked

- **A check that could not run is not a check that passed.** A dead-control scan
  stood down whenever a modal was open — correct in principle, since a modal
  legitimately inerts the page behind it — and then passed on the very bug it
  was written for, because the dialog had not finished opening when the setup
  dismissed it. Make "could not run" its own failure with its own message.
- **Prove coverage, do not assume it.** Six of eight routes in that same scan
  never reached the state they were named for, so they passed without exercising
  anything. Where a case depends on a state, assert the state was reached before
  asserting anything about it.
- **A validator reads prose as code unless told otherwise.** Two checks flagged
  the comment explaining a defect as the defect, so the fix re-raised the
  finding and the only way out was to stop writing the explanation down. Mask
  comments with position-preserving whitespace so line numbers still point at
  real lines.
- **Check what the gate runs, not the nearest command.** `tsc -b --force` is not
  the type-check job; the job also regenerates an inventory. Running the
  cheaper neighbour and reporting the gate green is how a red build reaches the
  owner instead of the author.

### Shipping a migration partial

- **A fail-closed gate needs somewhere to record a decision, and that record
  must expire.** When the owner rules that part of the migration ships
  un-migrated, the options are usually a silenced rule or a promise in a commit
  message; both rot. Build one registry the gates read, holding the ruling
  verbatim, an approver, and a single review date. Enforce three properties
  rather than trusting them: it fails the build once the date passes; an entry
  matching no file is an error, so a rename cannot leave it explaining a
  suppression that stopped happening; and every gate prints what it suppressed,
  because a suppression nobody sees is indistinguishable from a rule nobody
  wrote. List the rules a deferral may cover explicitly — a rule about behaviour
  a reader hits today must not end up inside one by accident.
- **Deferral categories and exemption categories are different things.** An
  allowance meaning "this literal is content and is correct forever" cannot
  carry "this is wrong and we decided to fix it later" without one of the two
  meanings quietly winning.

### The consumer boundary

- **The design system is usually consumed as a built package.** Editing its
  source changes nothing in the application until the package is rebuilt, so a
  fix can be real in the repository and absent from every test and preview.
  Rebuild before measuring, and say which artifact you measured.
- **Unlayered component CSS beats a utility class, so a consumer override
  silently does nothing.** The class is present in the markup, resolves, and
  loses. Publish the axis on the component instead, and gate the dead override
  — it reads as a deliberate difference and is the absence of one.
- **A class-merge helper deletes as well as adds.** A later width utility
  removes the component's default rather than layering over it.
- **Two names for one control is one too many.** An icon-only button given both
  an explicit `aria-label` and visible-but-hidden label text answers to the same
  name twice, and the duplicate leaks upward: an ancestor whose own name is
  computed from its content picks it up.
- **A native `title` is not a truncation reveal.** It fires on hover whether or
  not anything is clipped, so adding one per row to protect long labels puts a
  grey box over every row repeating text the reader can already see. Reveal
  clipped text with one page-level mechanism that measures before it speaks.
- **A hand-rolled control beside published ones does not read as emphasis.** It
  reads as a mistake, because it is one — the reported symptom was "why is there
  a shadow behind this icon", and the answer was that it was the only one of
  three not built from the published button.

### Reporting

- **Verify at the layer the reader experiences, and say which layer you
  checked.** A story is not the product, a passing unit test is not a working
  screen, and a source grep is not the deployed artifact.
- **A preview URL is a claim about a build, not about a branch.** Two hosting
  channels answered for the same pull request after a naming convention changed;
  the stale one kept serving a build from before the work and looked perfectly
  healthy. Publish a build identity the reader can check — the commit the
  artifact came from — and check it yourself before concluding anything from
  what you see.
- **Report in the reader's terms.** A designer asking why an icon has a shadow
  needs the answer, not the test that now guards it. Reporting your own
  machinery instead of their outcome is a way of not answering.

## Stop conditions

Stop and request a decision when:

- visual and behavioral authorities conflict without a precedence rule;
- a production-reachable pattern is absent from design authority and its intended lifecycle is unknown;
- accessibility remediation would materially change an approved visual;
- a destructive migration or component retirement lacks usage evidence;
- visually similar implementations have not been judged semantically equivalent;
- an automation would change behavior, public API, lifecycle, or production without human review;
- a responsive rule, content model, or interaction state cannot be inferred safely;
- deployment access or publication scope is not authorized.
