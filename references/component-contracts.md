# Component contracts

## Contents

1. Required contract
2. State modelling
3. Responsive rules
4. Interaction and accessibility
5. Composition and publication
6. Story fixtures

## Required contract

Every public component must document:

```text
Purpose
Non-goals
Source evidence
Typed API
State model
Content/data model
Behavior
Responsive/overflow rules
Accessibility
Composition rules
Visual tokens
Known gaps
Migration notes
Validation coverage
```

Avoid decorative props such as `state="hover"` in production APIs. Let native interaction create hover, focus, pressed, disabled, loading, invalid, expanded, and selected states. Use visual-state props only in stories when the browser cannot deterministically produce a state for review.

## State modelling

Inventory state axes before writing variants:

- semantic variant;
- size;
- interaction state;
- selection or progress state;
- content density;
- leading/trailing media;
- validation status;
- open/closed placement;
- user role or mode;
- responsive mode.

Compose variable subcomponents inside one parent. Do not stack multiple complete parent components and call the result a variant set.

Use discriminated unions when states have different required data. A chat transcript, table row, card, notification, or generation event should have a typed content model rather than visibility booleans around hard-coded demo content.

## Responsive rules

Document behavior, not just screenshots:

- width model: fixed, intrinsic, fluid, resizable, or container-bound;
- min/default/max width;
- height model and viewport offsets;
- wrapping versus truncation priority;
- scroll owner and sticky regions;
- element order under pressure;
- placement and collision behavior;
- supported viewport/container fixtures.

Use container queries when behavior depends on the component’s allocated width. Use viewport breakpoints only for page-level decisions.

For resizable components, specify pointer and keyboard resizing, clamp rules, persistence, and re-clamping after viewport change.

## Interaction and accessibility

- Use semantic controls (`button`, `input`, `textarea`, `select`, landmarks) or proven headless primitives.
- Support keyboard operation and visible focus.
- Expose expanded, selected, current, invalid, busy, progress, and value semantics.
- Make icon-only controls have accessible names.
- Return focus after dismissed overlays when appropriate.
- Test outside click, Escape, Tab, arrow-key navigation, Home/End, and form submission where relevant.
- Preserve native text editing expectations: Enter, Shift+Enter, composition events, selection, and auto-growth.
- Add accessibility improvements freely when they do not change approved visuals. Escalate material visual drift.

## Composition and publication

Publish a nested element only when it has a plausible independent consumer.

Keep private:

- breadcrumbs tied to one shell contract;
- component-specific composer rows;
- internal message renderers;
- one-off dropdown sections;
- layout spacers and Figma extraction fragments.

Publish when independently reusable:

- identity assets;
- generic buttons and controls;
- common avatar or icon systems;
- validated cards or patterns with their own contract.

Expose slots or data arrays instead of requiring consumers to reach into internal DOM.

## Story fixtures

Every ready component should include:

- a controlled playground;
- every semantic variant and size;
- native hover/focus/pressed/disabled/loading states;
- boundary content: empty, long, dense, error, loading;
- responsive fixtures at agreed widths;
- interaction assertions;
- composition examples;
- a source/provenance note;
- at least one realistic recipe or screen context.

Stories are executable specifications. Do not create stories from mock components when the real component exists.
