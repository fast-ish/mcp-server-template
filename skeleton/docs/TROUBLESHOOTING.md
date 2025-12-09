# Troubleshooting

## Common Issues

### Server Won't Start

**Symptom:** Server exits immediately or shows errors on startup.

**Solutions:**

1. Check Node.js/Python version:
{%- if values.language == "typescript" %}
   ```bash
   node --version  # Should be ${{ values.nodeVersion }}+
   ```
{%- else %}
   ```bash
   python --version  # Should be ${{ values.pythonVersion }}+
   ```
{%- endif %}

2. Reinstall dependencies:
{%- if values.language == "typescript" %}
   ```bash
   rm -rf node_modules
{%- if values.packageManager == "pnpm" %}
   pnpm install
{%- elif values.packageManager == "yarn" %}
   yarn install
{%- else %}
   npm install
{%- endif %}
   ```
{%- else %}
   ```bash
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```
{%- endif %}

3. Check for missing environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with required values
   ```

### Claude Desktop Not Connecting

**Symptom:** Server doesn't appear in Claude Desktop.

**Solutions:**

1. Verify config file location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Check JSON syntax:
   ```bash
   cat ~/.config/Claude/claude_desktop_config.json | jq .
   ```

3. Use absolute paths in config:
   ```json
   {
     "mcpServers": {
       "${{ values.name }}": {
{%- if values.language == "typescript" %}
         "command": "node",
         "args": ["/absolute/path/to/build/index.js"]
{%- else %}
         "command": "/absolute/path/to/.venv/bin/python",
         "args": ["-m", "src.server"],
         "cwd": "/absolute/path/to/project"
{%- endif %}
       }
     }
   }
   ```

4. Restart Claude Desktop completely (quit from menu bar, not just close window)

### Tools Not Working

**Symptom:** Tools appear but return errors when called.

**Solutions:**

1. Test with MCP Inspector:
   ```bash
{%- if values.language == "typescript" %}
{%- if values.packageManager == "pnpm" %}
   pnpm inspect
{%- else %}
   npm run inspect
{%- endif %}
{%- else %}
   npx @modelcontextprotocol/inspector python -m src.server
{%- endif %}
   ```

2. Check server logs for errors:
{%- if values.language == "typescript" %}
   ```bash
   # Run directly to see stderr
   node build/index.js
   ```
{%- else %}
   ```bash
   # Run directly to see stderr
   python -m src.server
   ```
{%- endif %}

3. Verify input validation is passing:
   - Check that all required parameters are provided
   - Verify types match expected schema

{%- if values.enableFileSystem %}

### File Access Denied

**Symptom:** "Access denied: path outside allowed directory"

**Solutions:**

1. Set the allowed directory:
   ```bash
   export MCP_ALLOWED_DIR=/path/to/allowed/directory
   ```

2. Ensure the path is within the allowed directory:
   ```bash
   # Check resolved path
   readlink -f /path/to/file
   ```

3. Check file permissions:
   ```bash
   ls -la /path/to/file
   ```

{%- endif %}

{%- if values.enableDatabase %}

### Database Connection Failed

**Symptom:** "Connection refused" or "Authentication failed"

**Solutions:**

1. Verify DATABASE_URL format:
   ```bash
   # PostgreSQL
   export DATABASE_URL=postgresql://user:password@localhost:5432/dbname

   # SQLite
   export DATABASE_URL=sqlite:///./data.db
   ```

2. Check database is running:
   ```bash
   # PostgreSQL
   pg_isready -h localhost -p 5432
   ```

3. Test connection manually:
   ```bash
   psql $DATABASE_URL
   ```

{%- endif %}

### Build Errors

{%- if values.language == "typescript" %}

**Symptom:** TypeScript compilation fails.

**Solutions:**

1. Clear build cache:
   ```bash
   rm -rf build
{%- if values.packageManager == "pnpm" %}
   pnpm build
{%- else %}
   npm run build
{%- endif %}
   ```

2. Check for type errors:
   ```bash
{%- if values.packageManager == "pnpm" %}
   pnpm typecheck
{%- else %}
   npm run typecheck
{%- endif %}
   ```

3. Update dependencies:
   ```bash
{%- if values.packageManager == "pnpm" %}
   pnpm update
{%- else %}
   npm update
{%- endif %}
   ```

{%- else %}

**Symptom:** Import errors or missing modules.

**Solutions:**

1. Reinstall in editable mode:
   ```bash
   uv pip install -e ".[dev]"
   ```

2. Check for type errors:
   ```bash
   mypy src
   ```

3. Verify package structure:
   ```bash
   python -c "from src.server import create_server; print('OK')"
   ```

{%- endif %}

## Debug Mode

### Enable Verbose Logging

{%- if values.language == "typescript" %}
```bash
DEBUG=mcp:* node build/index.js
```
{%- else %}
```bash
export LOG_LEVEL=DEBUG
python -m src.server
```
{%- endif %}

### Use MCP Inspector

The MCP Inspector provides a web UI for testing:

```bash
npx @modelcontextprotocol/inspector {%- if values.language == "typescript" %} node build/index.js{%- else %} python -m src.server{%- endif %}
```

Features:
- List all tools, resources, and prompts
- Execute tools with custom inputs
- View raw JSON-RPC messages

## Getting Help

- **Slack**: #platform-help
- **MCP Docs**: https://modelcontextprotocol.io
- **GitHub Issues**: https://github.com/fast-ish/${{ values.name }}/issues
