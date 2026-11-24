# SkillParity

**Same skill name. Different agent. Same files?**

A dependency-free, read-only CLI that compares Agent Skills directories across coding tools against a source of truth. It reports missing skills, extra skills, changed files, and broken or unapproved symlinks without executing a single skill or modifying your installations.

## Demo

Run `python skillparity.py demo` (Python 3.10+):

```text
SkillParity | baseline: "source"
"review"
  source: MATCH (directory)
  claude: DRIFT (directory)
    removed: "checklist.md"
  codex: DRIFT (directory)
    changed: "checklist.md"
```

The demo intentionally exits with code 1 to illustrate a failed parity check. It uses temporary synthetic fixtures, not actual agent installations.

## Why this exists

Teams increasingly share `SKILL.md` packages across coding agents. A skill can be installed under the same folder name in multiple locations while its supporting files differ. Installers and lockfiles are useful; sometimes you just want to compare what is actually on disk, without changing it.

SkillParity is not an installer, a semantic validator, or an agent runtime. It complements tools such as Vercel Skills and skill validators by answering a narrow question: do the selected copies have identical regular-file paths and bytes?

## Quick start

Clone the repository and try the demo:

```sh
git clone https://github.com/splucasaugusto666/skillparity.git
cd skillparity
python skillparity.py demo
python -m unittest discover -s tests -v
```

Or install the CLI from the repository using pipx (isolated environment):

```sh
pipx install git+https://github.com/splucasaugusto666/skillparity.git
skillparity demo
```

The package is not currently published to PyPI. A local clone also supports `python -m pip install .` in a virtual environment.

Compare two directories containing skill subdirectories. Paths are examples; select the actual directories used by your setup.

```sh
python skillparity.py check --baseline source \
  --root source=.agents/skills \
  --root claude=.claude/skills \
  --root codex=.codex/skills
```

For machine-readable output append `--json`; for compact CI output append `--summary` (counts are per target, excluding baseline cells). For symlinks that resolve outside the supplied roots, specify their trusted target directory with `--allow-target PATH`. Only allow directories you trust. Roots themselves are explicitly selected and resolved. No automatic home-directory discovery is performed.

## Repeatable checks with a config file

Save `skillparity.json` in your project (adjust paths to your actual installations):

```json
{"baseline":"source","roots":{"source":".agents/skills","claude":".claude/skills","codex":".codex/skills"}}
```

```sh
skillparity check --config skillparity.json --summary
```

Relative paths are interpreted from the configuration file's directory. Only `baseline` and `roots` are accepted; duplicate keys are rejected. `--config` replaces `--root` and `--baseline`. Use only trusted configuration files; configured roots can reference arbitrary readable directories. External skill-link targets still require explicit `--allow-target` CLI arguments. Do not use untrusted PR configurations on privileged runners.

See [CI integration](docs/CI_INTEGRATION.md) for a pinned workflow example.

## GitHub Action

Add a parity gate to your repository on a Linux runner with Python 3.10+ and a checked-out workspace. Use the [integration guide](docs/CI_INTEGRATION.md) to pin a reviewed commit and configure the composite action. The action emits only aggregate counts, fails on drift or incomplete verification, and rejects configuration paths and catalog roots that resolve outside the workspace. It does not install or execute skills. Remote Action execution has not yet been verified.

## Visual reports

Generate a standalone HTML report (no JavaScript, external assets or network requests):

```sh
skillparity demo --html > report.html
```

Open `report.html` in a browser. The demo returns exit code 1 intentionally. Reports include skill and file names; review them before sharing. For CI logs use `--summary` instead.

## Results

| Status | Meaning |
|---|---|
| MATCH | Same relative regular-file paths and SHA-256 digests as baseline |
| DRIFT | Files added, removed or changed relative to baseline |
| MISSING | Baseline contains a skill absent in this root |
| EXTRA | Skill exists here but not in baseline |
| ABSENT | Extra skill is absent in this other root |
| ERROR | Broken/unapproved link, unsupported entry or read failure |
| UNVERIFIED | Baseline copy could not be read safely |

Exit codes: **0** verified parity; **1** differences; **2** incomplete verification, invalid input or empty catalog. `--json` emits schema version 1. The CLI does not print file contents, hashes or resolved absolute paths. File names and root labels are still reported: review before sharing.

## Scope and limitations

- Immediate non-hidden skill folders are matched by folder name, not YAML metadata. Non-skill regular folders and ordinary files at the catalog root are ignored. Top-level symlinks are checked even if broken.
- Compares all regular files in each skill, including support files; empty directories, permissions, timestamps and runtime behavior are not compared.
- Skill-level links are permitted only within explicitly selected/allowed roots. Internal symlinks and special files are rejected rather than followed.
- Maximum 32 MiB per file, 10,000 files per skill. Not a sandbox for concurrently modified or hostile filesystems; compare a stable trusted checkout. Windows reparse-point behavior has not been verified locally.
- Intentional per-agent variants may legitimately differ. `DRIFT` does not mean a security defect or invalid skill.
- No network requests, telemetry, API keys or third-party runtime dependencies. The demo only writes temporary fixtures.

## CI

Run `python -m unittest discover -s tests -v` for the project's own tests. To enforce parity in your repository, call the `check` command with your actual roots and baseline in your existing CI. The supplied workflow tests this project on Linux, Windows and macOS when enabled by GitHub Actions; remote execution is not yet verified.

## Contributing

Reproducible reports and small tests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

MIT licensed. If this project is useful to you, consider giving it a star.
