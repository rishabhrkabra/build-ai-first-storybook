# Storybook information architecture

## Contents

1. Catalogue structure
2. Canonical story requirements
3. Review and migration evidence
4. Recipes and evaluation screens
5. Documentation writing rules

## Catalogue structure

One possible top-level order (adapt to the project's audience):

```text
Get Started
Foundations
Components
Patterns & Recipes
Brand
Governance
```

Prefer names readers can predict. Actions, Forms, Navigation, Overlays,
Feedback, Data Display and Layout are examples, not an exhaustive standard.
Identity or Containment may fit another project's taxonomy; do not inherit a
ban from a prior review. Avoid duplicate introductory sections.

Use Brand for identity assets/guidance when helpful, and locate icons where
this project's readers expect them. A distinctive reusable component is still
a component. Branding does not determine implementation ownership.

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

In local/private review, put noncanonical material under an unmistakable review
namespace with a persistent warning and metadata containing:

- lifecycle;
- why it is not selectable;
- replacement when known;
- source path;
- owner or decision needed;
- whether the evidence is temporary;
- the exact deletion condition and what provenance remains afterward.

Do not hide evidence before classification. Do not let evidence appear beside canonical components without a warning.

Track runtime adoption, story classification and artifact retention separately.
A titlePrefix can organize temporary review; it neither removes duplicates nor
migrates consumers. A component without a replacement is not automatically OLD.

Exclude temporary review/visual/engineering evidence from the production story
index and distributed assets before release. Use local/private review builds or
CI/PR artifacts when evidence is still needed. Agree whether removal means
source fixtures, generated assets or hosted routes. Delete source only at the
authorized retention boundary, preserving reusable tests, canonical docs and
required provenance. Do not satisfy deletion by renaming a group.

Verify discovery against the production build's index and asset tree, including
direct URLs. Prefer explicit inclusion scopes. Glob negation and titlePrefix
behavior depend on the installed Storybook version/configuration; test them
rather than universalizing a historical incident.

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
