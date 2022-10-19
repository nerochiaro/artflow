import asyncio
from aiohttp import web

class WorkerConnector:
    def __init__(self, port, exit, handlers):
        self.port = port
        self.exit = exit
        self.handlers = handlers
        self.app = web.Application()
        self.app.add_routes([web.post('/state', self._handle_state_update)])
        self.app.add_routes([web.post('/progress', self._handle_progress_update)])
        self.runner = web.AppRunner(self.app)

    async def _handle_state_update(self, request):
        json = await request.json()
        print("RECEIVED STATE FROM CLIENT:", json)
        if 'state' in self.handlers:
            await self.handlers['state'](json)
        return web.Response(text="OK")

    async def _handle_progress_update(self, request):
        json = await request.json()
        print("RECEIVED PROGRESS FROM CLIENT:", json)
        if 'progress' in self.handlers:
            await self.handlers['progress'](json)
        return web.Response(text="OK")

    async def run(self):
        print(f"Starting WorkerConnector on port {self.port}")
        await self.runner.setup()
        # Only listen to local connections
        site = web.TCPSite(self.runner, port=self.port)
        try:
            await site.start()
        except OSError as e:
            print("OS Error starting server", e)
            return e
        
        print("WorkerConnector listening on port", self.port)
        try:
            # Wait forever. The event loop will call into the server as routes are hit.
            # await will return when the exit event is triggered or we are interrupted.
            await self.exit.wait()
        except asyncio.CancelledError as ex:
            print("WorkerConnector Task cancelled!")
        finally:
            # Ensure ports are cleaned up
            print("WorkerConnector stopping")
            await site.stop()
            print("WorkerConnector has stopped")
