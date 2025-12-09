{%- if values.language == "typescript" and values.enablePrompts %}
/**
 * Prompts Registration
 * ====================
 *
 * Prompts are reusable templates for common interactions.
 * They can include dynamic arguments and resource context.
 */

import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

/**
 * Register all prompts with the MCP server.
 */
export function registerPrompts(server: McpServer): void {
  // Example: Code review prompt
  server.prompt(
    "code_review",
    "Review code for quality and suggest improvements",
    {
      code: z.string().describe("The code to review"),
      language: z.string().optional().describe("Programming language"),
      focus: z
        .enum(["security", "performance", "readability", "all"])
        .optional()
        .describe("What to focus on"),
    },
    async ({ code, language, focus }) => {
      const focusArea = focus || "all";
      const lang = language || "unknown";

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Please review the following ${lang} code with a focus on ${focusArea}:

\`\`\`${lang}
${code}
\`\`\`

Provide:
1. A summary of what the code does
2. Potential issues or improvements
3. Specific suggestions with code examples`,
            },
          },
        ],
      };
    }
  );

  // Example: Explain concept prompt
  server.prompt(
    "explain",
    "Explain a concept in simple terms",
    {
      topic: z.string().describe("The topic to explain"),
      audience: z
        .enum(["beginner", "intermediate", "expert"])
        .optional()
        .describe("Target audience level"),
    },
    async ({ topic, audience }) => {
      const level = audience || "beginner";

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Please explain "${topic}" for a ${level} audience.

Include:
- A clear definition
- Key concepts
- Practical examples
- Common misconceptions (if any)`,
            },
          },
        ],
      };
    }
  );

  // Add your custom prompts here
  // server.prompt("my_prompt", "Description", { arg: z.string() }, async ({ arg }) => { ... });
}
{%- endif %}
