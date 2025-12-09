# MCP Server Template

> Golden path template for building Model Context Protocol servers with TypeScript or Python.

[![Backstage](https://img.shields.io/badge/Backstage-Template-blue)](https://backstage.io)
[![MCP](https://img.shields.io/badge/MCP-Protocol-purple)](https://modelcontextprotocol.io)

## What's Included

| Category | Components |
|----------|------------|
| **Core** | Server setup, transport configuration, capability registration |
| **Tools** | Callable functions for LLM actions |
| **Resources** | Data providers for LLM context |
| **Prompts** | Reusable interaction templates |
| **Testing** | Unit tests, MCP Inspector integration |

## Quick Start

1. Go to [Backstage Software Catalog](https://backstage.yourcompany.com/create)
2. Select "MCP Server"
3. Configure your server capabilities
4. Submit and start building

## Template Options

### Component Info

| Parameter | Description |
|-----------|-------------|
| `name` | Unique server name (lowercase, alphanumeric with hyphens) |
| `owner` | Owning team from Backstage catalog |
| `description` | What capabilities does this server provide? |

### Runtime

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `language` | typescript, python | typescript | Implementation language |
| `nodeVersion` | 22, 20, 18 | 20 | Node.js version (for TypeScript) |
| `pythonVersion` | 3.13, 3.12, 3.11 | 3.12 | Python version (for Python) |
| `packageManager` | npm, pnpm, yarn, uv, poetry | pnpm | Package manager |

### MCP Capabilities

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enableTools` | true | Expose callable functions to the LLM |
| `enableResources` | true | Expose data/context to the LLM |
| `enablePrompts` | false | Expose reusable prompt templates |

### Transport & Deployment

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `transport` | stdio, http | stdio | Communication transport |
| `deployment` | local, docker, lambda | local | Deployment target |

### Integrations

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enableDatabase` | false | PostgreSQL/SQLite database access |
| `enableHttp` | false | Make external HTTP requests |
| `enableFileSystem` | false | Read/write local files |
| `enableGitHub` | false | GitHub API access |

### Security

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `enableAuth` | true/false | false | OAuth 2.1 authentication (for HTTP) |
| `inputValidation` | zod, pydantic, jsonschema | zod | Schema validation library |

## What Gets Created

```
{name}/
├── src/
│   ├── index.ts / server.py    # Entry point
│   ├── tools/                   # Tool implementations
│   ├── resources/               # Resource handlers
│   └── prompts/                 # Prompt templates
├── tests/
│   └── server.test.ts / test_server.py
├── docs/
│   ├── GETTING_STARTED.md
│   ├── architecture.md
│   ├── SECURITY.md
│   └── TROUBLESHOOTING.md
├── .github/
│   ├── workflows/ci.yaml
│   └── dependabot.yml
├── catalog-info.yaml
├── package.json / pyproject.toml
└── README.md
```

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](./docs/GETTING_STARTED.md) | First steps |
| [Architecture](./docs/ARCHITECTURE.md) | MCP protocol overview |
| [Security](./docs/SECURITY.md) | Security best practices |

## Based On

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## Support

- **Slack**: #platform-help
- **Office Hours**: Thursdays 2-3pm
