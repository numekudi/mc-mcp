from mcp.server.fastmcp import FastMCP

from server.broadcast_queue import queue
from server.schema import new_command_request

mcp = FastMCP("mc-mcp")


@mcp.tool()
async def send_command(command: str) -> str:
    """Send a command to the Minecraft server and return the response."""
    data = new_command_request(command)
    await queue.put(data)
    return f"Response: {command} successfully sent!"


def run_mcp_server():
    """Run the MCP server."""
    mcp.run(transport="stdio")
