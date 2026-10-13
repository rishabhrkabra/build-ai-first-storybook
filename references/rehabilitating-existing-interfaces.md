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

Infer mode from the explicit request and repository evidence, then record it
when automation needs it. Ask only if ambiguity would materially change scope.

## Fail-closed task declaration

For substantial rehabilitation with automated consumer gates, record a small
task declaration, for example `design-system.screen.json`. An audit or bounded
maintenance task does not need an unrelated screen recipe or sidecar:

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

The schema is project-specific. CI must check the declared scope and evidence
required for that task. Use a ready recipe when one fits; otherwise identify the
composition gap and propose a recipe without calling it canonical. Do not block
safe unrelated work just because a novel composition awaits approval.

## Mandatory rehabilitation workflow

1. Capture the existing interface at named viewports and meaningful states.
2. Inventory behavior into `preserve`, `replace`, and `decision required`.
3. Refresh the current design-system release; use a relevant ready recipe if one fits, otherwise compose supported primitives and record the gap.
4. Map existing regions to canonical owners: shell, navigation, selection, forms, overlays, data display, and conversation.
5. Replace design-system-owned composites atomically. Do not cosmetically patch a cloned shell.
6. Apply semantic tokens and documented layout/radius roles to product-owned content.
7. Run static consumer validation before visual review.
8. Capture the same states and viewports after the change.
9. Compare before, after, and authority reference together.
10. Record consumer workarounds; recurrence opens review for a component, token,
    rule or recipe. It does not automatically promote one.

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

Publish a canonical choice primitive when the same selection contract recurs.
Validate against the project's semantic selection tokens; do not impose another
project's colours or assume an inverse appearance is universally wrong.

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

State the project's optical nesting rules and exceptions. Relating radii to
inset often improves nested surfaces; it is not a universal prohibition on inner
pills or other independent shapes. Document which border/shadow creates each
separation, and avoid accidental stacked surfaces.

### Complete composite presets

If a composite has a common required configuration, expose a named preset rather than many independent booleans. The preset should guarantee all required collaborators, utilities, actions, or destinations. Keep low-level configuration only for genuinely distinct approved scenarios.

## Consumer validation rules

Configure static validation for the agreed scope to reject:

- missing task declaration when the project requires it for this task, or a claimed approved recipe that does not exist;
- local clones of canonical shell components;
- arbitrary design-system selector overrides;
- selection states that contradict the approved semantic selection contract (shared token values are not inherently invalid);
- hard-coded spacing, radii, shadows, colors, or typography where semantic roles exist;
- visible replacement controls for behavior the canonical component already owns;
- missing required shell regions or utilities;
- stale or review-only imports;
- missing before/after evidence at handoff.

Use local, explicit suppressions only when they include a reason and an owner. Do not permit global waivers.

Static checks cannot prove visual quality, but they can prevent predictable structural failures before human review.

## Storybook requirements

For a system that supports rehabilitation workflows, provide discoverable guidance with:

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
- the stable authorized design-system interface (hosted, package or local);
- a requirement to preserve behavior;
- no expected component list or known-defect list.

Automatic failures include:

- only colors and typography change when structural replacement was required;
- a canonical shell remains locally recreated;
- required navigation or utilities disappear;
- persistent choices contradict the project's approved selection contract;
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

Repeated manual correction is a signal to inspect the shared contract, not an
automatic finding that different workflows need the same component.
