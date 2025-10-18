# -*- coding: utf-8 -*-
"""
ZhiYu_LabelKit - ComfyUI 自定义节点包
节点分类: ZhiYu/工具箱
包含：
- 批量加载图片
- 获取图片名称
- 格式转换
- 保存标签到 TXT
"""

from .batch_image_loader import BatchImageLoaderNode
from .get_image_name import GetImageNameNode
from .format_converter import FormatConverterNode
from .save_label_to_txt import SaveLabelToTxtNode

NODE_CLASS_MAPPINGS = {
    "BatchImageLoaderNode": BatchImageLoaderNode,
    "GetImageNameNode": GetImageNameNode,
    "FormatConverterNode": FormatConverterNode,
    "SaveLabelToTxtNode": SaveLabelToTxtNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoaderNode": "批量加载图片",
    "GetImageNameNode": "获取图片名称",
    "FormatConverterNode": "格式转换",
    "SaveLabelToTxtNode": "保存标签到TXT",
}
