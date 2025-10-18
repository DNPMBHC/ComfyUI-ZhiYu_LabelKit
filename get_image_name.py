# -*- coding: utf-8 -*-

from modules import nodes
import os

class GetImageNameNode(nodes.Node):
    """
    获取图片名称
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_paths": ("ANY",),  # 支持 PATH / STRING / LIST
            }
        }

    RETURN_TYPES = ("STRING", "LIST", "PATH")
    RETURN_NAMES = ("as_string", "as_list", "as_path")
    FUNCTION = "get_names"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "获取图片名称"

    def get_names(self, input_paths):
        """
        输入：
            input_paths: STRING / LIST / PATH
        输出：
            as_string: 分号分隔的文件名
            as_list: Python 列表形式的文件名
            as_path: 路径列表，方便后续 PATH 类型节点使用
        """
        # 规范化输入为列表
        if input_paths is None:
            paths = []
        elif isinstance(input_paths, list):
            paths = input_paths
        elif isinstance(input_paths, str):
            # 支持 ; , | 分隔
            separators = [";", ",", "|"]
            for sep in separators:
                if sep in input_paths:
                    paths = [p.strip() for p in input_paths.split(sep) if p.strip()]
                    break
            else:
                paths = [input_paths.strip()]
        else:
            paths = [str(input_paths)]

        # 获取文件名
        names = [os.path.basename(p) for p in paths]

        # 输出三个端口
        as_string = "; ".join(names)
        as_list = names
        as_path = paths

        return as_string, as_list, as_path
