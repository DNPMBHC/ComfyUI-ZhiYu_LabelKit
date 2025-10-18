# -*- coding: utf-8 -*-

import subprocess
import sys
import os

def install_requirements():
    """安装 requirements.txt 中列出的依赖"""
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"[Install] 未找到 {requirements_file}，跳过依赖安装")
        return

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("[Install] 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print("[Install] 依赖安装失败:", e)
        print("[Install] 请手动检查网络或依赖名称")

if __name__ == "__main__":
    install_requirements()
