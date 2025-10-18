# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：格式转换（STRING / LIST / PATH）
节点分类：ZhiYu/工具箱
"""

from modules import nodes
import os

class FormatConverterNode(nodes.Node):
    """
    输入：
        input_data (ANY) - STRING/LIST/PATH
        output_type (ENUM) - "STRING" / "LIST" / "PATH"
    输出：
        as_string, as_list, as_path
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data": ("ANY",),
                "output_type": (["STRING", "LIST", "PATH"], {"default": "LIST"}),
            }
        }

    RETURN_TYPES = ("STRING", "LIST", "PATH")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "convert"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "格式转换"

    def convert(self, input_data, output_type):
        if input_data is None:
            items = []
        elif isinstance(input_data, list):
            items = [str(i) for i in input_data if i]
        elif isinstance(input_data, str):
            for sep in [";", ",", "|"]:
                if sep in input_data:
                    items = [i.strip() for i in input_data.split(sep) if i.strip()]
                    break
            else:
                items = [input_data.strip()]
        else:
            items = [str(input_data)]

        as_string = "; ".join(items)
        as_list = items
        as_path = [os.path.abspath(i) for i in items] if output_type == "PATH" else []
        return (as_string, as_list, as_path)

NODE_CLASS_MAPPINGS = {
    "FormatConverterNode": FormatConverterNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FormatConverterNode": "格式转换"
}
