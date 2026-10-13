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

Avoid decorative props such as `state="hover"` in production APIs. Let actual
pointer/keyboard interaction create transient hover/focus/pressed states. Use real
controlled or internal state for loading, invalid, expanded, selected and disabled
behavior. Story-only state simulation must not substitute for interaction tests.

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

Prefer container queries when behavior depends on allocated width; use viewport
breakpoints for viewport-dependent behavior, including viewport-bound overlays.

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

Use this admission order before creating a family:

1. Reuse a canonical primitive or approved composition that already owns the capability.
2. If behavior is missing, add a justified screen-neutral prop, slot or state to that owner.
3. Keep domain data/state/callback translation in a thin feature-local adapter.
4. Propose a new family only when purpose, behavior or interaction truly differs.

Composites must use DS primitives for the visuals those primitives own. Native
and headless code belongs inside foundational primitives where appropriate;
do not create circular dependencies merely to claim primitive usage. A brand
colour supplied as user content is different from a hard-coded selection token.

Examples: an account-state adapter maps domain statuses to Badge; a numeric
amount adapter keeps parsing/validation while Input owns its field boundary;
an error adapter supplies retry callbacks while Alert owns layout/actions.
Avoid props such as `billingScreen` or `isProjectModal` that conceal visual clones.
Preserve different semantics: a canvas loading screen and a chat generation card
may share progress primitives without sharing the same container or interaction.

Publish a nested element only with a justified independent contract and owner
review. Recurrence is one signal, not a prerequisite for a needed foundational primitive.

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
- applicable hover/focus/pressed/disabled/loading states using real behavior;
- boundary content: empty, long, dense, error, loading;
- responsive fixtures at agreed widths;
- interaction assertions;
- composition examples;
- a source/provenance note;
- at least one realistic recipe or screen context.

Stories are executable specifications. Do not create stories from mock components when the real component exists.
