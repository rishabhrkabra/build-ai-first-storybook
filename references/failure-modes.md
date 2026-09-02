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
| Only specifically requested components exist | Work followed prompts instead of exhaustive source inventory | Inventory first; sequence implementation by foundations, primitives, composites, recipes |
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
| Agent fixes CSS in each new module | Component/global contract is incomplete | Move repeated fix into tokens, canonical CSS, API, or recipe; prohibit consumer restyling |
| One-off visual exceptions multiply | Feedback was patched locally | Identify the shared dimension—size, stroke, radius, hover, input height—and encode one rule |

## Documentation and agent use

| Symptom | Root cause | Global correction |
|---|---|---|
| Storybook looks complete but agent cannot implement from it | Only rendered stories and prop tables were published | Host exact source, CSS, types, assets, contracts, and recipes |
| Agent uses a stale bundle | Mutable archive is the real interface | Serve versioned artifacts from the stable site and require current-pointer refresh |
| Agent selects a deprecated or review component | Lifecycle wording is descriptive, not enforceable | Fail closed in a machine-readable catalogue and CLI |
| Agent invents layout around correct primitives | No approved screen recipe exists | Derive recipes from polished screens with component and responsive mappings |
| Inventory shows meaningless names | Extraction labels became canonical names | Use stable IDs and product-language names; preserve raw labels only as provenance |
| Storybook, MCP, and agent files disagree | Each delivery surface became a hand-maintained truth | Generate or validate every surface from one versioned registry |
| Product-specific starter screens spread everywhere | Evaluation evidence was published as a reusable component | Keep screens as fixtures and derive small semantic recipes instead |
| Docs say “responsive” or “accessible” but failures recur | Claims are not measurable | Publish exact breakpoints/container rules and interaction/accessibility assertions |
| A Storybook story tests a mock, not runtime code | Documentation was written separately | Import the production component and assert the same exported API |

## Migration and release

| Symptom | Root cause | Global correction |
|---|---|---|
| Production-only patterns are retired accidentally | Missing design mapping was treated as deprecation | Require usage evidence and owner lifecycle decision |
| Existing instances break after replacement | API compatibility was ignored | Use adapters/codemods and test representative consumers |
| Hosted site disagrees with repository | Build, revision, registry, and deployment were created at different source states | Commit once, build and package that exact revision, publish checksums, verify live endpoints |
| Agents cannot tell whether a link changed | Stable URL has no release identity | Put semantic version, immutable revision, timestamp, and checksums in `current.json` |
| Review catalogue becomes permanent limbo | Blockers have no owner or gate | Record explicit blockers, owner, decision needed, and readiness criteria |
| Exceptions become permanent local law | Suppressions have no owner, expiry, or mining loop | Use an expiring ledger and promote repeated exceptions into system candidates |

When the same correction appears twice, treat it as a design-system defect rather than an application exception.
