"""Workspace-confined entry point for the composite GitHub Action."""
import os
from pathlib import Path
import sys

from skillparity import compare, exit_code, load_config, render_summary


def check(workspace, config):
    if os.name != 'posix':
        raise ValueError('the composite action requires a POSIX runner')
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError('workspace must be a directory')
    config = (workspace / config).resolve(strict=True)
    if not config.is_relative_to(workspace) or not config.is_file():
        raise ValueError('config must be a regular file inside the workspace')
    roots, baseline = load_config(config)
    roots = {label: path.resolve(strict=True) for label, path in roots.items()}
    if any(not path.is_relative_to(workspace) for path in roots.values()):
        raise ValueError('all roots must resolve inside the workspace')
    report = compare(roots, baseline)
    render_summary(report)
    return exit_code(report)


def main():
    try:
        return check(os.environ['GITHUB_WORKSPACE'], os.environ['SKILLPARITY_CONFIG'])
    except (KeyError, OSError, RuntimeError, ValueError):
        # Do not expose paths or config contents in public CI logs.
        print('SkillParity: invalid or unreadable workspace configuration', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
