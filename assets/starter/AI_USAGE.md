# Use this design system with coding agents

1. Fetch the configured current-release URL at task start (commonly `/ai/current.json`; nested sites can use `/storybook/ai/current.json`). Use approved authentication when required.
2. Follow its links and verify version, revision, and checksums.
3. Select production components only from the pointer's catalogue records whose status is `ready` for the target framework.
4. Private inventory and candidates never grant selectability and are not published by default.
5. Read the relevant source/package, styles, types, assets and contracts through the approved access path. Use applicable published rules and recipes; a novel app composition is not automatically a reusable recipe.
6. Do not deep-import internal components or restyle canonical classes from application code.
7. Report missing components, behaviors, or contradictions instead of inventing reusable APIs.
8. Run the published validation commands before handoff.
9. Turn repeated local exceptions into an evidence-backed design-system gap or candidate; do not normalize them silently.
10. Start workflow-specific UI in its owning feature. Repetition opens candidate review; it does not grant shared or public placement.
11. Treat zero consumers as a retirement-review signal, never permission to deprecate or delete.

The authorized interface can be local, authenticated or public. It must supply the documented consumption contract without hidden project history. A mutable archive must not be the only current source of truth.

This directory is private authoring input. Never add it to Storybook staticDirs.
Only export_public.py output is distributable; generation does not authorize deployment.
Validator success establishes metadata structure only unless a trusted-base policy
check also runs. Neither authenticates approvals nor executes browser/build tests.
