# Storybook information architecture

## Contents

1. Catalogue structure
2. Canonical story requirements
3. Review and migration evidence
4. Recipes and evaluation screens
5. Documentation writing rules

## Catalogue structure

Prefer this top-level order:

```text
Get Started
Foundations
Components
Patterns & Recipes
Brand
Governance
```

Name every section after a category the design world already recognises. A
section invented for the system's own convenience is a filing decision the
reader has to learn. Three failed that test in review and were removed:
`Containment` (nobody groups accordions and cards under one word),
`Identity` (it held third-party platform marks, which is not what the word
means to anyone else), and a `Start Here` sitting beside an existing
`Get Started` that held the same thing.

Brand holds what could belong to no one else — mascot artwork, the wordmark,
proprietary marks. Everything in Components and Foundations is a good version of
something every product has. Interface icons are Foundations, where every mature
system puts them; an avatar is a component. The test for a candidate is whether
a competitor could ship the same thing.

Keep component categories semantic: Actions, Forms, Navigation, Overlays, Feedback, Data Display, Layout, Conversation, or domain-neutral equivalents. `Identity` is deliberately absent from that list.

Avoid exposing the repository’s folder history as information architecture.

## Canonical story requirements

For each ready component, make Docs answer:

- when to use it;
- when not to use it;
- exact import path;
- typed props and defaults;
- interaction and keyboard behavior;
- responsive behavior;
- composition rules;
- source authority and current version;
- known constraints;
- migration notes.

Make stories deterministic. Use fixed fixtures, seeded data, stable dates, and local assets. Avoid network-dependent examples in visual regression.

Use stable story IDs. Renaming a human-facing title should not silently break agent links.

## Review and migration evidence

Put all noncanonical material under an unmistakable review namespace. Add a persistent warning in the canvas and metadata containing:

- lifecycle;
- why it is not selectable;
- replacement when known;
- source path;
- owner or decision needed;
- whether the evidence is temporary;
- the exact deletion condition and what provenance remains afterward.

Do not hide evidence before classification. Do not let evidence appear beside canonical components without a warning.

Migration Review, where it exists, is a working surface and not a permanent
museum — and it belongs in source rather than in the hosted catalogue, which is
a production-facing surface. Review packets and proposals stay checked in and
stay out of the published index. After the approved production adoption is merged, deployed, and verified against the recorded behavior and visual evidence, delete the temporary Storybook review group. Retain the canonical component documentation, versioned migration entry, and required release provenance.

## Recipes and evaluation screens

Components alone do not teach layout. Publish validated recipes for repeated compositions such as:

- application shell;
- navigation plus content plus side panel;
- form/input screen;
- results screen;
- empty/loading/error states;
- modal or drawer workflow;
- dense list or table.

Each recipe must state required components, layout rules, responsive behavior, allowed substitutions, and source evidence. Derive recipes from polished approved screens, not invented generic dashboards.

Do not force optional shells into every starter. Record when panels, sidebars, breadcrumbs, or utilities enter or leave a flow.

Keep full product screens as evaluation targets, visual-regression fixtures, provenance, and good/bad rehabilitation evidence. Do not export a product-specific “module starter” as a public design-system component; it freezes one information architecture and encourages agents to copy an example as a standard.

## Documentation writing rules

- Lead with rules and copy-ready examples.
- Use canonical product-language names.
- Show raw source/export names only as provenance.
- Distinguish defaults from examples.
- State negative rules explicitly: “Do not use,” “Only for,” “Always,” “Never.”
- Avoid vague labels such as “responsive,” “accessible,” or “flexible” without measurable behavior.
- Keep documentation close to the component and derive machine data from the same source where practical.
- Ensure every link works in the production static build, not only in local development.
