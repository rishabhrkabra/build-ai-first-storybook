# Framework adapters

Keep the core component contract semantic and map it to each supported framework.

## Core versus adapter

Core identity includes:

- stable component ID and human name;
- purpose and capabilities;
- semantic inputs, outputs, slots, and state;
- behavior, responsive, accessibility, and composition contracts;
- tokens and provenance.

An adapter includes:

- package and import path;
- export, element, or directive name;
- prop/attribute/property bindings;
- event or emit bindings;
- slot bindings;
- type and style artifacts;
- framework-specific setup and peer dependencies;
- compiled examples and tests.

Do not use a React export, Vue name, custom-element tag, filename, or design-tool label as the stable semantic ID.

## Readiness

Declare a framework supported only after a clean consumer can:

1. install or retrieve the declared artifact;
2. import the public entry point;
3. compile a typed example;
4. load required styles and assets;
5. exercise inputs, outputs, and slots;
6. pass interaction and accessibility tests.

One ready adapter does not make all adapters ready. Compute production selectability for the target framework.

The portable v2 starter currently models one framework binding per component record,
not a full multi-adapter release model. For the same semantic component in multiple
frameworks, extend and version the schema/selector with independently verified adapter
records before publishing them; do not duplicate IDs or claim untested adapters ready.

## Avoid overfitting

- Encode observable behavior, not preferred libraries.
- Keep framework-specific tooling out of the semantic contract.
- Allow CSS, native platform tokens, or generated bindings without assuming CSS variables.
- Derive required states from capabilities such as pressable, focusable, selectable, async, overlay, or resizable.
- Keep project-specific extensions under a namespaced `extensions` field rather than expanding the shared schema.
