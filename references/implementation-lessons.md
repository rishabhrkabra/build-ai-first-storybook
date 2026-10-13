# Implementation lessons, with their limits

These are reusable failure classes, not project styling rules.

- **Check relationships in the browser.** Moving visible controls into a hidden
  canvas's inert subtree can pass type/unit checks. Test intended active controls,
  with legitimate inert modal backgrounds and decorative aria-hidden icons as
  counterexamples. jsdom is not a layout engine.
- **Preserve the relevant behavior in doubles.** A null stub can remove the
  interaction between a blocking screen and its parent. Keep the events, mount
  timing and rendered regions the parent responds to, or use an integration test.
- **Prove setup and coverage.** Assert route, fixture and overlay state before
  scanning. Required tests that cannot run do not pass. Report explicit
  inapplicability separately from failure and executed coverage.
- **Test the actual artifact.** If the app consumes built package output,
  rebuild it before measuring. A correct source edit can be absent from the app.
  Run the real CI command and check deployment revision, not a plausible URL.
- **Inspect the cascade, not class names.** Normal unlayered author declarations
  outrank normal layered declarations; utility classes are not necessarily
  layered, and importance changes precedence. Check computed styles and layer
  ordering in this project. A merge utility may also remove earlier classes.
  [CSS cascade reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction).
- **Inspect computed accessible names.** aria-label plus visually hidden text
  does not inherently double a control's name. Naming precedence, references and
  ancestor roles matter. Test the actual accessible name and structure.
  [Accessible name algorithm](https://www.w3.org/TR/accname-1.2/).
- **Make truncation disclosure intentional.** A native title alone is unreliable
  for keyboard/touch and may redundantly repeat unclipped text. Use the project's
  approved accessible disclosure pattern; a universal page-level tooltip is not
  mandatory. Interactive disclosure belongs in a suitable popover, not Tooltip.
- **Bind suppressions to meaning and expiry.** Temporary debt and permanent
  content/asset exceptions are different. Print active suppressions; reject
  expired or orphaned entries. Do not hide current behavior defects in a visual
  debt exemption. Source scanners must parse code or mask comments accurately.
- **Do not mistake documentation for enforcement.** Name the executable gate,
  its supported scope and its negative fixture. A written skill rule is useful
  instruction, but is not an executable guard.
- **Shorten process when justified.** A maintenance change should not inherit a
  full-system launch ritual. Keep the risk-relevant evidence and consent, not
  ceremonial steps. One incident does not establish a universal rule.
- **Show the user the outcome.** Designers need faithful same-state visual
  comparisons, not raw engineering tables. Test counts support the evidence but
  do not substitute for the visible result or human acceptance.

Archive/review build artifacts follow project retention policy. Do not publish
these diagnostic fixtures as reusable components or production catalogue entries.
