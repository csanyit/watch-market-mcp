# Watch Marketplace MCP Server

A Model Context Protocol (MCP) server for searching Chrono24 watch listings and retrieving listing details.

## Start locally

Requires Python 3.10 or newer. From the project directory, install the project and its dependencies:

```bash
python -m pip install -e .
python src/__main__.py
```

### Using uv

Install [uv](https://docs.astral.sh/uv/), then run these commands from the project directory. `uv sync` creates a virtual environment and installs the project and its dependencies:

```bash
uv sync
uv run python src/__main__.py
```

The server runs over stdio by default. To run the HTTP/SSE transport instead:

```bash
python src/__main__.py --http=true
```

With uv:

```bash
uv run python src/__main__.py --http=true
```

## MCP client setup

For a local stdio connection, add a server entry to your MCP client's configuration. Replace the path with the absolute path to this project:

```json
{
  "mcpServers": {
    "watch-marketplace": {
      "command": "python",
      "args": ["/absolute/path/to/watch_mcp/src/__main__.py"]
    }
  }
}
```

If you want the MCP client to launch the server using the project's uv environment, use this configuration instead (replace the directory path):

```json
{
  "mcpServers": {
    "watch-marketplace": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/watch_mcp",
        "run",
        "python",
        "src/__main__.py"
      ]
    }
  }
}
```

Use the `search_watches` tool to find listings, for example with `query="Rolex Submariner"` and `limit=3`. Use `get_watch_details` for more detailed listing results.
