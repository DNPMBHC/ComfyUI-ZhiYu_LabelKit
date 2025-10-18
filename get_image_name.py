# -*- coding: utf-8 -*-
"""
获取图片名称节点（ZhiYu/工具箱）
"""

import os

class GetImageNameNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_paths": ("STRING", {"default": ""}),  # 支持多路径字符串
            }
        }

    # 返回全部为 STRING（用户在需要时自己 split）
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "get_names"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "获取图片名称"

    def _split_input(self, input_paths):
        if input_paths is None:
            return []
        s = str(input_paths).strip()
        if not s:
            return []
        for sep in [";", ",", "|"]:
            if sep in s:
                return [p.strip() for p in s.split(sep) if p.strip()]
        return [s]

    def get_names(self, input_paths):
        paths = self._split_input(input_paths)
        names = [os.path.basename(p) for p in paths]
        as_string = ";".join(names)
        as_list = ";".join(names)    # 以 STRING 形式返回列表内容（分号拼接）
        as_path = ";".join(paths)    # 路径也以分号拼接返回
        return (as_string, as_list, as_path)

NODE_CLASS_MAPPINGS = {
    "GetImageNameNode": GetImageNameNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageNameNode": "获取图片名称"
}
