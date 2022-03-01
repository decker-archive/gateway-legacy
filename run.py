import asyncio
import logging
import http
from websockets import server
from gateway import handler

logging.basicConfig(level=logging.DEBUG)


async def health_check(path, head):
    if path == '/health':
        return http.HTTPStatus.OK, [], b'OK\n'


async def start_gateway():
    print('DEBUG:gateway:Starting Gateway')
    await asyncio.sleep(3)
    await server.serve(
        handler.gateway_handler,
        '0.0.0.0',
        443,
        ping_timeout=30,
        process_request=health_check,
    )


loop = asyncio.new_event_loop()
loop.run_until_complete(start_gateway())
loop.run_forever()
