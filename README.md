# build-ai-first-storybook

A Claude Code skill for building design systems that coding agents can actually use.

## What it does

Most Storybooks are written for humans. An agent pointed at one has to guess what it may use, how components behave, and whether its output complies — and it guesses wrong in ways that look right.

This skill guides an agent through building, rehabilitating, or auditing a design-system Storybook **plus a machine-readable agent interface**, so that a fresh coding agent with no project history can:

- discover the current release from one stable URL;
- select only production-ready components, fail-closed — unknown, legacy, deprecated, or unverified items are never valid choices;
- pull exact source, styles, types, tokens, assets, and usage rules;
- compose real screens from approved recipes instead of inventing layout;
- prove its result still complies by running the system's own validation gates.

The design system is treated as one canonical, versioned registry. Storybook, the hosted `/ai` endpoints, lint rules, and agent docs are generated views over that registry — no hand-maintained parallel truths.

## Who it's for

- Design-system engineers pointing coding agents (Claude Code, Codex, and similar) at a component library.
- Teams whose Storybook is complete for humans and useless for agents.
- Anyone rehabilitating a drifted Storybook or Chromatic setup, or repairing an off-brand interface against a design system.
- Teams planning Figma-publish-to-PR automation, MCP facades over a design system, or constrained generative UI.

## Install

This is a [Claude Code](https://claude.com/claude-code) skill. Drop the repo into a skills directory:

```bash
# available in every project
git clone https://github.com/rishabhrkabra/build-ai-first-storybook ~/.claude/skills/build-ai-first-storybook

# or scoped to one project
git clone https://github.com/rishabhrkabra/build-ai-first-storybook <project>/.claude/skills/build-ai-first-storybook
```

Claude Code discovers it automatically from the `SKILL.md` frontmatter. Ask for design-system or Storybook work and it loads, or invoke it directly with `/build-ai-first-storybook`.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The workflow: authority, inventory, public API, foundations, contracts, Storybook IA, hosted agent interface, validation, learning loop, stop conditions. |
| `references/` | Deep dives loaded on demand: operating model, component contracts, Storybook information architecture, the hosted agent interface, quality gates, rehabilitating existing interfaces, continuous evolution, framework adapters, blind evaluation, failure modes. |
| `scripts/` | Stdlib-only Python: `scaffold.py` creates a framework-neutral starter contract, `validate.py` checks it, `update_checksums.py` refreshes integrity hashes. |
| `assets/starter/` | The starter contract: manifest, inventory, public API, context index, tokens, content, rules, recipes, migrations, decisions, release, and an `llms.txt` agent entry point. |
| `agents/openai.yaml` | Display metadata for OpenAI-compatible agent runners. |

## Born from

Distilled from building and operating a production design system's agent interface — every rule in it is the residue of a real failure that shipped through green checks first.

## License

MIT — see [LICENSE](LICENSE).
