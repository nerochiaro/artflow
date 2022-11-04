from os import path
import asyncio
import aiohttp
from aiohttp import web
import json

class ClientConnector:
    def __init__(self, port, exit, ui_dir, onconnect):
        self.port = port
        self.exit = exit
        self.onconnect = onconnect
        self.app = web.Application()
        self.app.add_routes([web.get('/ws', self.websocket_handler)])
        self.app.add_routes([web.static('/ui', ui_dir)])
        self.ws = None

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print('Websocket connection ready')

        self.ws = ws
        if self.onconnect is not None:
          await self.onconnect(self.ws)

        async for msg in ws:
            print("received msg", msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())

        print('websocket connection closed')

        return ws

    async def run(self):
        self.runner = web.AppRunner(self.app)

        print(f"Starting ClientConnector on port {self.port}")
        await self.runner.setup()
        site = web.TCPSite(self.runner, port=self.port)
        try:
            await site.start()
        except OSError as e:
            print("OS Error starting server", e)
            return e
        
        print("ClientConnector listening on port", self.port)
        try:
            # Wait forever. The event loop will call into the server as routes are hit.
            # await will return when the exit event is triggered or we are interrupted.
            await self.exit.wait()
        except asyncio.CancelledError as ex:
            print("ClientConnector Task cancelled!")
        finally:
            # Ensure ports are cleaned up
            print("ClientConnector stopping")
            await site.stop()
            print("ClientConnector has stopped")

    async def on_state(self, state):
        await self.ws.send_str(json.dumps(state))
    async def on_progress(self, progress):
        await self.ws.send_str(json.dumps(progress))
