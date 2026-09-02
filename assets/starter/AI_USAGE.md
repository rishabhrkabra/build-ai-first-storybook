# Use this design system with coding agents

1. Fetch `/ai/current.json` at the start of every task.
2. Follow its links and verify version, revision, and checksums.
3. Select production components only from `/ai/catalog.json` records whose status is `ready`.
4. Treat `/ai/inventory.json` as evidence, never as a component catalogue.
5. Read the exact source, styles, types, assets, component contract, content rules, design rules, and approved recipes before implementation.
6. Do not deep-import internal components or restyle canonical classes from application code.
7. Report missing components, behaviors, or contradictions instead of inventing reusable APIs.
8. Run the published validation commands before handoff.
9. Turn repeated local exceptions into an evidence-backed design-system gap or candidate; do not normalize them silently.

The hosted interface must contain everything needed for consumption. A separately downloaded archive may be an optional immutable snapshot, never a required source of truth.
