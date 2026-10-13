# Failure modes and first-principle corrections

## Contents

1. Architecture
2. Components
3. Documentation and agent use
4. Migration and release

## Architecture

| Symptom | Root cause | Global correction |
|---|---|---|
| New catalogue looks like the old noisy Storybook | Existing story discovery was reused without classification | Start with a canonical namespace or clean project; opt review evidence in explicitly |
| A full migration misses affected consumers | Inventory was incomplete for its promised scope | Inventory that scope first; do not expand a bounded audit or fix into a full-system rebuild |
| Agents see hundreds of unusable items | Inventory and public API were merged | Publish a strict ready allow-list separate from exhaustive evidence |
| A design-tool publish changes production immediately | Change detection was mistaken for release authority | Coalesce events, generate a branch, run gates, and require owner merge |
| Visual drift propagates across components | Foundations were not stabilized first | Freeze token roles and global interaction geometry before component scaling |
| A headless library did not fix visuals | Behavioral infrastructure was mistaken for design authority | Use headless primitives for semantics; style from approved tokens and measured references |

## Components

| Symptom | Root cause | Global correction |
|---|---|---|
| Component variants are whole components stacked together | Variant axes were not decomposed | Build small private variable parts, compose one parent, expose meaningful props |
| A responsive component clips or wraps unpredictably | Width screenshots were copied without behavior rules | Contract min/default/max, truncation priority, scroll owner, and resize behavior |
| Demo content appears in production | Stories and components share hard-coded content | Define a typed data model and keep fixtures in stories |
| Interactive control renders but cannot be used | Generated extraction markup lacks events and semantics | Rebuild with native/headless behavior and interaction tests |
| Tooltip, menu, or popover pointer floats inside its surface | Placement semantics and edge geometry are undocumented | Test every rendered side, collision flip, gap, and arrow asset |
| Internal breadcrumb/composer pieces pollute the catalogue | Every design component was published mechanically | Publish only independently reusable families; keep subsets private |
| One workflow-specific composition enters the shared library | A generic folder or Storybook story was mistaken for reuse authority | Keep it feature-local; require a separate owner receipt for shared placement or public promotion |
| Existing shared-library debt keeps growing | The inventory baseline was treated as approval | Treat the baseline as a protected freeze line, never endorsement; new entries need lifecycle approval |
| Agent fixes CSS in each new module | Component/global contract is incomplete | Move repeated fix into tokens, canonical CSS, API, or recipe; prohibit consumer restyling |
| One-off visual exceptions multiply | Feedback was patched locally | Identify the shared dimension—size, stroke, radius, hover, input height—and encode one rule |

## Documentation and agent use

| Symptom | Root cause | Global correction |
|---|---|---|
| Storybook looks complete but agent cannot implement from it | Only rendered stories and prop tables were published | Supply exact source/package, style/type/asset bindings and contracts through an authorized interface |
| Agent uses a stale bundle | Mutable archive is the real interface | Serve versioned artifacts from the stable site and require current-pointer refresh |
| Agent selects a deprecated or review component | Lifecycle wording is descriptive, not enforceable | Fail closed in a machine-readable catalogue and CLI |
| Agent invents unsupported behavior around correct primitives | Composition contract is missing | Document the common semantic composition; keep novel product composition local until approved |
| Inventory shows meaningless names | Extraction labels became canonical names | Use stable IDs and product-language names; preserve raw labels only as provenance |
| Storybook, MCP, and agent files disagree | Each delivery surface became a hand-maintained truth | Generate or validate every surface from one versioned registry |
| A private candidate appears in agent search | Candidate evidence leaked into the public API or hosted context | Keep candidates in a private non-selectable registry and fail if an unapproved candidate reaches `/ai` or MCP selection |
| Product-specific starter screens spread everywhere | Evaluation evidence was published as a reusable component | Keep screens as fixtures and derive small semantic recipes instead |
| Docs say “responsive” or “accessible” but failures recur | Claims are not measurable | Publish exact breakpoints/container rules and interaction/accessibility assertions |
| A Storybook story tests a mock, not runtime code | Documentation was written separately | Import the production component and assert the same exported API |

## Migration and release

| Symptom | Root cause | Global correction |
|---|---|---|
| Production-only patterns are retired accidentally | Missing design mapping was treated as deprecation | Require usage evidence and owner lifecycle decision |
| A zero-consumer report deletes a component | Static or observed usage was mistaken for complete reachability | Open retirement review only; check routes, registries, dynamic consumers and downstream packages, then require owner approval |
| Existing instances break after replacement | API compatibility was ignored | Use adapters/codemods and test representative consumers |
| Generated Storybook copies run as duplicate tests | Build output is inside compiler or test discovery | Exclude generated mirrors and prove the exact CI command against a clean and a populated build directory |
| Hosted site disagrees with repository | Build, revision, registry, and deployment were created at different source states | Build the approved immutable revision and bind receipts/checksums to it; verify live endpoints through the authorized release workflow |
| Agents cannot tell whether a link changed | Stable URL has no release identity | Put semantic version, immutable revision, timestamp, and checksums in `current.json` |
| Review catalogue becomes permanent limbo | Blockers have no owner or gate | Record explicit blockers, owner, decision needed, and readiness criteria |
| Exceptions become permanent local law | Suppressions have no owner, expiry, or mining loop | Use an expiring ledger and promote repeated exceptions into system candidates |
| “Self-healing” changes lifecycle or production silently | Repair capability was mistaken for decision authority | Limit automation to diagnosis, branch repair, verification and PR creation; forbid silent promotion, deletion, baseline acceptance, merge and deploy |

Repeated corrections are a signal to investigate ownership, not proof that both cases
need one component. Compare semantics and visual contracts before proposing promotion.

## Failures in the skill itself

| Symptom | Correction |
|---|---|
| A schema pass is described as release readiness | Report metadata, repository policy, real runtime tests and human visual acceptance separately |
| Private candidates ship through `staticDirs` | Keep authoring outside publication; generate an explicit allow-listed fresh output and test negative URLs |
| A change edits its own baseline to pass | Compare with an immutable protected base and protect checker/workflow changes |
| Different installed copies scaffold incompatible registries | Maintain one authoring source, reconcile unique material, and synchronize reviewed mirrors |
| One project's correction becomes a law for another project | Preserve the failure class; derive colors, dimensions, taxonomy and applicable rules from the target project's authority |
| Removing OLD or Evidence labels is counted as deletion | Verify consumer migration, story information architecture and published/source file deletion independently |
