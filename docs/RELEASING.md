# Release v1.0.0

The release workflow is restricted to main. It calls the existing Linux, macOS and Windows CI matrix and the composite-action smoke test, builds a wheel only on success, checks the installed CLI, and publishes the wheel plus SHA256SUMS only after those checks pass. Only the publish job has contents: write. The release targets the tested commit and refuses to reuse an existing orphan tag. An existing release is left unchanged.

The workflow triggers on a push modifying release.yml on main, or a maintainer can run it manually from Actions > Release v1.0.0 > Run workflow (main). If the run is not visible, check Actions settings and workflow permissions. Do not report the release as published without checking the Releases page.

## Local verification
```sh
python -m unittest discover -s tests -v
python -m pip wheel --no-deps -w dist .
python -m venv .venv
.venv/bin/python -m pip install --no-deps dist/skillparity-1.0.0-py3-none-any.whl
.venv/bin/skillparity --version
```

The local wheel was built and installed on Linux/Python 3.13.5. The 42 tests passed. Remote CI and the formal release were not confirmed at the time this document was prepared.
