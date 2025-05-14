import asyncio
import os
from typing import Optional, Set

import websockets


class WebSocketServerManager:
    def __init__(self, host: str = "localhost", port: int = 9000):
        self.host = host
        self.port = port
        self._server: Optional[websockets.Server] = None
        self._task: Optional[asyncio.Task] = None
        self.connected: Set[websockets.ServerConnection] = set()

    @property
    def is_running(self) -> bool:
        return self._server is not None

    async def start(self) -> str:
        if self._server is not None:
            return "WebSocket server is already running."

        self._server = await websockets.serve(handler, self.host, self.port)

        self._task = asyncio.create_task(self._server.wait_closed())

        return f"WebSocket server started at ws://{self.host}:{self.port}"

    async def stop(self) -> str:
        if self._server is None:
            return "WebSocket server is not running."

        self._server.close()
        await self._server.wait_closed()
        self._server = None

        if self._task:
            self._task.cancel()
            self._task = None

        return "WebSocket server stopped."


host = os.environ.get("MC_MCP_WS_HOST", "localhost")
port = int(os.environ.get("MC_MCP_WS_PORT", 9000))
server_manager = WebSocketServerManager(host, port)


async def handler(websocket: websockets.ServerConnection):
    server_manager.connected.add(websocket)
    try:
        async for message in websocket:
            ...
    finally:
        server_manager.connected.remove(websocket)


async def run_ws_server():
    await server_manager.start()
    return server_manager
