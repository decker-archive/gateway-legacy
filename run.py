import asyncio
import logging
import http
import os
import json
from dotenv import load_dotenv
from websockets import server
from gateway import handler, connection
from gateway.db import loop

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


async def health_check(path, head):
    if path == '/health':
        return http.HTTPStatus.OK, [], b'OK\n'
    elif path == '/available':
        return {
            http.HTTPStatus.OK,
            [],
            '{}'.format(get_available_gateway()).encode()
        }
    elif path == '/_dev/clients':
        return '{}'.format(len(connection.sessions)).encode()

async def echo_chamber(ws: server.WebSocketServerProtocol):
    while True:
        r = await ws.recv()
        break
    d = json.loads(r)
    await ws.send(json.dumps(d))
    await ws.close()


async def start_gateway():
    print('DEBUG:gateway:Starting Gateway')
    await asyncio.sleep(20)

    if os.getenv('environd', 'false') == 'true':
        await server.serve(
                handler.gateway_handler,
                '0.0.0.0',
                443,
                ping_timeout=20,
                process_request=health_check,
        )
    else:
        await server.serve(
            echo_chamber,
            '0.0.0.0',
            443,
            ping_timeout=1,
            process_request=health_check,
        )

def get_available_gateway():
    return 'https://gateway-prod-1.vincentrps.xyz'


loop.create_task(start_gateway())
loop.run_forever()
