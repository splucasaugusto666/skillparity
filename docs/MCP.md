# Experimental local MCP adapter (development checkout)

This optional stdio adapter uses the official [Python SDK v1](https://py.sdk.modelcontextprotocol.io/v1/). It does not change the core CLI or the published v1.0.0 wheel.

In a dedicated virtual environment, review the checkout and install the optional SDK:

```sh
python -m pip install 'mcp>=1.12,<2'
python skillparity_mcp.py --workspace . --config examples/parity/skillparity.json
```

Configure your MCP-capable host to launch the selected virtual environment's Python executable with absolute script and workspace paths. The host's stdio process has no HTTP listener. The tool `check_parity` has no path arguments; operator-selected roots are fixed at startup, config and catalogs must resolve within the workspace, and results contain aggregate counts only. Never expose an untrusted, changing filesystem or privileged workspace. This is not an OS sandbox; use trusted, stable directories and least-privilege processes. The SDK is optional and may have its own dependencies and security updates.

Run the dedicated protocol test with `python tests/mcp_protocol_smoke.py` after installing the SDK. Six adapter unit tests passed locally without the SDK. The end-to-end protocol test has not yet run locally because no SDK distribution was available in that environment. Client-specific compatibility remains unverified.
