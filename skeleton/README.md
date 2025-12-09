# ${{ values.name }}

> ${{ values.description }}

## Quick Start

### Prerequisites

{%- if values.language == "typescript" %}
- Node.js ${{ values.nodeVersion }}+
{%- if values.packageManager == "pnpm" %}
- pnpm
{%- elif values.packageManager == "yarn" %}
- yarn
{%- else %}
- npm
{%- endif %}
{%- else %}
- Python ${{ values.pythonVersion }}+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
{%- endif %}

### Setup

```bash
# Clone the repository
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

# Build
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

### Running the Server

{%- if values.transport == "stdio" %}
{%- if values.language == "typescript" %}
```bash
# Development mode
{%- if values.packageManager == "pnpm" %}
pnpm dev
{%- elif values.packageManager == "yarn" %}
yarn dev
{%- else %}
npm run dev
{%- endif %}

# Production mode
node build/index.js
```
{%- else %}
```bash
# Development mode
python -m src.server

# Or using the installed command
${{ values.name }}
```
{%- endif %}
{%- else %}
{%- if values.language == "typescript" %}
```bash
# Start HTTP server on port 8000
{%- if values.packageManager == "pnpm" %}
pnpm start
{%- elif values.packageManager == "yarn" %}
yarn start
{%- else %}
npm start
{%- endif %}
```
{%- else %}
```bash
# Start HTTP server on port 8000
python -m src.server
```
{%- endif %}
{%- endif %}

### Testing with MCP Inspector

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

## Claude Desktop Configuration

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "${{ values.name }}": {
{%- if values.language == "typescript" %}
      "command": "node",
      "args": ["/path/to/${{ values.name }}/build/index.js"]
{%- else %}
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/${{ values.name }}"
{%- endif %}
    }
  }
}
```

## Capabilities

{%- if values.enableTools %}

### Tools

| Tool | Description |
|------|-------------|
| `echo` | Echo back a message |
| `get_time` | Get current date and time |
{%- if values.enableHttp %}
| `fetch_url` | Fetch content from a URL |
{%- endif %}
{%- endif %}

{%- if values.enableResources %}

### Resources

| Resource | Description |
|----------|-------------|
| `server://info` | Server information and capabilities |
{%- if values.enableFileSystem %}
| `file://{path}` | Read files from allowed directory |
{%- endif %}
{%- endif %}

{%- if values.enablePrompts %}

### Prompts

| Prompt | Description |
|--------|-------------|
| `code_review` | Review code for quality |
| `explain` | Explain a concept |
{%- endif %}

## Development

```bash
{%- if values.language == "typescript" %}
# Run tests
{%- if values.packageManager == "pnpm" %}
pnpm test
{%- elif values.packageManager == "yarn" %}
yarn test
{%- else %}
npm test
{%- endif %}

# Run linting
{%- if values.packageManager == "pnpm" %}
pnpm lint
{%- elif values.packageManager == "yarn" %}
yarn lint
{%- else %}
npm run lint
{%- endif %}

# Type check
{%- if values.packageManager == "pnpm" %}
pnpm typecheck
{%- elif values.packageManager == "yarn" %}
yarn typecheck
{%- else %}
npm run typecheck
{%- endif %}
{%- else %}
# Run tests
pytest tests -v

# Run linting
ruff check src tests

# Type check
mypy src
{%- endif %}
```

## Support

- **Slack**: #platform-help
- **Docs**: [Internal Platform Docs](https://docs.yourcompany.com)
