{%- if values.language == "python" and values.enableResources %}
"""
Resources Registration
======================

Resources expose data to the LLM for context.
They can be static (config files) or dynamic (live data).
"""

import json
import os
{%- if values.enableFileSystem %}
from pathlib import Path
{%- endif %}
from typing import Any

from mcp.server import Server
from mcp.types import Resource, TextResourceContents


def register_resources(server: Server) -> None:
    """Register all resources with the MCP server."""

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources."""
        resources = [
            Resource(
                uri="server://info",
                name="Server Info",
                description="Server information and capabilities",
                mimeType="application/json",
            ),
        ]
{%- if values.enableFileSystem %}
        # Add file resources from allowed directory
        allowed_dir = Path(os.environ.get("MCP_ALLOWED_DIR", "."))
        if allowed_dir.exists():
            for file_path in allowed_dir.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith("."):
                    resources.append(
                        Resource(
                            uri=f"file://{file_path.relative_to(allowed_dir)}",
                            name=file_path.name,
                            description=f"File: {file_path.relative_to(allowed_dir)}",
                            mimeType=get_mime_type(file_path),
                        )
                    )
{%- endif %}
        return resources

    @server.read_resource()
    async def read_resource(uri: str) -> list[TextResourceContents]:
        """Read a resource by URI."""
        if uri == "server://info":
            info = {
                "name": "${{ values.name }}",
                "version": "0.1.0",
                "description": "${{ values.description }}",
                "capabilities": {
                    "tools": ${{ values.enableTools | lower }},
                    "resources": True,
                    "prompts": ${{ values.enablePrompts | lower }},
                },
            }
            return [
                TextResourceContents(
                    uri=uri,
                    mimeType="application/json",
                    text=json.dumps(info, indent=2),
                )
            ]

{%- if values.enableFileSystem %}
        if uri.startswith("file://"):
            file_path = uri[7:]  # Remove "file://" prefix
            allowed_dir = Path(os.environ.get("MCP_ALLOWED_DIR", ".")).resolve()
            resolved_path = (allowed_dir / file_path).resolve()

            # Security: Validate path is within allowed directory
            if not str(resolved_path).startswith(str(allowed_dir)):
                raise ValueError("Access denied: path outside allowed directory")

            if not resolved_path.exists():
                raise ValueError(f"File not found: {file_path}")

            content = resolved_path.read_text()
            return [
                TextResourceContents(
                    uri=uri,
                    mimeType=get_mime_type(resolved_path),
                    text=content,
                )
            ]
{%- endif %}

        raise ValueError(f"Unknown resource: {uri}")


{%- if values.enableFileSystem %}
def get_mime_type(file_path: Path) -> str:
    """Get MIME type from file extension."""
    mime_types = {
        ".json": "application/json",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".xml": "application/xml",
        ".html": "text/html",
        ".css": "text/css",
        ".js": "text/javascript",
        ".ts": "text/typescript",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".py": "text/x-python",
        ".go": "text/x-go",
        ".rs": "text/x-rust",
    }
    return mime_types.get(file_path.suffix.lower(), "text/plain")
{%- endif %}
{%- endif %}
