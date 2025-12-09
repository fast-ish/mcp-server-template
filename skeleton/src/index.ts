{%- if values.language == "typescript" %}
#!/usr/bin/env node
/**
 * ${{ values.name }}
 * {{ '=' * (values.name | length) }}
 *
 * ${{ values.description }}
 *
 * Usage:
 *   npx ${{ values.name }}
 *   node build/index.js
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
{%- if values.transport == "stdio" %}
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
{%- else %}
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
{%- endif %}

{%- if values.enableTools %}
import { registerTools } from "./tools/index.js";
{%- endif %}
{%- if values.enableResources %}
import { registerResources } from "./resources/index.js";
{%- endif %}
{%- if values.enablePrompts %}
import { registerPrompts } from "./prompts/index.js";
{%- endif %}

const SERVER_NAME = "${{ values.name }}";
const SERVER_VERSION = "0.1.0";

async function main(): Promise<void> {
  const server = new McpServer({
    name: SERVER_NAME,
    version: SERVER_VERSION,
  });

{%- if values.enableTools %}

  // Register tools (callable functions)
  registerTools(server);
{%- endif %}

{%- if values.enableResources %}

  // Register resources (data providers)
  registerResources(server);
{%- endif %}

{%- if values.enablePrompts %}

  // Register prompts (reusable templates)
  registerPrompts(server);
{%- endif %}

{%- if values.transport == "stdio" %}

  // Create STDIO transport for local communication
  const transport = new StdioServerTransport();
{%- else %}

  // Create HTTP transport for remote communication
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => crypto.randomUUID(),
  });
{%- endif %}

  // Connect server to transport
  await server.connect(transport);

  console.error(`${SERVER_NAME} v${SERVER_VERSION} running on ${{ values.transport | upper }}`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
{%- endif %}
