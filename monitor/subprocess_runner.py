import asyncio
import os

class SubprocessRunner:
    def __init__(self, cmd, name, shell=True):
        self.cmd = cmd
        self.name = name
        self.shell = shell

    def log(self, stream, *msgs):
        print(f"[{self.name}:{stream}]", *msgs)

    async def _read_stream(self, stream, stream_name, cb):
        while True:
            line = await stream.readline()
            if line:
                cb(line)
            else:
                self.log(stream_name, "stream finished")
                break

    async def _stream_subprocess(self, stdout_cb, stderr_cb):
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = "1"
        process = await asyncio.create_subprocess_shell(
                    self.cmd,
                    env = env,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        self.log('proc', f'spawned {self.cmd}')
        await asyncio.wait([
            self._read_stream(process.stdout, 'out', stdout_cb),
            self._read_stream(process.stderr, 'err', stderr_cb)
        ])
        return await process.wait()

    async def execute(self):
        return await self._stream_subprocess(
              lambda data: self.log("out", data),
              lambda data: self.log("err", data)
        )

    async def capture(self):
        sout = ""
        serr = ""
        def capture_out(data):
            nonlocal sout
            sout += str(data, 'utf8')
        def capture_err(data):
            nonlocal serr
            serr += str(data, 'utf8')
        code = await self._stream_subprocess(
            capture_out, capture_err
        )
        return sout, serr, code

