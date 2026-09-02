# Rehabilitating existing interfaces

Greenfield creation and existing-UI rehabilitation are different design-system tasks.

## Contents

1. The core distinction
2. Fail-closed task declaration
3. Mandatory rehabilitation workflow
4. What the design system must own
5. Consumer validation rules
6. Storybook requirements
7. Blind evaluation
8. What still needs human judgment

In greenfield work, the design system supplies the starting structure. In rehabilitation, an existing interface already contains plausible-looking markup, behavior, layout, and local styles. An agent will preserve that structure unless the design system explicitly tells it what must be replaced. Token adoption alone can therefore make a weak interface look branded without making it correct.

## The core distinction

| Mode | Primary risk | Required authority |
|---|---|---|
| Greenfield | The agent invents missing structure | Ready components, recipes, responsive rules, and examples |
| Rehabilitation | The agent preserves incorrect structure | Everything required for greenfield, plus a replacement map, structural invariants, and before/after validation |

Never infer the mode from prose or repository history. Require it as machine-readable task metadata.

## Fail-closed task declaration

Require a small sidecar in every consumer repository, for example `design-system.screen.json`:

```json
{
  "schemaVersion": 1,
  "taskMode": "rehabilitation",
  "recipeId": "workspace-with-navigation-and-panel",
  "entrypoints": ["src/screens/Workspace.tsx"],
  "preserve": ["business rules", "data fetching", "route transitions"],
  "replace": ["application shell", "selection controls", "layout grammar"],
  "evidence": {
    "before": ["artifacts/before-1440x900.png"],
    "after": ["artifacts/after-1440x900.png"]
  }
}
```

The exact schema is system-specific, but the invariant is not: missing task mode, missing ready recipe, or missing evidence must fail validation. A command-line flag is insufficient because an agent can forget or omit it.

## Mandatory rehabilitation workflow

1. Capture the existing interface at named viewports and meaningful states.
2. Inventory behavior into `preserve`, `replace`, and `decision required`.
3. Refresh the current design-system release and resolve one ready composition recipe.
4. Map existing regions to canonical owners: shell, navigation, selection, forms, overlays, data display, and conversation.
5. Replace design-system-owned composites atomically. Do not cosmetically patch a cloned shell.
6. Apply semantic tokens and documented layout/radius roles to product-owned content.
7. Run static consumer validation before visual review.
8. Capture the same states and viewports after the change.
9. Compare before, after, and authority reference together.
10. Record every consumer workaround; promote repeated workarounds into a component, token, rule, or recipe.

## What the design system must own

### Structural invariants

For every application shell recipe, publish exact rules such as:

- region order and row/column ownership;
- fixed versus fluid dimensions;
- required versus optional utilities;
- navigation topology and item limits;
- scroll owners and containment boundaries;
- resize affordance and constraints;
- responsive behavior based on viewport or container;
- which regions consumers may configure and which they may not replace.

Prefer a typed composite that renders canonical regions from configuration. Arbitrary `ReactNode` slots make cloning easy and validation weak.

### Semantic state language

Actions and selections are different concepts.

- Actions use action components and action tokens.
- Persistent selection uses selection components and selection tokens.
- Current navigation uses navigation-current semantics.
- Hover and focus are transient and must not be mistaken for persistent selection.

Publish one canonical choice primitive when the same selected-pill or selected-card language recurs. Consumer validation should reject action-primary or inverse tokens inside selected states.

### Layout grammar

Tokens alone do not create hierarchy. Publish roles for:

- page gutter;
- section gap;
- group gap;
- item gap;
- section padding;
- nested-surface padding;
- maximum readable width;
- dense-table exceptions.

Document their intended nesting. An agent should be able to distinguish a page section, a group within that section, and repeated rows inside the group without inventing spacing.

### Radius and elevation grammar

Publish radius roles by semantic depth, not one generic radius scale:

- outer section or dialog;
- nested card or field group;
- control;
- pill;
- icon-only action;

State the optical nesting rule. Inner corners must be smaller than outer corners, and the radius difference should relate to the inset. Do the same for borders and shadows: only one layer should create separation unless the reference explicitly requires more.

### Complete composite presets

If a composite has a common required configuration, expose a named preset rather than many independent booleans. The preset should guarantee all required collaborators, utilities, actions, or destinations. Keep low-level configuration only for genuinely distinct approved scenarios.

## Consumer validation rules

Static validation should reject, at minimum:

- missing task declaration or unknown recipe;
- local clones of canonical shell components;
- arbitrary design-system selector overrides;
- selection states styled with primary-action tokens;
- hard-coded spacing, radii, shadows, colors, or typography where semantic roles exist;
- visible replacement controls for behavior the canonical component already owns;
- missing required shell regions or utilities;
- stale or review-only imports;
- missing before/after evidence at handoff.

Use local, explicit suppressions only when they include a reason and an owner. Do not permit global waivers.

Static checks cannot prove visual quality, but they can prevent predictable structural failures before human review.

## Storybook requirements

Include a dedicated `Rehabilitate Existing UI` entry with:

- task-mode decision table;
- sidecar schema and runnable validation command;
- ready rehabilitation recipes;
- action-versus-selection comparison;
- shell replacement example;
- layout and radius grammar;
- before/after evidence requirements;
- automatic-failure list;
- the boundary between system-owned decisions and human review.

Do not bury these rules in prose alone. Publish their machine-readable equivalents beside the human story.

## Blind evaluation

Test rehabilitation separately from greenfield creation.

Give a fresh agent:

- a deliberately off-brand but functional interface;
- the stable hosted design-system bootstrap only;
- a requirement to preserve behavior;
- no expected component list or known-defect list.

Automatic failures include:

- only colors and typography change;
- a canonical shell remains locally recreated;
- required navigation or utilities disappear;
- persistent choices use primary-action styling;
- custom resize controls appear for canonical resize behavior;
- dense content remains an undifferentiated ledger;
- nested radii or spacing contradict the documented grammar;
- the agent cannot show before/after evidence at the same viewport and state.

Score structure, selection semantics, hierarchy, responsive behavior, preserved behavior, and validation discipline separately from visual attractiveness.

## What still needs human judgment

A robust design system can encode most repeated quality:

- shell completeness;
- component choice;
- state language;
- spacing and radius hierarchy;
- icon geometry;
- responsive and interaction behavior;
- accessibility and validation.

Human judgment remains valuable for genuinely novel information architecture, priority and emphasis, content-specific density exceptions, and final optical review. Do not use “taste” as an excuse for a missing repeated rule.

When two rehabilitation tasks need the same manual correction, the design system is incomplete.
