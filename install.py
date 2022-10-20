import subprocess
import sys
import os
from os import path
from reporting import state
from environment import content, drive
import tempfile

def run_subprocess(cmd):
    return subprocess.run(cmd, shell=True, check=True)

def install_hub(root):
    # TODO: control versioning of this library too. They all need to be in sync
    with state(f"Installing library huggingface_hub"):
      result = run_subprocess(f'pip3 install huggingface-hub --no-dependencies --target {root}')
      if result != 0: return False

def install_library(name, repo, version, root):
    with state(f"Installing library {name}"):
        repo_dir = tempfile.mkdtemp(prefix=f"lib_{name}_")
        run_subprocess(f"git -c advice.detachedHead=false clone --depth 1 --branch {version} {repo} {repo_dir}")
        run_subprocess(f"pip3 install git+file://{repo_dir} --no-dependencies --target {root}")

# load libraries from pre-installed archive in drive, or install them and create pre-installed archive in drive
def ensure_libraries():
    libs_root = content('libs')
    libs_archive_name = 'libs.tar.gz'
    libs_archive_path = drive('AI', libs_archive_name)
    tmp = tempfile.mkdtemp()

    if os.access(libs_archive_path, os.R_OK):
        # if there is a pre-loaded library bundle in drive, copy it to a local temporary path, then unzip it in the content root
        # (where it will create a subdirectory).
        run_subprocess(f"cp {libs_archive_path} {tmp} && cd {content()} && tar xvf {path.join(tmp, libs_archive_name)}")
    else:
        # otherwise install the necessary libraries in a subdirectory of the content root, then make a bundle of it and upload it
        # to drive. for this run they will be already available, and for the next run the bundle will be found and used.
        run_subprocess(f'mkdir -p {libs_root}')
        install_library('diffusers', 'https://github.com/huggingface/diffusers.git', 'v0.4.1', libs_root)
        install_library('transformers', 'https://github.com/huggingface/transformers.git', 'v4.22.2', libs_root)
        install_hub(libs_root)
        run_subprocess(f"cd {path.dirname(libs_root)} && tar cvvzf {libs_archive_name} {path.basename(libs_root)} && " +
                       f"cp -v {libs_archive_name} {path.dirname(libs_archive_path)}")

    # ensure the libraries can be found
    sys.path.append(libs_root)
