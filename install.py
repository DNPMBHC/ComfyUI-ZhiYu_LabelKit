# -*- coding: utf-8 -*-

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
