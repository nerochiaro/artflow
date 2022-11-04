import subprocess
import time

def open_tunnel(port)
    tunnel = subprocess.Popen(f"node tunnel.js ${port}", shell=True, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(1)  # TODO: ideally we should monitor the file and when it appears and is closed read it.
    try:
        url = open("/tmp/url", "r").read()
        return url
    except e:
        print(e)
        print(tun.stderr.read())
        return None
