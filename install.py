# -*- coding: utf-8 -*-
"""
ComfyUI-ZhiYu_LabelKit 安装脚本
用于 ComfyUI-Manager 自动处理依赖
"""

import subprocess
import sys

def install_requirements():
    """
    安装 requirements.txt 中列出的依赖
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成")
    except subprocess.CalledProcessError as e:
        print("依赖安装失败:", e)

if __name__ == "__main__":
    install_requirements()
