import asyncio
import os
import threading

from dotenv import load_dotenv

from server.mcp_server import run_mcp_server
from server.ws import run_ws_server

load_dotenv()


async def main():
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()

    host = os.environ.get("MC_MCP_WS_HOST", "localhost")
    port = int(os.environ.get("MC_MCP_WS_PORT", 9000))
    await run_ws_server(host, port)


if __name__ == "__main__":
    asyncio.run(main())
