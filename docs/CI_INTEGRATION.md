# CI integration

Commit a `skillparity.json` containing your baseline label and catalog paths. A failing check returns 1 for drift and 2 for incomplete verification. Both should fail a parity gate.

Example GitHub Actions steps, assuming Python and Git are installed:

```yaml
- name: Install reviewed SkillParity revision
  run: python -m pip install 'git+https://github.com/splucasaugusto666/skillparity.git@REVIEWED_COMMIT_SHA'
- name: Check skills
  run: skillparity check --config skillparity.json --summary
```

Replace `REVIEWED_COMMIT_SHA` with an actual reviewed commit supporting `--config` (v0.3.0 or later). Use ordinary pull_request workflows with minimal permissions, no secrets, and isolated runners. Never use pull_request_target to evaluate a contributor-controlled config. This tool is not a sandbox; it reads selected roots. JSON output can include file names and root labels. Review before sharing.
