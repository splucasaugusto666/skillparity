# Changelog

## 0.2.0 — release candidate

- Added installable Python package and CLI entry point.
- Added compact `--summary` output for CI; preserves exit semantics.
- Added four regression tests and CI installation smoke checks.
- Local Linux/Python 3.13.5: 19 tests passed; local wheel built and installed. Remote CI pending.

## 0.1.0 — local release candidate, 2026-11-23

- Read-only SHA-256 comparison of skill folders with a named baseline.
- Added, removed, changed, missing and extra skill/file reporting.
- Controlled skill-root symlink resolution; internal symlinks rejected.
- JSON output, exit codes and synthetic demo.
- Local unit tests and proposed cross-platform CI workflow.
