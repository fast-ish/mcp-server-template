# MCP Server Template

Backstage template for creating Model Context Protocol servers.

## Structure

```
/template.yaml          # Backstage scaffolder definition
/skeleton/              # Generated server code
/docs/                  # Template documentation
```

## Key Files

- `template.yaml` - Template parameters and steps (scaffolder.backstage.io/v1beta3)
- `skeleton/` - Generated files:
  - `src/index.ts` or `src/server.py` - Entry point, server setup
  - `src/tools/` - Tool implementations (callable functions)
  - `src/resources/` - Resource handlers (data providers)
  - `src/prompts/` - Prompt templates (reusable interactions)
  - `tests/` - Server tests

## Template Syntax

Uses Jinja2 via Backstage:
- Variables: `${{ values.name }}`, `${{ values.language }}`
- Conditionals: `{%- if values.enableTools %}...{%- endif %}`
- Language switching: `{%- if values.language == "typescript" %}...{%- endif %}`

## MCP Architecture

### Three Core Capabilities

1. **Tools** - Functions the LLM can call (actions/verbs)
2. **Resources** - Data the LLM can read (context/nouns)
3. **Prompts** - Reusable message templates (workflows)

### Transport Options

- **STDIO** - Local communication via stdin/stdout (default)
- **HTTP** - Remote communication via HTTP/SSE

## Template Parameters

### Component Info

| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Server name (lowercase, alphanumeric with hyphens) |
| owner | string | Owning team from Backstage catalog |
| description | string | What capabilities does this server provide? |

### Runtime

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | enum | typescript | Implementation language (typescript/python) |
| nodeVersion | enum | 20 | Node.js version (22, 20, 18) |
| pythonVersion | enum | 3.12 | Python version (3.13, 3.12, 3.11) |
| packageManager | enum | pnpm | Package manager (npm/pnpm/yarn/uv/poetry) |

### MCP Capabilities

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enableTools | boolean | true | Expose callable functions |
| enableResources | boolean | true | Expose data/context |
| enablePrompts | boolean | false | Expose prompt templates |

### Transport & Deployment

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| transport | enum | stdio | Transport: stdio, http |
| deployment | enum | local | Target: local, docker, lambda |

### Integrations

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enableDatabase | boolean | false | PostgreSQL/SQLite access |
| enableHttp | boolean | false | External HTTP requests |
| enableFileSystem | boolean | false | Local file access |
| enableGitHub | boolean | false | GitHub API access |

### Security

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enableAuth | boolean | false | OAuth 2.1 authentication |
| inputValidation | enum | zod | Schema validation library |

## Where Parameters Are Used

| Parameter | Files |
|-----------|-------|
| `name` | package.json, pyproject.toml, catalog-info.yaml, README.md |
| `language` | All files (conditionally includes TS or Python code) |
| `nodeVersion` | package.json, .github/workflows/ci.yaml |
| `pythonVersion` | pyproject.toml, .github/workflows/ci.yaml |
| `packageManager` | Makefile-equivalent commands in README, CI |
| `enableTools` | src/index.ts, src/server.py (tool registration) |
| `enableResources` | src/index.ts, src/server.py (resource registration) |
| `enablePrompts` | src/index.ts, src/server.py (prompt registration) |
| `transport` | src/index.ts, src/server.py (transport setup) |
| `enableDatabase` | package.json, pyproject.toml (dependencies) |
| `enableHttp` | src/tools/ (fetch_url tool) |
| `enableFileSystem` | src/resources/ (file resource) |
| `enableGitHub` | package.json, pyproject.toml (dependencies) |
| `enableAuth` | .env.example (OAuth config) |

## Conventions

- Entry point: `node build/index.js` or `python -m src.server`
- Testing: `npx @modelcontextprotocol/inspector` for interactive testing
- Config: `~/.config/Claude/claude_desktop_config.json` for Claude Desktop

## Don't

- Expose sensitive data in resources without authentication
- Allow arbitrary file system access outside allowed directories
- Skip input validation on tools
- Use string concatenation for database queries
