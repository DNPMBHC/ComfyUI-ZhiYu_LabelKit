# __init__.py
# 使用显式导入：只暴露 ComfyUI 需要的映射，避免包导入时执行不必要的全局逻辑
from .save_label_to_txt import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
