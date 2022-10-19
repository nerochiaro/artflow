import asyncio
from worker_connector import WorkerConnector
from client_connector import ClientConnector
from subprocess_runner import SubprocessRunner

async def tunnel():
    sr = SubprocessRunner('npx localtunnel --port 9014', 'localtunnel')
    out, err, exit = await sr.capture()
    print("Subprocess => ", out, err, exit)

exit = asyncio.Event()
client_conn = ClientConnector(9015, exit)
worker_conn = WorkerConnector(9014, exit, handlers={
    "state": client_conn.on_state,
    "progress": client_conn.on_progress
})

async def main():
    await asyncio.gather(
        tunnel(),
        worker_conn.run(),
        client_conn.run()
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())