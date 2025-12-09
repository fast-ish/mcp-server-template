# Architecture

## Model Context Protocol (MCP)

MCP is a protocol that enables AI assistants like Claude to interact with external tools and data sources.

```
┌─────────────────┐     JSON-RPC 2.0     ┌─────────────────┐
│                 │◄───────────────────►│                 │
│  Claude / Host  │    (${{ values.transport | upper }} Transport)    │   MCP Server    │
│   (Client)      │                      │  (${{ values.name }})      │
└─────────────────┘                      └─────────────────┘
```

## Server Components

### Tools (Actions)

Tools are functions the LLM can invoke to perform actions:

{%- if values.enableTools %}
```
┌────────────────────────────────────────────────────────────┐
│ Tool: echo                                                  │
├────────────────────────────────────────────────────────────┤
│ Input: { message: string }                                 │
│ Output: { content: [{ type: "text", text: "Echo: ..." }] } │
└────────────────────────────────────────────────────────────┘
```
{%- else %}
(Tools disabled in this configuration)
{%- endif %}

### Resources (Data)

Resources expose data to provide context to the LLM:

{%- if values.enableResources %}
```
┌────────────────────────────────────────────────────────────┐
│ Resource: server://info                                     │
├────────────────────────────────────────────────────────────┤
│ URI: server://info                                         │
│ MIME: application/json                                      │
│ Content: { name, version, capabilities }                   │
└────────────────────────────────────────────────────────────┘
```
{%- else %}
(Resources disabled in this configuration)
{%- endif %}

### Prompts (Templates)

Prompts are reusable templates for common interactions:

{%- if values.enablePrompts %}
```
┌────────────────────────────────────────────────────────────┐
│ Prompt: code_review                                         │
├────────────────────────────────────────────────────────────┤
│ Arguments: code (required), language, focus                │
│ Output: Formatted review request message                   │
└────────────────────────────────────────────────────────────┘
```
{%- else %}
(Prompts disabled in this configuration)
{%- endif %}

## Transport Layer

{%- if values.transport == "stdio" %}

### STDIO Transport

Communication via standard input/output:

```
Host Process ──stdin──► MCP Server
             ◄─stdout──
```

**Advantages:**
- No network ports required
- Secure (no network exposure)
- Simple to deploy locally

**Usage:**
```bash
{%- if values.language == "typescript" %}
node build/index.js
{%- else %}
python -m src.server
{%- endif %}
```

{%- else %}

### HTTP Transport

Communication via HTTP/SSE:

```
Host ──HTTP POST──► MCP Server :8000
     ◄────SSE─────
```

**Advantages:**
- Remote deployment possible
- Multiple clients supported
- Cloud-native

**Usage:**
```bash
{%- if values.language == "typescript" %}
node build/index.js  # Listens on port 8000
{%- else %}
python -m src.server  # Listens on port 8000
{%- endif %}
```

{%- endif %}

## Request/Response Flow

```
1. Client sends request (JSON-RPC 2.0)
   ──────────────────────────────────────►

2. Server validates input (Zod/Pydantic)
   ◄──────────────────────────────────────

3. Server executes handler
   ◄──────────────────────────────────────

4. Server returns result
   ◄──────────────────────────────────────
```

## File Structure

```
${{ values.name }}/
{%- if values.language == "typescript" %}
├── src/
│   ├── index.ts          # Entry point, server setup
│   ├── tools/            # Tool implementations
│   │   └── index.ts
│   ├── resources/        # Resource handlers
│   │   └── index.ts
│   └── prompts/          # Prompt templates
│       └── index.ts
├── tests/
│   └── server.test.ts
├── build/                # Compiled output
├── package.json
└── tsconfig.json
{%- else %}
├── src/
│   ├── __init__.py
│   ├── server.py         # Entry point, server setup
│   ├── tools/            # Tool implementations
│   │   └── __init__.py
│   ├── resources/        # Resource handlers
│   │   └── __init__.py
│   └── prompts/          # Prompt templates
│       └── __init__.py
├── tests/
│   └── test_server.py
└── pyproject.toml
{%- endif %}
```

## References

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP SDK Documentation](https://modelcontextprotocol.io/docs)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
