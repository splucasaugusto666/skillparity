"""Optional local MCP adapter; the core CLI remains dependency-free."""
import argparse
from pathlib import Path

from skillparity import compare, load_config, summarize


def configured_check(workspace, config):
    """Return a no-argument check using operator-selected trusted catalogs."""
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError('workspace must be a directory')
    config = (workspace / config).resolve(strict=True)
    if not config.is_relative_to(workspace) or not config.is_file():
        raise ValueError('config must be inside workspace')
    roots, baseline = load_config(config)
    roots = {k: p.resolve(strict=True) for k, p in roots.items()}
    if any(not p.is_relative_to(workspace) or not p.is_dir() for p in roots.values()):
        raise ValueError('catalogs must be directories inside workspace')

    def check():
        try:
            if any(p.resolve(strict=True) != p for p in roots.values()):
                raise ValueError('catalog path changed')
            return summarize(compare(roots, baseline))
        except (OSError, ValueError, RuntimeError):
            return {'schema_version': 1, 'exit_code': 2, 'error': 'incomplete verification'}

    return check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    try:
        check = configured_check(args.workspace, args.config)
    except (OSError, ValueError, RuntimeError):
        parser.error('invalid trusted workspace configuration')
    try:
        from mcp.server.fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        if exc.name != "mcp":
            raise
        parser.error("MCP SDK missing; install the optional skillparity[mcp] extra")
    server = FastMCP('SkillParity')

    @server.tool()
    def check_parity() -> dict:
        """Compare configured skill catalogs read-only; return aggregate counts only."""
        return check()

    server.run(transport='stdio')


if __name__ == '__main__':
    main()
