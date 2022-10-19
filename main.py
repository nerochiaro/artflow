import subprocess
import sys
import os
from tqdm_patch import patch_tqdm
from install import ensure_libraries
from tunnel import run_tunnel

def main():
    try:
        patch_tqdm()
    except:
        print("Library tqdm not found. Not patching. Other things will fail.")

    url, proc = run_tunnel()
    print("Tunnel URL: ", url)

    ensure_libraries()

if __name__ == "__main__":
    main()

    import torch
    from time import time
    start = time()
    from diffusers import StableDiffusionPipeline
    from install import run_subprocess, get_path

    # try:
    #     pipe, out = StableDiffusionPipeline.from_pretrained(
    #         get_path('AI/models'), # "CompVis/stable-diffusion-v1-4", 
    #         revision="fp16", 
    #         torch_dtype=torch.float16,
    #         local_files_only=True,
    run_subprocess(f'rm {get_path("AI/models")} -rf')
    result = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        use_auth_token='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',
        revision="fp16", 
        torch_dtype=torch.float16,
        force_download=True,
    )
    # pipe.save_pretrained(get_path('AI/models')) 

    # from models.basic import Models
    # models = Models(get_path('AI/models'))
    # models.load()