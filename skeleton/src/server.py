{%- if values.language == "python" %}
#!/usr/bin/env python3
"""
${{ values.name }}
{{ '=' * (values.name | length) }}

${{ values.description }}

Usage:
    python -m src.server
    uvx ${{ values.name }}
"""

from mcp.server import Server
{%- if values.transport == "stdio" %}
from mcp.server.stdio import stdio_server
{%- else %}
from mcp.server.http import http_server
{%- endif %}

{%- if values.enableTools %}
from .tools import register_tools
{%- endif %}
{%- if values.enableResources %}
from .resources import register_resources
{%- endif %}
{%- if values.enablePrompts %}
from .prompts import register_prompts
{%- endif %}

SERVER_NAME = "${{ values.name }}"
SERVER_VERSION = "0.1.0"


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server(SERVER_NAME)

{%- if values.enableTools %}

    # Register tools (callable functions)
    register_tools(server)
{%- endif %}

{%- if values.enableResources %}

    # Register resources (data providers)
    register_resources(server)
{%- endif %}

{%- if values.enablePrompts %}

    # Register prompts (reusable templates)
    register_prompts(server)
{%- endif %}

    return server


async def main() -> None:
    """Main entry point."""
    server = create_server()

{%- if values.transport == "stdio" %}
    # Run with STDIO transport for local communication
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
{%- else %}
    # Run with HTTP transport for remote communication
    await http_server(server, host="0.0.0.0", port=8000)
{%- endif %}


def main_sync() -> None:
    """Synchronous entry point."""
    import asyncio

    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
{%- endif %}
