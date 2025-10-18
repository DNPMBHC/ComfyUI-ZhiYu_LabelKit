# -*- coding: utf-8 -*-
"""
格式转换节点（ZhiYu/工具箱）
"""

import os

class FormatConverterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data": ("STRING", {"default": ""}),
                "output_type": (["STRING", "LIST", "PATH"], {"default": "LIST"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "convert"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "格式转换"

    def _split_input(self, input_data):
        if input_data is None:
            return []
        s = str(input_data).strip()
        if not s:
            return []
        for sep in [";", ",", "|"]:
            if sep in s:
                return [p.strip() for p in s.split(sep) if p.strip()]
        return [s]

    def convert(self, input_data, output_type="LIST"):
        items = self._split_input(input_data)
        as_string = ";".join(items)
        as_list = ";".join(items)     # 以 STRING 返回列表（分号拼接）
        as_path = ";".join([os.path.abspath(i) for i in items]) if items else ""
        # 如果用户希望 PATH 类型，下游可自行 split 并用 PATH 插口接入
        return (as_string, as_list, as_path)

NODE_CLASS_MAPPINGS = {
    "FormatConverterNode": FormatConverterNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FormatConverterNode": "格式转换"
}
