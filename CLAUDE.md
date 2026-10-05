# CLAUDE.md: working in ethanfoell-skills

**This repo is a generated snapshot, not a working tree.** The skills are authored elsewhere, in a private repo; each public release is exported from it and lands here as one snapshot commit (`chore: export v<version> from <source-sha>`). Nothing in this tree is edited in place, because the next export overwrites it.

What that means in practice:

- **Don't author or edit skills here.** A change committed to this tree never reaches the authoring home and won't survive the next export. If the user wants to adapt a skill, copy its folder into their own project (`npx skills add ethanfoell/skills` does exactly that) and edit the copy.
- **There is no build, lint, or test toolchain here, by design.** Every install surface reads the tree directly: `skills/` + `.claude-plugin/` serve the Claude app's marketplace sync, the Claude Code marketplace, and `npx skills add`; the `.plugin` for the no-marketplace account-upload fallback is built privately.
- **Layout:** skills live at `skills/<bucket>/<skill>/SKILL.md`, with any reference files beside them in the skill folder. Six buckets (`finance/`, `folders/`, `engineering/`, `productivity/`, `meta/`, `misc/`), each with a README listing its skills. `docs/site/` holds the interactive guide's static site.
- **To use the skills**, install per the [README](./README.md); run `/setup-skills-ef` once per repo before the planning-pipeline skills, and `/ask-ef` to find the right skill for a situation.
