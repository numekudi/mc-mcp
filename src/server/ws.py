import asyncio
import json
from typing import Set

import websockets

from server.broadcast_queue import queue

connected: Set[websockets.ServerConnection] = set()


async def handler(websocket: websockets.ServerConnection):
    connected.add(websocket)
    try:
        async for message in websocket:
            ...
    finally:
        connected.remove(websocket)


async def broadcast_loop():
    while True:
        message = await queue.get()
        if connected and message:
            await asyncio.gather(*(ws.send(json.dumps(message)) for ws in connected))


async def run_ws_server(
    host: str,
    port: int,
):
    server = await websockets.serve(handler, host, port)
    asyncio.create_task(broadcast_loop())

    await server.serve_forever()
