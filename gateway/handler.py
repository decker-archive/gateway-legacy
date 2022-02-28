import asyncio
import json
from .connection import GatewayConnection
from websockets import server

async def gateway_handler(ws: server.WebSocketServerProtocol):
    try:
        while True:
            r = await ws.recv()

            d: dict = json.loads(r)
            
            try:
                encoding = d['encoding']
            except(KeyError, IndexError):
                encoding = 'json'

            connection = GatewayConnection(ws, encoding)

            break

        await connection.run(d)
        await asyncio.Future()

    except asyncio.CancelledError:
        pass
