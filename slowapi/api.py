import os
import asyncio
from aiohttp import web

async def handle(request):
    delay = float(request.query.get('delay') or 1)
    await asyncio.sleep(delay)
    text = '延时时间:{}秒'.format(delay)
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=5200)