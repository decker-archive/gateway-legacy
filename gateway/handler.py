import asyncio
import json
import urllib.parse
from .connection import GatewayConnection
from .connection_v2 import GatewayConnection as ConnectionV2
from websockets import server

async def gateway_handler(ws: server.WebSocketServerProtocol, url):
    try:
        while True:
            r = await ws.recv()

            d: dict = json.loads(r)

            args = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)

            try:
                version = args['v'][0]
            except(KeyError, IndexError):
                version = "2"
            
            try:
                encoding = args['encoding'][0]
            except(KeyError, IndexError):
                encoding = 'json'

            if version == '1':
                connection = GatewayConnection(ws, encoding)
            elif version == '2':
                connection = ConnectionV2(ws, encoding)
            else:
                await ws.close(4007, 'Invalid Gateway Version')

            break

        await connection.run(d)
        await asyncio.Future()

    except asyncio.CancelledError:
        pass
