# Experimental local MCP adapter (v1.1.0 candidate)

This optional stdio adapter uses the official [Python SDK v1](https://py.sdk.modelcontextprotocol.io/v1/). The optional dependency is available via `pip install '.[mcp]'` from a reviewed v1.1.0 checkout. The ordinary package installation remains dependency-free.

In a dedicated virtual environment, review the checkout and install the optional SDK:

```sh
python -m pip install '.[mcp]'
skillparity-mcp --workspace . --config examples/parity/skillparity.json
```

Configure your MCP-capable host to launch the selected virtual environment's `skillparity-mcp` executable with an absolute workspace path and config path. The host's stdio process has no HTTP listener. The tool `check_parity` has no path arguments; operator-selected roots are fixed at startup, config and catalogs must resolve within the workspace, and results contain aggregate counts only. Never expose an untrusted, changing filesystem or privileged workspace. This is not an OS sandbox; use trusted, stable directories and least-privilege processes. The SDK is optional and may have its own dependencies and security updates.

Run the dedicated protocol test with `python tests/mcp_protocol_smoke.py` after installing the SDK. Six adapter unit tests passed locally without the SDK. The [end-to-end protocol test passed remotely](https://github.com/splucasaugusto666/skillparity/actions/runs/45309886663). The SDK is not installed in the local test environment. Client-specific compatibility remains unverified.
