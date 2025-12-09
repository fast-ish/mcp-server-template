{%- if values.language == "python" and values.enableTools %}
"""
Tools Registration
==================

Tools are callable functions that the LLM can invoke.
They represent actions the server can perform.
"""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

{%- if values.enableHttp %}
import httpx
{%- endif %}


class EchoInput(BaseModel):
    """Input for echo tool."""

    message: str = Field(description="Message to echo back")


class GetTimeInput(BaseModel):
    """Input for get_time tool."""

    timezone: str = Field(default="UTC", description="Timezone (e.g., 'UTC', 'America/New_York')")


{%- if values.enableHttp %}
class FetchUrlInput(BaseModel):
    """Input for fetch_url tool."""

    url: str = Field(description="URL to fetch")
{%- endif %}


def register_tools(server: Server) -> None:
    """Register all tools with the MCP server."""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        tools = [
            Tool(
                name="echo",
                description="Echo back a message (example tool)",
                inputSchema=EchoInput.model_json_schema(),
            ),
            Tool(
                name="get_time",
                description="Get the current date and time",
                inputSchema=GetTimeInput.model_json_schema(),
            ),
{%- if values.enableHttp %}
            Tool(
                name="fetch_url",
                description="Fetch content from a URL",
                inputSchema=FetchUrlInput.model_json_schema(),
            ),
{%- endif %}
        ]
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle tool calls."""
        if name == "echo":
            args = EchoInput(**arguments)
            return [TextContent(type="text", text=f"Echo: {args.message}")]

        elif name == "get_time":
            args = GetTimeInput(**arguments)
            try:
                tz = ZoneInfo(args.timezone)
            except Exception:
                tz = ZoneInfo("UTC")
            now = datetime.now(tz)
            formatted = now.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
            return [TextContent(type="text", text=formatted)]

{%- if values.enableHttp %}
        elif name == "fetch_url":
            args = FetchUrlInput(**arguments)
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(args.url, timeout=30.0)
                    text = response.text[:10000]  # Limit response size
                return [TextContent(type="text", text=text)]
            except Exception as e:
                return [TextContent(type="text", text=f"Error fetching URL: {e}")]
{%- endif %}

        else:
            raise ValueError(f"Unknown tool: {name}")
{%- endif %}
