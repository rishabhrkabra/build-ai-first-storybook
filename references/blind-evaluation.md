# Blind evaluation

Documentation is ready only when a fresh coding agent succeeds without leaked project history.

## Setup

- Use a clean temporary repository and a new agent session.
- Provide the authorized bootstrap interface (hosted, authenticated, package or local) and a realistic module brief.
- Do not provide the expected component list, known defects or prior conclusions. Supply the ordinary access/dependencies a real consumer is allowed to use; do not create artificial access failures.
- Choose representative supported capabilities. A full-system test can cover foundations, components, a recipe, responsiveness and an interaction. A bounded maintenance test should target its changed contract instead.

## Required agent behavior

The agent must:

1. refresh the current release pointer;
2. select only ready components for its target framework;
3. cite the chosen components and relevant approved recipe, if one exists;
4. retrieve exact source/package, styles, types, and assets;
5. identify missing capabilities as gaps rather than inventing reusable APIs;
6. implement responsive fixtures and behavior tests;
7. run consumer validation.

## Automatic failures

- trusts cached or mutable downloaded context;
- selects review, legacy, deprecated, internal, or inventory-only records;
- deep-imports or reaches into private DOM;
- restyles canonical selectors from application code;
- invents undocumented props, breakpoints, tokens, states, or recipes;
- claims responsiveness from one screenshot;
- cannot build through the project's documented authorized consumption interface;
- ignores a documented contradiction or blocker.

## Score separately

Score:

- discovery and correct selection;
- API and behavior fidelity;
- visual and responsive fidelity;
- composition quality;
- validation discipline;
- documentation gaps encountered.

Do not let an attractive output hide documentation failure. Record every application-level workaround; repeated workarounds should become design-system fixes.

Separate missing system capabilities from bad consumer choices. A novel screen made
from supported primitives is not a failed evaluation merely because no named recipe
exists. If independent-agent evaluation is unavailable, label a local synthetic
forward test as such; do not claim blind-agent success.

Forward-test on unrelated systems and frameworks before treating the skill itself as general. Use raw project artifacts, never the intended answers.
