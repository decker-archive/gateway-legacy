import asyncio
import json
from typing import Dict, List
from .connection import GatewayConnection, sessions
from websockets import server

available: Dict[str, List] = {}

async def gateway_handler(ws: server.WebSocketServerProtocol):
    try:
        while True:
            r = await ws.recv()

            d: dict = json.loads(r)

            valid_ws = False

            for key, _ in sessions.items():
                if key == ws.port:
                    sesions = sessions.get(key, [])
                    for session in sesions:
                        if d.get('id', '') == session:
                            valid_ws = True

            if not valid_ws:
                await ws.close(4001, 'Invalid Gateway ID for This Port')
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
