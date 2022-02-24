import asyncio
import logging
import quart
from websockets import server
from gateway import handler

logging.basicConfig(level=logging.DEBUG)
app = quart.Quart(__name__)

async def start_gateway():
    print('Starting Gateway')
    await server.serve(handler.gateway_handler, '0.0.0.0', 443, ping_timeout=30)

@app.route('/')
async def heartbeat():
    d = {
        'http': 'https://hatsu.vincentrps.xyz',
        'gateway': 'wss://gateway.vincentrps.xyz'
    }

app.run('0.0.0.0', 443)
loop = asyncio.new_event_loop()
loop.run_until_complete(start_gateway())
loop.run_forever()