"""Optional end-to-end protocol test, invoked separately with MCP SDK v1."""
import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def smoke():
    repo = Path(__file__).resolve().parents[1]
    params = StdioServerParameters(command=sys.executable, args=[
        str(repo / 'skillparity_mcp.py'), '--workspace', str(repo),
        '--config', 'examples/parity/skillparity.json'])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert [tool.name for tool in tools.tools] == ['check_parity']
            assert not tools.tools[0].inputSchema.get('properties')
            result = await session.call_tool('check_parity', {})
            assert not result.isError
            data = json.loads(result.content[0].text)
            assert data == {'schema_version': 1, 'skills': 1, 'targets': 1,
                            'counts': {'MATCH': 1}, 'exit_code': 0}


if __name__ == '__main__':
    asyncio.run(asyncio.wait_for(smoke(), timeout=30))
