# Market research — 2026-11-23

## Observed signals

GitHub Trending: https://github.com/trending
Independent 30-day trending sample, 199 repos, including 49 AI coding add-ons: https://trend.ondo.sh/github/r/en.html
Seven-day star additions reported by that tracker: Claude-BugHunter 12,161; Superpowers 6,269; mattpocock/skills 5,417; Ponytail 5,393; last30days-skill 5,305; addyosmani/agent-skills 1,704. These are tracker-reported interval counts, not all GitHub projects or proof of usage. Creation dates, first releases, historical low-growth controls and causal attribution were not established. No contributor-density or fork-rate inference was made.

## Problem evidence

- https://github.com/vercel-labs/skills/issues/1812 — reported installed-content drift.
- https://github.com/vercel-labs/skills/issues/1517 — reported lost sibling files on update.
- https://github.com/vercel-labs/skills/issues/1290 — reported per-agent variant handling.
- https://github.com/vercel-labs/skills/issues/456 — reported broken relative symlinks.
- https://www.reddit.com/r/ClaudeAI/comments/1y3n4qg/how_are_you_sharing_and_versioning_agent_skills/ — current discussion of cross-agent drift.

These are reports of experienced problems, not proof that the bugs remain open or affect current releases.

## Alternatives

Vercel Skills already supports install/check/lockfile workflows; skilllock and skill-lock also verify changes. Agent-parity and agent-config-sync manage shared configurations. skillscout inventories skills. Therefore a generic installer, lockfile or linter is not a meaningful novelty claim. SkillParity focuses on explicit-root, read-only comparison of actual local files with an immediate matrix-like report and no runtime dependencies. This is a narrow positioning hypothesis, not a claim of unique functionality.

https://github.com/vercel-labs/skills/blob/main/docs/commands.md
https://github.com/lz1834career/skilllock
https://github.com/techdevfun/skill-lock
https://github.com/libkim/agent-parity
https://github.com/thawee/skillscout
https://github.com/agent-ecosystem/skill-validator

## Opportunity triage

15 initial concepts: cross-agent skill parity; skill package reference linter; skill lockfile diff; skill frontmatter repair; prompt duplicate detector; MCP configuration validator; context budget profiler; model cost estimator; local RAG fixture generator; agent evaluation harness; action pinning audit; API fixture scrubber; shell command documentation checker; dependency license summary; offline README demo generator.

Five illustrative finalists. Scores are analyst judgments, not measured market demand. Criterion order: demand 20%, utility 15%, differentiation 15%, organic growth 15%, day-zero feasibility 15%, demo 10%, international 5%, professional relevance 5%.

| Candidate | D | U | Diff | G | F | Demo | I | P | Weighted /10 |
|---|---|---|---|---|---|---|---|---|---|
| Skill parity | 8 | 9 | 6 | 8 | 10 | 9 | 9 | 8 | 8.30 |
| Skill reference lint | 8 | 8 | 4 | 7 | 10 | 8 | 9 | 7 | 7.55 |
| Skill lockfile diff | 8 | 8 | 4 | 7 | 8 | 8 | 9 | 8 | 7.30 |
| Context budget profiler | 6 | 8 | 5 | 7 | 7 | 8 | 9 | 8 | 6.90 |
| MCP configuration validator | 6 | 8 | 4 | 7 | 8 | 8 | 9 | 8 | 6.90 |

Adversarial review: parity may be redundant for teams using one canonical symlink; test whether heterogeneous or intentionally copied installations need it. Reference lint has established validators and adds little. Lockfile diff has direct competitors and a format-maintenance burden. The narrow parity tool is feasible without paid APIs but its demand remains to be validated by independent users. No broad market-size estimate or trademark clearance.
