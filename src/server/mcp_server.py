import json

from mcp.server.fastmcp import FastMCP

from server.schema import new_command_request
from server.ws import run_ws_server, server_manager

mcp = FastMCP("mc-mcp")


@mcp.tool()
async def send_command(command: str) -> str:
    """Send a command to the Minecraft server and return the response."""
    data = new_command_request(command)
    for connection in server_manager.connected:
        await connection.send(json.dumps(data))
    return f"Response: {command} successfully sent!"


@mcp.tool()
async def start_websocket_server():
    """Start the Minecraft WebSocket API server. returns the server URL."""

    server = await run_ws_server()
    return f"WebSocket server started at ws://{server.host}:{server.port}"


@mcp.tool()
async def stop_websocket_server():
    """Stop the Minecraft WebSocket API server."""
    await server_manager.stop()
    return "WebSocket server stopped."


async def run_mcp_server():
    await mcp.run_stdio_async()
