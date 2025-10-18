# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：格式转换节点
节点分类：ZhiYu/工具箱
功能：统一转换 PATH / STRING / LIST 格式
"""

from modules import nodes
import os


class FormatConverterNode(nodes.Node):
    """
    将路径 / 字符串 / 列表进行互相转换，方便节点对接
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data": ("ANY",),  # 支持任意类型输入
                "output_type": (
                    ["STRING", "LIST", "PATH"],
                    {"default": "LIST"},
                ),
            }
        }

    RETURN_TYPES = ("STRING", "LIST", "PATH")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "convert"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "格式转换"

    def convert(self, input_data, output_type):
        """
        输入：
            input_data: STRING / LIST / PATH
            output_type: 目标类型 STRING / LIST / PATH
        输出：
            as_string: 分号分隔字符串
            as_list: Python 列表
            as_path: 列表形式的路径，仅在 output_type 为 PATH 时返回
        """
        # 规范化输入为列表
        if input_data is None:
            items = []
        elif isinstance(input_data, list):
            items = [str(i) for i in input_data if i]
        elif isinstance(input_data, str):
            separators = [";", ",", "|"]
            for sep in separators:
                if sep in input_data:
                    items = [i.strip() for i in input_data.split(sep) if i.strip()]
                    break
            else:
                items = [input_data.strip()]
        else:
            items = [str(input_data)]

        # 输出端口
        as_string = "; ".join(items)
        as_list = items
        as_path = [os.path.abspath(i) for i in items] if output_type == "PATH" else []

        return as_string, as_list, as_path


NODE_CLASS_MAPPINGS = {
    "FormatConverterNode": FormatConverterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FormatConverterNode": "格式转换"
}
