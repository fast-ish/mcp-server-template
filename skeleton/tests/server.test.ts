{%- if values.language == "typescript" %}
/**
 * Server Tests
 * ============
 *
 * Tests for MCP server functionality.
 */

import { describe, it, expect } from "vitest";

describe("${{ values.name }}", () => {
  describe("server initialization", () => {
    it("should create server with correct name", () => {
      // TODO: Add server initialization test
      expect(true).toBe(true);
    });
  });

{%- if values.enableTools %}

  describe("tools", () => {
    it("should register echo tool", () => {
      // TODO: Add tool registration test
      expect(true).toBe(true);
    });

    it("should handle echo tool call", async () => {
      // TODO: Add tool execution test
      expect(true).toBe(true);
    });
  });
{%- endif %}

{%- if values.enableResources %}

  describe("resources", () => {
    it("should list available resources", async () => {
      // TODO: Add resource listing test
      expect(true).toBe(true);
    });

    it("should read server info resource", async () => {
      // TODO: Add resource reading test
      expect(true).toBe(true);
    });
  });
{%- endif %}

{%- if values.enablePrompts %}

  describe("prompts", () => {
    it("should list available prompts", async () => {
      // TODO: Add prompt listing test
      expect(true).toBe(true);
    });

    it("should generate code review prompt", async () => {
      // TODO: Add prompt generation test
      expect(true).toBe(true);
    });
  });
{%- endif %}
});
{%- endif %}
