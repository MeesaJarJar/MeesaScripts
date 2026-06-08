# MeesaJarJar MeesaJarJar.com MeesaJarJar.shop Github.com/MeesaJarJar SDXL Setup Script
# Download, installs the required tools and model to run SDXL AI Image 2 Image Generation
import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RE_SCRIPTS = Path(r"C:\Program Files (x86)\UOForever\UO\ForeverOnline\RazorEnhanced\Scripts")
PYTHON_DIR = RE_SCRIPTS / "python_embedded"
PYTHON_EXE = PYTHON_DIR / "python.exe"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
GET_PIP_LOCAL = RE_SCRIPTS / "get-pip.py"
PYTHONDOWNLOAD = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip"
TORCH_INDEX = "https://download.pytorch.org/whl/cu126"
PYTHONDOWNLOAD_ZIP = RE_SCRIPTS / "python_embedded.zip"


def download(url, dest):
    print(f"  Downloading {url} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"  Saved to {dest}")


def run(cmd, check=True):
    print(f"  > {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    out = stdout.decode("utf-8", errors="replace")
    err = stderr.decode("utf-8", errors="replace")
    if out:
        last_lines = out.strip().split("\n")[-5:]
        print("\n".join(last_lines))
    if proc.returncode != 0 and check:
        print(f"  ERROR: {err[-500:]}")
        sys.exit(1)
    return proc


def main():
    print("=== SDXL Turbo Python Setup ===\n")
    print(f"Target: {PYTHON_DIR}\n")

    # Step 1: Download Python embeddable
    if PYTHON_EXE.exists():
        print(f"[OK] Python already installed at {PYTHON_DIR}")
    else:
        print("[1/4] Downloading Python 3.12 embeddable...")
        download(PYTHONDOWNLOAD, str(PYTHONDOWNLOAD_ZIP))

        print("  Extracting...")
        PYTHON_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(str(PYTHONDOWNLOAD_ZIP), "r") as zf:
            zf.extractall(str(PYTHON_DIR))

        try:
            PYTHONDOWNLOAD_ZIP.unlink()
        except:
            pass
        print(f"  Extracted to {PYTHON_DIR}")

        # Enable pip: uncomment import site in python312._pth
        pth_file = list(PYTHON_DIR.glob("python*._pth"))
        if pth_file:
            text = pth_file[0].read_text(encoding="utf-8")
            text = text.replace("#import site", "import site")
            pth_file[0].write_text(text, encoding="utf-8")
            print("  Enabled import site in ._pth file")

    # Step 2: Bootstrap pip
    print("\n[2/4] Bootstrapping pip...")
    if not GET_PIP_LOCAL.exists():
        download(GET_PIP_URL, str(GET_PIP_LOCAL))

    run([str(PYTHON_EXE), str(GET_PIP_LOCAL)])
    try:
        GET_PIP_LOCAL.unlink()
    except:
        pass

    # Step 3: Install packages
    print("\n[3/4] Installing packages (torch+cu124, diffusers, etc.)...")
    pip_exe = PYTHON_DIR / "Scripts" / "pip.exe"
    run([
        str(pip_exe), "install",
        "torch", "torchvision",
        "--index-url", TORCH_INDEX,
    ])
    run([
        str(pip_exe), "install",
        "diffusers==0.30.3", "transformers==4.44.2", "accelerate==0.34.2", "safetensors", "Pillow",
    ])

    # Step 4: Copy sdxl_server.py
    print("\n[4/4] Copying sdxl_server.py...")
    server_src = SCRIPT_DIR / "sdxl_server.py"
    server_dst = RE_SCRIPTS / "sdxl_server.py"
    if server_src.exists():
        if str(server_src.resolve()) != str(server_dst.resolve()):
            shutil.copy2(str(server_src), str(server_dst))
            print(f"  Copied to {server_dst}")
        else:
            print(f"  Already in place: {server_dst}")
    else:
        print(f"  WARNING: {server_src} not found, skipping copy")

    # Verify
    print("\nVerifying...")
    run([str(PYTHON_EXE), "-c", "import torch; import diffusers; print(f'torch={torch.__version__} CUDA={torch.cuda.is_available()} diffusers={diffusers.__version__}')"])

    print(f"\n=== DONE ===")
    print(f"Python: {PYTHON_EXE}")
    print(f"Server: {server_dst}")
    print(f"Run SDXLAutoReplace.py in-game — it uses this Python directly.")


if __name__ == "__main__":
    main()
