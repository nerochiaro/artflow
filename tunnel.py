import os
import subprocess
from install import run_subprocess

def run_tunnel():
    run_subprocess("npm install localtunnel") # install before running with npx to ensure npx's output doesn't pollute the actual output

    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen('npx localtunnel --port 9014', shell=True, stdout=subprocess.PIPE)
    line = proc.stdout.readline()  # read the first line, which either contains the tunnel address or an error message
    url = str(line, 'utf8').strip().replace('your url is: ', '')

    # return the first line and the process descriptor, without waiting for it to end (it won't unless it fails to open the tunnel)
    return url, proc