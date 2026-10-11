# Installing the StrikerAPI MCP server

StrikerAPI is a hosted (remote) MCP server over Streamable HTTP. There is nothing to clone, build or run locally.

## 1. Get an API key

Ask the user for their StrikerAPI API key. If they do not have one, they can create one free (500 credits, no card) at https://strikerapi.com/signup. Connecting and listing tools works without a key; calling a tool needs one.

## 2. Add the server

For Cline, add this to `cline_mcp_settings.json`, replacing YOUR_API_KEY:

```json
{
  "mcpServers": {
    "strikerapi": {
      "type": "streamableHttp",
      "url": "https://mcp.strikerapi.com/mcp",
      "headers": { "x-api-key": "YOUR_API_KEY" },
      "disabled": false
    }
  }
}
```

If the client cannot send headers, put the key in the URL instead: `https://mcp.strikerapi.com/mcp?key=YOUR_API_KEY`.

## 3. Check it works

Call `list_teams`. It costs 1 credit and confirms the key and connection.
