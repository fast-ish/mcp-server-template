{%- if values.language == "typescript" and values.enableTools %}
/**
 * Tools Registration
 * ==================
 *
 * Tools are callable functions that the LLM can invoke.
 * They represent actions the server can perform.
 */

import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

/**
 * Register all tools with the MCP server.
 */
export function registerTools(server: McpServer): void {
  // Example: Echo tool
  server.tool(
    "echo",
    "Echo back a message (example tool)",
    {
      message: z.string().describe("Message to echo back"),
    },
    async ({ message }) => {
      return {
        content: [
          {
            type: "text",
            text: `Echo: ${message}`,
          },
        ],
      };
    }
  );

  // Example: Get current time
  server.tool(
    "get_time",
    "Get the current date and time",
    {
      timezone: z.string().optional().describe("Timezone (e.g., 'UTC', 'America/New_York')"),
    },
    async ({ timezone }) => {
      const now = new Date();
      const options: Intl.DateTimeFormatOptions = {
        dateStyle: "full",
        timeStyle: "long",
        timeZone: timezone || "UTC",
      };
      const formatted = now.toLocaleString("en-US", options);

      return {
        content: [
          {
            type: "text",
            text: formatted,
          },
        ],
      };
    }
  );

{%- if values.enableHttp %}

  // Example: Fetch URL
  server.tool(
    "fetch_url",
    "Fetch content from a URL",
    {
      url: z.string().url().describe("URL to fetch"),
    },
    async ({ url }) => {
      try {
        const response = await fetch(url);
        const text = await response.text();

        return {
          content: [
            {
              type: "text",
              text: text.slice(0, 10000), // Limit response size
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error fetching URL: ${error}`,
            },
          ],
          isError: true,
        };
      }
    }
  );
{%- endif %}

  // Add your custom tools here
  // server.tool("my_tool", "Description", { param: z.string() }, async ({ param }) => { ... });
}
{%- endif %}
