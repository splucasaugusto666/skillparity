# CI integration

Commit a `skillparity.json` containing your baseline label and catalog paths. A failing check returns 1 for drift and 2 for incomplete verification. Both should fail a parity gate.

Example GitHub Actions steps, assuming Python and Git are installed:

```yaml
- name: Install reviewed SkillParity revision
  run: python -m pip install 'git+https://github.com/splucasaugusto666/skillparity.git@3bd3dc0bb6f2c87326108ac2e6940ee6795ef78d'
- name: Check skills
  run: skillparity check --config skillparity.json --summary
```

This example pins the published v1.0.0 release commit; review it before use. Use ordinary pull_request workflows with minimal permissions, no secrets, and isolated runners. Never use pull_request_target to evaluate a contributor-controlled config. This tool is not a sandbox; it reads selected roots. JSON output can include file names and root labels. Review before sharing.

## Composite GitHub Action (v0.4.0+)

The example pins the official v1.0.0 release commit. Review the code before running; keep the SHA pinned rather than using a mutable branch. On a Linux hosted runner with Python 3.10+ already on PATH, after checkout:

```yaml
- uses: splucasaugusto666/skillparity@3bd3dc0bb6f2c87326108ac2e6940ee6795ef78d
  with:
    config: skillparity.json
```

The action checks the configured baseline and roots and exits 0 (match), 1 (drift) or 2 (incomplete). It emits aggregate counts without names or paths. The config file and all roots must resolve inside the checkout; external skill symlinks are rejected. Explicit external target overrides are not supported by the action. Use trusted, stable checkouts on isolated POSIX runners; this is not a filesystem sandbox or a defense against concurrent mutation. Do not run privileged workflows on untrusted pull requests. Use minimal permissions and disable persisted checkout credentials when possible.

A checked-in synthetic fixture under `examples/parity` is included for a local smoke test:

```sh
GITHUB_WORKSPACE="$PWD" SKILLPARITY_CONFIG=examples/parity/skillparity.json python ci_check.py
```
