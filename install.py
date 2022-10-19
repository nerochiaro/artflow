import subprocess
import sys
import os
from os import path
from reporting import state

def get_path(leaf):
    root = os.environ.get('DRIVE_ROOT', '/content/drive/MyDrive/')
    return path.join(root, leaf)

def run_subprocess(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return proc.wait()

def install_hub(root):
    with state(f"Installing library huggingface_hub"):
      result = run_subprocess(f'pip3 install huggingface-hub --no-dependencies --target {root}')
      if result != 0: return False

def install_library(name, repo, version, root):
    with state(f"Installing library {name}"):
        repo_dir = f"/tmp/repo_{name}"
        run_subprocess(f"git clone --depth 1 --branch {version} {repo} {repo_dir}")
        run_subprocess(f"pip3 install git+file://{repo_dir} --no-dependencies --target {root}")

# load libraries from pre-installed archive in drive, or install them and create pre-installed archive in drive
def ensure_libraries():
    libs_root = '/content/libs'
    libs_archive = get_path('AI/libs.tar.gz')
    sys.path.append(libs_root)

    if os.access(libs_archive, os.R_OK):
        run_subprocess(f"cp {libs_archive} /content/ && cd /content/ && tar xvf libs.tar.gz")
    else:
        run_subprocess(f'mkdir -p {libs_root}')
        install_library('diffusers', 'https://github.com/huggingface/diffusers.git', 'v0.4.1', libs_root)
        install_library('transformers', 'https://github.com/huggingface/transformers.git', 'v4.22.2', libs_root)
        install_hub(libs_root)
        run_subprocess(f"cd /content/ && tar cvvzf {path.basename(libs_archive)} libs && cp -v {path.basename(libs_archive)} {path.dirname(libs_archive)}")
