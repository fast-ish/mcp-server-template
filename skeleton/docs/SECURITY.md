# Security

## Overview

MCP servers can expose powerful capabilities to AI assistants. This document outlines security best practices.

## Principles

1. **Principle of Least Privilege** - Only expose necessary capabilities
2. **Input Validation** - Validate all inputs before processing
3. **Output Sanitization** - Sanitize outputs to prevent injection
4. **Access Control** - Restrict access to sensitive resources

## Input Validation

{%- if values.language == "typescript" %}

### Zod Schema Validation

All tool inputs are validated using Zod schemas:

```typescript
import { z } from "zod";

server.tool(
  "safe_tool",
  "A safely validated tool",
  {
    // Required string with length limits
    input: z.string().min(1).max(1000),
    // Optional enum with allowed values
    action: z.enum(["read", "write"]).optional(),
    // URL validation
    url: z.string().url(),
  },
  async ({ input, action, url }) => {
    // Inputs are guaranteed to match schema
  }
);
```

{%- else %}

### Pydantic Validation

All tool inputs are validated using Pydantic models:

```python
from pydantic import BaseModel, Field, field_validator

class SafeInput(BaseModel):
    # Required string with length limits
    input: str = Field(min_length=1, max_length=1000)
    # Optional enum with allowed values
    action: Literal["read", "write"] | None = None
    # URL validation
    url: str

    @field_validator("url")
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("Invalid URL")
        return v
```

{%- endif %}

{%- if values.enableFileSystem %}

## File System Security

### Path Traversal Prevention

Always validate paths are within allowed directories:

{%- if values.language == "typescript" %}
```typescript
import * as path from "path";

function validatePath(userPath: string, allowedDir: string): string {
  const resolved = path.resolve(allowedDir, userPath);

  if (!resolved.startsWith(allowedDir)) {
    throw new Error("Access denied: path outside allowed directory");
  }

  return resolved;
}
```
{%- else %}
```python
from pathlib import Path

def validate_path(user_path: str, allowed_dir: Path) -> Path:
    resolved = (allowed_dir / user_path).resolve()

    if not str(resolved).startswith(str(allowed_dir.resolve())):
        raise ValueError("Access denied: path outside allowed directory")

    return resolved
```
{%- endif %}

### Allowed Directory Configuration

Set the allowed directory via environment variable:

```bash
export MCP_ALLOWED_DIR=/safe/directory
```

{%- endif %}

{%- if values.enableHttp %}

## HTTP Request Security

### URL Validation

Validate URLs before making requests:

{%- if values.language == "typescript" %}
```typescript
function validateUrl(url: string): void {
  const parsed = new URL(url);

  // Block private networks
  const blockedHosts = ["localhost", "127.0.0.1", "0.0.0.0"];
  if (blockedHosts.includes(parsed.hostname)) {
    throw new Error("Access to private networks not allowed");
  }

  // Only allow HTTPS
  if (parsed.protocol !== "https:") {
    throw new Error("Only HTTPS URLs allowed");
  }
}
```
{%- else %}
```python
from urllib.parse import urlparse

def validate_url(url: str) -> None:
    parsed = urlparse(url)

    # Block private networks
    blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
    if parsed.hostname in blocked_hosts:
        raise ValueError("Access to private networks not allowed")

    # Only allow HTTPS
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs allowed")
```
{%- endif %}

{%- endif %}

{%- if values.enableDatabase %}

## Database Security

### Parameterized Queries

Always use parameterized queries to prevent SQL injection:

{%- if values.language == "typescript" %}
```typescript
// GOOD - Parameterized query
const result = await client.query(
  "SELECT * FROM users WHERE id = $1",
  [userId]
);

// BAD - String concatenation
const result = await client.query(
  `SELECT * FROM users WHERE id = ${userId}`  // VULNERABLE!
);
```
{%- else %}
```python
# GOOD - Parameterized query
await conn.execute(
    "SELECT * FROM users WHERE id = $1",
    user_id
)

# BAD - String formatting
await conn.execute(
    f"SELECT * FROM users WHERE id = {user_id}"  # VULNERABLE!
)
```
{%- endif %}

{%- endif %}

{%- if values.enableAuth %}

## Authentication (HTTP Transport)

### OAuth 2.1 Configuration

Configure OAuth for production HTTP deployments:

```bash
export OAUTH_CLIENT_ID=your-client-id
export OAUTH_CLIENT_SECRET=your-client-secret
export OAUTH_ISSUER_URL=https://auth.yourcompany.com
```

### Token Validation

Always validate tokens on every request:

1. Verify token signature
2. Check expiration
3. Validate issuer and audience
4. Check required scopes

{%- endif %}

## Error Handling

### Safe Error Messages

Don't expose internal details in error messages:

{%- if values.language == "typescript" %}
```typescript
try {
  await riskyOperation();
} catch (error) {
  // Log full error internally
  console.error("Internal error:", error);

  // Return safe message to client
  return {
    content: [{ type: "text", text: "Operation failed" }],
    isError: true,
  };
}
```
{%- else %}
```python
try:
    await risky_operation()
except Exception as e:
    # Log full error internally
    logger.error(f"Internal error: {e}")

    # Return safe message to client
    return [TextContent(type="text", text="Operation failed")]
```
{%- endif %}

## Security Checklist

- [ ] All inputs validated with schemas
- [ ] File paths checked against allowed directory
- [ ] URLs validated before HTTP requests
- [ ] Database queries parameterized
- [ ] Error messages sanitized
- [ ] Authentication configured (if HTTP transport)
- [ ] Secrets stored in environment variables
- [ ] Logging doesn't include sensitive data
