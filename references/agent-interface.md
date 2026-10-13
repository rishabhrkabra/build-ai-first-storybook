# Agent interface

## Access and source contract

A rendered Storybook alone is insufficient when an agent cannot discover supported
APIs, styling, assets and composition rules. Provide an authorized interface appropriate
to the project: same-origin endpoints, authenticated docs/package registry, or local
artifacts. Do not force proprietary source onto a public site. Provide exact source,
CSS, types and asset bindings or an approved installable package interface, with a
revision and usage contract. A mutable archive must not be the only current source.

Keep one private authoring registry and generate delivery surfaces from it. Read
[portable-contract.md](portable-contract.md) for the shipped v2 scripts, their stricter
local-file mapping format, explicit v1 upgrade and limitations. The package-only
delivery alternative requires an adapter and its own import/build validation; the
supplied file exporter does not implement a package registry.

## Generated endpoints

`/ai` is an example configurable base path, not a requirement. Follow the current
release's endpoint map; never guess URLs or advertise files that were not generated.

| Generated artifact | Purpose |
|---|---|
| `current.json` | Release revision, schema, access mode, checksums, endpoint map |
| `catalog.json` | Ready-only component selection, framework and artifact bindings |
| `context/index.json` | Lightweight index of the same ready IDs |
| `context/<id>.json` | Selective component contract generated from that same record |
| `llms.txt` | Short current-release entry point |
| Explicitly reviewed optional files | Tokens, content rules, consumer rules, migrations, recipes and distributable source/assets |

Inventory, candidates, approval receipts, private authority and unresolved decisions
stay private. Publish a deliberately sanitized summary only when authorized; never
expose these registries wholesale. Source/CSS/type/font licensing and privacy review
apply before export. A manifest field is not server access control.

## Authoring record versus exported record

Use `id` for identity, `name` for a human-facing canonical name and `sourceName` in
private inventory for extraction joins. Use `storyIds` consistently, never a parallel
`stories` field. Private records reference repo-relative local paths. The exporter
turns **approved mapped** paths into URL paths and strips private authority/verification
details. It does not publish every key present in an authoring record.

A declared-ready record binds `framework`, `importPath`, `source`, `styles`, `types`,
`docs`, `storyIds`, `assets` where relevant, and a measurable contract:

- states, including disabled/loading/error/empty where applicable;
- behavior, events, focus and dismissal;
- responsive sizing, overflow and container/viewport ownership;
- accessibility semantics and interaction expectations;
- supported composition and non-goals.

Authoring also records exact tests, authority and revision-bound verification receipts.
The full format lives in the starter and validator; do not invent a second example
schema with different keys. Existence of a receipt is not proof that its checks ran.

## Cache and release

Keep a stable entry point, immutable release identity and exact distributed checksums.
Version schemas and publish upgrade notes. Fetch `current.json` for every new task;
pin the selected revision for that task and explicitly handle changes instead of
mixing artifacts from different releases. Retain immutable releases when required
for reproducibility. Generated candidate output is not a successful deployment:
verify the served files and access controls after approved publication.

## Consumption workflow

1. Read the current pointer through the authorized access path.
2. Read its ready catalogue and any relevant published recipes/rules.
3. Select records for the actual target framework and inspect exact supported APIs.
4. Prefer an existing primitive, then a neutral extension, then an app adapter;
   propose a new semantic family only when those do not express the need safely.
5. Use a relevant approved recipe if one exists. Novel screens may compose supported
   primitives without pretending the new composition is an approved reusable recipe.
6. Keep product data, routing and business logic in the app; do not restyle private
   canonical DOM or invent unsupported props.
7. Run target-project validation and report gaps, blocked checks and source conflicts.

## Thin agent adapters

Storybook, MCP, `AGENTS.md`, `CLAUDE.md` and skills should point to the same versioned
contracts. Keep only surface/tool-specific instructions in adapters. A skill advises;
repository and protected CI checks enforce admission. MCP exposes tools and context,
not authority to promote, retire, accept visual baselines, merge or deploy. Distinguish
configured tools from a tool actually exercised and a repair loop actually tested.
