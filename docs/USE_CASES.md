# Detect Agent Skills drift across coding agents

A package manager can report successful installation even when a target link is absent or copied files diverge. Public issue reports illustrate this class of failure: [broken links with symlinked catalogs](https://github.com/vercel-labs/skills/issues/481), [missing project-scoped Claude Code link](https://github.com/vercel-labs/skills/issues/1355). These reports document specific setups, not proof that every current version is affected. SkillParity is an independent read-only diagnostic, not a replacement for an installer or an affiliation with those projects.

## 1. Compare a shared catalog with a separate Claude Code catalog

Select existing local roots. The OpenAI CLI docs list `.agents/skills/` for Codex project scope, and the [Vercel Skills agent documentation](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) describes agent-specific locations. Actual installations vary; some agents deliberately share the same directory.

```sh
skillparity check --baseline shared --root shared=.agents/skills --root claude=.claude/skills --summary
```

If both paths resolve to the same catalog, parity is expected by construction; this does not prove either agent discovers or invokes the skill. If a root does not exist, the CLI returns 2, not a successful empty result. Do not create missing directories just to make a check pass.

## 2. Make a reproducible drift fixture

Run `skillparity demo` to see a removed supporting file and a changed supporting file. The demo intentionally returns 1. It neither installs nor executes skills.

## 3. Prevent drift in a team's GitHub CI

Commit the baseline and target catalogs under the same workspace and a JSON config that references them. Use the pinned example in [CI integration](CI_INTEGRATION.md). Run on an isolated Linux runner with minimal permissions and no secrets. The action returns 1 for drift, 2 for incomplete verification. It reports aggregate counts rather than file names.

## 4. Report a real problem safely

Try a synthetic reproduction first. Share OS, Python version, agent names and expected/actual exit code in [the early-adopter feedback thread](https://github.com/splucasaugusto666/skillparity/issues/1). Do not expose skill contents or private paths.

## What this does not establish

Matching file paths and bytes is not proof of semantic equivalence, agent discovery, or secure skill content. SkillParity does not repair links, run skill scripts, validate instructions, or certify third-party installers.
