{%- if values.language == "typescript" and values.enableResources %}
/**
 * Resources Registration
 * ======================
 *
 * Resources expose data to the LLM for context.
 * They can be static (config files) or dynamic (live data).
 */

import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
{%- if values.enableFileSystem %}
import * as fs from "fs/promises";
import * as path from "path";
{%- endif %}

/**
 * Register all resources with the MCP server.
 */
export function registerResources(server: McpServer): void {
  // Example: Server info resource
  server.resource(
    "server://info",
    "Server information and capabilities",
    async () => {
      const info = {
        name: "${{ values.name }}",
        version: "0.1.0",
        description: "${{ values.description }}",
        capabilities: {
          tools: ${{ values.enableTools | lower }},
          resources: true,
          prompts: ${{ values.enablePrompts | lower }},
        },
      };

      return {
        contents: [
          {
            uri: "server://info",
            mimeType: "application/json",
            text: JSON.stringify(info, null, 2),
          },
        ],
      };
    }
  );

{%- if values.enableFileSystem %}

  // Example: File resource (with file system access)
  server.resource(
    "file://{path}",
    "Read a file from the allowed directory",
    async (uri) => {
      // Extract path from URI
      const filePath = uri.pathname;

      // Security: Validate path is within allowed directory
      const allowedDir = process.env.MCP_ALLOWED_DIR || process.cwd();
      const resolvedPath = path.resolve(allowedDir, filePath);

      if (!resolvedPath.startsWith(allowedDir)) {
        throw new Error("Access denied: path outside allowed directory");
      }

      try {
        const content = await fs.readFile(resolvedPath, "utf-8");
        const mimeType = getMimeType(resolvedPath);

        return {
          contents: [
            {
              uri: uri.href,
              mimeType,
              text: content,
            },
          ],
        };
      } catch (error) {
        throw new Error(`Failed to read file: ${error}`);
      }
    }
  );
{%- endif %}

  // Add your custom resources here
  // server.resource("custom://resource", "Description", async () => { ... });
}

{%- if values.enableFileSystem %}

/**
 * Get MIME type from file extension.
 */
function getMimeType(filePath: string): string {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes: Record<string, string> = {
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
  };
  return mimeTypes[ext] || "text/plain";
}
{%- endif %}
{%- endif %}
