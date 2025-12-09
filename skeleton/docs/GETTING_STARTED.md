# Getting Started

## Prerequisites

{%- if values.language == "typescript" %}
- Node.js ${{ values.nodeVersion }}+
{%- if values.packageManager == "pnpm" %}
- pnpm (`npm install -g pnpm`)
{%- elif values.packageManager == "yarn" %}
- yarn (`npm install -g yarn`)
{%- else %}
- npm (comes with Node.js)
{%- endif %}
{%- else %}
- Python ${{ values.pythonVersion }}+
- [uv](https://github.com/astral-sh/uv) package manager
{%- endif %}

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/fast-ish/${{ values.name }}.git
cd ${{ values.name }}

{%- if values.language == "typescript" %}
# Install dependencies
{%- if values.packageManager == "pnpm" %}
pnpm install
{%- elif values.packageManager == "yarn" %}
yarn install
{%- else %}
npm install
{%- endif %}

# Build the server
{%- if values.packageManager == "pnpm" %}
pnpm build
{%- elif values.packageManager == "yarn" %}
yarn build
{%- else %}
npm run build
{%- endif %}
{%- else %}
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
{%- endif %}
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Test the Server

Use the MCP Inspector to test your server:

```bash
{%- if values.language == "typescript" %}
{%- if values.packageManager == "pnpm" %}
pnpm inspect
{%- elif values.packageManager == "yarn" %}
yarn inspect
{%- else %}
npm run inspect
{%- endif %}
{%- else %}
npx @modelcontextprotocol/inspector python -m src.server
{%- endif %}
```

This opens a web UI where you can:
- List and call tools
- Browse and read resources
- Test prompts

### 4. Connect to Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "${{ values.name }}": {
{%- if values.language == "typescript" %}
      "command": "node",
      "args": ["$(pwd)/build/index.js"]
{%- else %}
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "$(pwd)"
{%- endif %}
    }
  }
}
```

Restart Claude Desktop to load the new server.

## Adding Custom Functionality

{%- if values.enableTools %}

### Adding a Tool

{%- if values.language == "typescript" %}
Edit `src/tools/index.ts`:

```typescript
server.tool(
  "my_tool",
  "Description of what the tool does",
  {
    param1: z.string().describe("First parameter"),
    param2: z.number().optional().describe("Optional number"),
  },
  async ({ param1, param2 }) => {
    // Your implementation here
    return {
      content: [{ type: "text", text: "Result" }],
    };
  }
);
```
{%- else %}
Edit `src/tools/__init__.py`:

```python
# Add to list_tools()
Tool(
    name="my_tool",
    description="Description of what the tool does",
    inputSchema=MyToolInput.model_json_schema(),
)

# Add to call_tool()
elif name == "my_tool":
    args = MyToolInput(**arguments)
    # Your implementation here
    return [TextContent(type="text", text="Result")]
```
{%- endif %}
{%- endif %}

{%- if values.enableResources %}

### Adding a Resource

{%- if values.language == "typescript" %}
Edit `src/resources/index.ts`:

```typescript
server.resource(
  "custom://my-resource",
  "Description of the resource",
  async () => {
    const data = await fetchData();
    return {
      contents: [{
        uri: "custom://my-resource",
        mimeType: "application/json",
        text: JSON.stringify(data),
      }],
    };
  }
);
```
{%- else %}
Edit `src/resources/__init__.py`:

```python
# Add to list_resources()
Resource(
    uri="custom://my-resource",
    name="My Resource",
    description="Description of the resource",
    mimeType="application/json",
)

# Add to read_resource()
if uri == "custom://my-resource":
    data = await fetch_data()
    return [TextResourceContents(
        uri=uri,
        mimeType="application/json",
        text=json.dumps(data),
    )]
```
{%- endif %}
{%- endif %}

## Next Steps

- Read [Architecture](./architecture.md) to understand the MCP protocol
- Review [Security](./SECURITY.md) for best practices
- Check [Troubleshooting](./TROUBLESHOOTING.md) if you run into issues
