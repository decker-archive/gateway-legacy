import asyncio
import logging
from websockets import server
from gateway import handler

logging.basicConfig(level=logging.DEBUG)

async def start_gateway():
    print('Starting Gateway')
    await server.serve(handler.gateway_handler, '0.0.0.0', 443, ping_timeout=30)

loop = asyncio.new_event_loop()
loop.run_until_complete(start_gateway())
loop.run_forever()