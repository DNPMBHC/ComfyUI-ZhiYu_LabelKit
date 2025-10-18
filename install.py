# -*- coding: utf-8 -*-
"""
Minimal installer invoked by ComfyUI-Manager.
只尝试安装 requirements.txt（如果存在），不做额外操作。
"""

import subprocess
import sys
import os

def install_requirements():
    req = "requirements.txt"
    if not os.path.exists(req):
        print("[install] no requirements.txt found, skip.")
        return
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req])
        print("[install] requirements installed.")
    except subprocess.CalledProcessError as e:
        print("[install] failed to install requirements:", e)

if __name__ == "__main__":
    install_requirements()
