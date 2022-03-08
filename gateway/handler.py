import asyncio
import json
from typing import Dict, List
from .connection import GatewayConnection, sessions, secret
from websockets import server

available: Dict[str, List] = {}

async def gateway_handler(ws: server.WebSocketServerProtocol):
    try:
        while True:
            r = await ws.recv()

            d: dict = json.loads(r)

            if not isinstance(d, dict):
                await ws.close(4002, 'Invalid Payload Type')
            
            if len(sessions[ws.port]) > 50000:
                await ws.close(4003, 'Too much users on port')
                break

            try:
                encoding = d['encoding']
            except (KeyError, IndexError):
                encoding = 'json'

            connection = GatewayConnection(ws, encoding)

            break
        try:
            await connection.run(d)
            await asyncio.Future()
        except UnboundLocalError:
            # invalid port.
            return

    except asyncio.CancelledError:
        pass
