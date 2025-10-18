# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：获取图片名称
节点分类：ZhiYu/工具箱
功能：把 PATH/STRING/LIST 规范化并输出文件名（字符串/列表/路径）
"""

from modules import nodes
import os

class GetImageNameNode(nodes.Node):
    """
    获取图片名称节点
    Inputs:
        input_paths (ANY) - PATH/STRING/LIST
    Returns:
        as_string (STRING) - 文件名分号分隔
        as_list (LIST) - 文件名列表
        as_path (PATH) - 路径列表（LIST）用于连接 PATH 插口
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_paths": ("ANY",),
            }
        }

    RETURN_TYPES = ("STRING", "LIST", "PATH")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "get_names"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "获取图片名称"

    def get_names(self, input_paths):
        # 规范化为列表并过滤空值
        if input_paths is None:
            paths = []
        elif isinstance(input_paths, list):
            paths = [str(p) for p in input_paths if p]
        elif isinstance(input_paths, str):
            for sep in [";", ",", "|"]:
                if sep in input_paths:
                    paths = [p.strip() for p in input_paths.split(sep) if p.strip()]
                    break
            else:
                paths = [input_paths.strip()]
        else:
            paths = [str(input_paths)]

        names = [os.path.basename(p) for p in paths]
        as_string = "; ".join(names)
        as_list = names
        as_path = paths
        return (as_string, as_list, as_path)

NODE_CLASS_MAPPINGS = {
    "GetImageNameNode": GetImageNameNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageNameNode": "获取图片名称"
}
