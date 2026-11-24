# Changelog

## 0.4.0 — release candidate

- Added a reusable composite GitHub Action for Linux/POSIX runners.
- Added a workspace-confined CI entry point, aggregate-only output and nine local integration tests.
- Added synthetic fixtures and a remote Action smoke-test job. Remote execution is not yet verified.

## 0.3.0 — release candidate

- Added reusable JSON configuration with relative paths, strict keys and size limit.
- Added label validation to the Python API and eight regression tests.
- Added CI integration guidance with explicit commit pinning and trust boundaries.
- Local Linux tests: 27 passed; wheel built. Remote CI still unverified.

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
