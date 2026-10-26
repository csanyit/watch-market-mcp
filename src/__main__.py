import argparse
import configparser
import chrono24
import os
import sys

from fastmcp import FastMCP
from pathlib import Path
from pydantic import Field

config = configparser.ConfigParser()
config_path = Path(__file__).resolve().parent / "watch_marketplace_mcp.properties"
if not config_path.is_file():
    raise FileNotFoundError(f"Config file not found: {config_path}")
config.read(config_path)

FASTMCP_HTTP_PORT = (
    os.getenv("FASTMCP_HTTP_PORT", "").strip()
    or config.get("FastMCP", "fastmcp.http.port")
)

mcp = FastMCP(name="Watch marketplace MCP Server")

@mcp.tool()
def search_watches(query: str = Field(
        description=(
            "The specific brand and model of the watch to search for, e.g.,"
            " 'Rolex Submariner' or 'Omega Speedmaster'. Avoid overly generic"
            " queries like 'watch'."
        )
    ),
    limit: int = Field(
        default=5,
        description=(
            "Maximum number of listing results to return. Recommended"
            " range is between 3 and 10 for optimal performance."
        ),
    ),) -> list:
  """Search for watches on watch marketplace.

  Use this tool when the user is searching for a specific watch model, wants to
  check market availability, or asks for price overviews. Returns basic listing
  data such as prices, condition, and seller information.
  """
  try:
    watch_query = chrono24.query(query)
    listings = list(watch_query.search(limit=limit))
    return listings
  except Exception as e:
    return [{"error": str(e)}]


@mcp.tool()
def get_watch_details(query: str = Field(
        description=(
            "The precise brand and model name to fetch detailed technical"
            " specifications for (e.g., 'Tudor Black Bay')."
        )
    ),
    limit: int = Field(
        default=2,
        description=(
            "Number of detailed listing items to fetch. Keep low (1 or 2) as"
            " detailed fetching requires more processing time."
        ),
    ),) -> list:
  """Fetch detailed watch specifications and technical data from Chrono24.

  Use this tool when the user asks for specific technical specs such as case
  diameter, movement/caliber, water resistance, dial color, or case material.
  """
  try:
    watch_query = chrono24.query(query)
    detailed_listings = list(watch_query.detailed_search(limit=limit))
    return detailed_listings
  except Exception as e:
    return [{"error": str(e)}]


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Watch marketplace MCP server")
  parser.add_argument("--http", help="Start MCP server in HTTP mode", required=False)
  args = parser.parse_args()
  if args.http:
    print(
        "Starting in HTTP/SSE on address http://localhost:${FASTMCP_HTTP_PORT}...",
        file=sys.stderr,
    )
    mcp.run(transport="sse", port=int(FASTMCP_HTTP_PORT))
  else:
    mcp.run(transport="stdio")
