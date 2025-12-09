{%- if values.language == "python" and values.enablePrompts %}
"""
Prompts Registration
====================

Prompts are reusable templates for common interactions.
They can include dynamic arguments and resource context.
"""

from typing import Any, Literal

from mcp.server import Server
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent
from pydantic import BaseModel, Field


class CodeReviewArgs(BaseModel):
    """Arguments for code review prompt."""

    code: str = Field(description="The code to review")
    language: str | None = Field(default=None, description="Programming language")
    focus: Literal["security", "performance", "readability", "all"] | None = Field(
        default=None, description="What to focus on"
    )


class ExplainArgs(BaseModel):
    """Arguments for explain prompt."""

    topic: str = Field(description="The topic to explain")
    audience: Literal["beginner", "intermediate", "expert"] | None = Field(
        default=None, description="Target audience level"
    )


def register_prompts(server: Server) -> None:
    """Register all prompts with the MCP server."""

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        """List available prompts."""
        return [
            Prompt(
                name="code_review",
                description="Review code for quality and suggest improvements",
                arguments=[
                    PromptArgument(
                        name="code",
                        description="The code to review",
                        required=True,
                    ),
                    PromptArgument(
                        name="language",
                        description="Programming language",
                        required=False,
                    ),
                    PromptArgument(
                        name="focus",
                        description="What to focus on (security, performance, readability, all)",
                        required=False,
                    ),
                ],
            ),
            Prompt(
                name="explain",
                description="Explain a concept in simple terms",
                arguments=[
                    PromptArgument(
                        name="topic",
                        description="The topic to explain",
                        required=True,
                    ),
                    PromptArgument(
                        name="audience",
                        description="Target audience level (beginner, intermediate, expert)",
                        required=False,
                    ),
                ],
            ),
        ]

    @server.get_prompt()
    async def get_prompt(
        name: str, arguments: dict[str, Any] | None
    ) -> list[PromptMessage]:
        """Get a prompt by name."""
        args = arguments or {}

        if name == "code_review":
            parsed = CodeReviewArgs(**args)
            focus_area = parsed.focus or "all"
            lang = parsed.language or "unknown"

            return [
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""Please review the following {lang} code with a focus on {focus_area}:

```{lang}
{parsed.code}
```

Provide:
1. A summary of what the code does
2. Potential issues or improvements
3. Specific suggestions with code examples""",
                    ),
                )
            ]

        elif name == "explain":
            parsed = ExplainArgs(**args)
            level = parsed.audience or "beginner"

            return [
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""Please explain "{parsed.topic}" for a {level} audience.

Include:
- A clear definition
- Key concepts
- Practical examples
- Common misconceptions (if any)""",
                    ),
                )
            ]

        raise ValueError(f"Unknown prompt: {name}")
{%- endif %}
