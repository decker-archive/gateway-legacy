import asyncio
import logging
import http
import json
from random import randint
from websockets import server
from gateway import handler, connection
from gateway.db import loop
from gateway.vendor import snowflake

logging.basicConfig(level=logging.DEBUG)

ports_ready = asyncio.Event()

async def health_check(path, head):
    if path == '/health':
        return http.HTTPStatus.OK, [], b'OK\n'


async def start_gateway():
    print('DEBUG:gateway:Starting Gateway')
    await asyncio.sleep(10)

    for port in range(49151):
        if port < 1024:
            pass
        if port > 10000:
            break
        else:
            try:
                await server.serve(
                    handler.gateway_handler,
                    '0.0.0.0',
                    port,
                    ping_timeout=20,
                    process_request=health_check,
                )
                handler.available[port] = []
                connection.sessions[port] = []
            except:
                pass

    ports_ready.set()

def get_port(ws) -> int:
    # port = randint(1024, 49151)
    port = randint(1024, 10000)

    av = connection.sessions.get(port)

    if av == None:
        return get_port(ws)

    if len(av) < 4000:
        return get_port(ws)

    return port

async def handle_port(ws: server.WebSocketServerProtocol):
    port = get_port(ws)
    id = snowflake.snowflake(port)
    
    connection.sessions[port].append(id)

    await ws.send(json.dumps({'url': f'wss://gateway.vincentrps.xyz:{port}', 'id': id}))
    # ws.remote_address
    await ws.close()

async def serve_port():
    print('DEBUG:gateway:Serving IPs!')
    await asyncio.sleep(5)

    try:
        await server.serve(
            handle_port,
            '0.0.0.0',
            443,
            ping_timeout=2,
            process_request=health_check
        )
    except:
        return await serve_port()

loop.run_until_complete(serve_port())
loop.run_until_complete(start_gateway())
loop.run_forever()
