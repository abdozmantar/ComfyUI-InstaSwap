print(f"")
print(f"-----------------------------------------------------------------")
print(f"------Welcome InstaSwap Face Swapper ComfyUI Node Installer------")
print(f"-----------------------------------------------------------------")
print(f"")
print(f"")

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import subprocess
import os, sys, shutil
try:
    from pkg_resources import get_distribution as distributions
except:
    from importlib_metadata import distributions
from tqdm import tqdm
import urllib.request
from packaging import version as pv
try:
    from folder_paths import models_dir
except:
    from pathlib import Path
    models_dir = os.path.join(Path(__file__).parents[2], "models")

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")

model_url = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"
model_name = os.path.basename(model_url)
models_dir_path = os.path.join(models_dir, "insightface")
model_path = os.path.join(models_dir_path, model_name)


def run_pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-warn-script-location", *args])

def is_installed (
        package: str, version: str = None, strict: bool = True
):
    has_package = None
    try:
        has_package = distributions(package)
        if has_package is not None:
            if version is not None:
                installed_version = has_package.version
                if (installed_version != version and strict == True) or (pv.parse(installed_version) < pv.parse(version) and strict == False):
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False
    except Exception as e:
        print(f"Status: {e}")
        return False
    
def download(url, path):
    request = urllib.request.urlopen(url)
    total = int(request.headers.get('Content-Length', 0))
    with tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:
        urllib.request.urlretrieve(url, path, reporthook=lambda count, block_size, total_size: progress.update(block_size))

if not os.path.exists(models_dir_path):
    os.makedirs(models_dir_path)

if not os.path.exists(model_path):
    download(model_url, model_path)


with open(req_file) as file:
    try:
        onxx = "onnxruntime-gpu"
        import torch
        if torch.backends.mps.is_available() or hasattr(torch,'dml'):
            onxx = "onnxruntime"
        if not is_installed(onxx,"1.16.1",False):
            run_pip(onxx, "-U")
    except Exception as e:
        print(f"------------------------!ERROR!--------------------------------------")
        print(f"MODULE : {onxx}")
        print(f"InstaSwap probably wont work.")
        print(f"ERROR : ")
        print(e)
        print(f"---------------------------------------------------------------------")
        raise e
    strict = True
    for package in file:
        package_version = None
        try:
            print(f"INSTALLING PACKAGE : {package}")
            package = package.strip()
            if "==" in package:
                package_version = package.split('==')[1]
            elif ">=" in package:
                package_version = package.split('>=')[1]
                strict = False
            if not is_installed(package,package_version,strict):
                run_pip(package)
        except Exception as e:
            print(f"------------------------!ERROR!--------------------------------------")
            print(f"MODULE : {package}")
            print(f"InstaSwap probably wont work.")
            print(f"ERROR : ")
            print(e)
            print(f"---------------------------------------------------------------------")
            raise e

print("") 
print("")   
print(f"-----------------------------------------------------------------")
print(f"InstaSwap Installation completed successfuly !")
print(f"Please restart ComfyUI to access InstaSwap nodes")
