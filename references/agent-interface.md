# Agent interface

## Contents

1. Hosted contract
2. Endpoint semantics
3. Component record
4. Cache and release policy
5. Consumption workflow
6. Agent instruction adapters

## Hosted contract

A rendered Storybook is insufficient when agents cannot retrieve exact source, CSS, types, assets, and rules. Publish these from the same stable origin as Storybook.

Avoid a required downloadable archive. Mutable archives create stale local copies and ambiguous update behavior. An archive may exist as an optional snapshot, never as the only complete interface.

## Endpoint semantics

Recommended endpoints:

| Endpoint | Purpose |
|---|---|
| `/ai/current.json` | Release pointer, revision, timestamps, checksums, endpoint map |
| `/ai/catalog.json` | Fail-closed allow-list for production selection |
| `/ai/inventory.json` | Exhaustive source coverage and lifecycle evidence |
| `/ai/context/index.json` | Lightweight index of component contexts |
| `/ai/context/<id>.json` | Selective component API, contracts, provenance, and artifact links |
| `/ai/tokens.json` | Typed design tokens and platform bindings |
| `/ai/content.json` | Structured voice, tone, terminology, and UI-message contracts |
| `/ai/rules.json` | Enforceable consumer rules and detectors |
| `/ai/migrations.json` | Structured API, token, artifact, and behavior changes |
| `/ai/recipes.json` | Approved compositions and page-shell rules |
| `/ai/decisions.json` | Authority conflicts, resolutions, and blockers |
| `/ai/llms.txt` | Short entry point for an unfamiliar agent |

Provide raw source/CSS/type/asset URLs in each ready catalogue record or an equivalent package endpoint.

Publish only allow-listed distributable artifacts. Scan for credentials, private endpoints, restricted fonts, unlicensed assets, and proprietary application code before hosting source.

## Component record

At minimum, a ready component record needs:

```json
{
  "id": "stable-id",
  "name": "Human-facing canonical name",
  "status": "ready",
  "importPath": "@scope/design-system/component",
  "source": ["/ai/source/component.tsx", "/ai/source/component.css"],
  "types": "/ai/source/component.d.ts",
  "assets": [],
  "stories": ["stable-story-id"],
  "contract": {
    "states": [],
    "behavior": [],
    "responsive": [],
    "accessibility": [],
    "composition": []
  },
  "authority": [],
  "tests": []
}
```

Keep `id`, display `name`, and original `sourceName` distinct. Use IDs for lookup, canonical names for humans, and source names only for extraction joins.

## Cache and release policy

- Keep the base URL stable.
- Change semantic version and immutable source revision for every published change.
- Include checksums for catalogue, inventory, recipes, decisions, and source bundles.
- Version every JSON schema and publish migrations when it changes.
- Instruct agents to fetch `current.json` for every new task.
- Do not tell agents to reuse a previously downloaded package without comparing revision and checksums.
- Keep old immutable releases available when consumers need reproducibility.
- Prefer a small index plus per-component context over one enormous agent document.

## Consumption workflow

Tell coding agents to:

1. Fetch `current.json`.
2. Fetch the referenced catalogue and recipes.
3. Select only `ready` records.
4. Read exact component source, types, CSS, and contract.
5. Choose the closest approved recipe.
6. Implement product-specific composition without restyling canonical classes.
7. Run prescribed validation.
8. Report missing primitives or contradictions rather than inventing them.

## Agent instruction adapters

Keep one canonical instruction source. Make Storybook, MCP, `AGENTS.md`, `CLAUDE.md`, or other agent-specific files thin adapters that point to it and restate only surface- or tool-specific commands.

Include rules such as:

- inventory is not a public API;
- review items are not production-selectable;
- never restyle design-system classes from application code;
- prefer composition over local clones;
- file a gap when required behavior is missing;
- refresh the release pointer at task start;
- retain source citations in generated module notes.
