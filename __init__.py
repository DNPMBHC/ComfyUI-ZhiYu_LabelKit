# __init__.py
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

from .batch_image_loader import BatchImageLoader
from .get_image_name import GetImageName
from .format_converter import FormatConverter
from .save_label_to_txt import SaveLabelToTxt

NODE_CLASS_MAPPINGS = {
    "BatchImageLoader": BatchImageLoader,
    "GetImageName": GetImageName,
    "FormatConverter": FormatConverter,
    "SaveLabelToTxt": SaveLabelToTxt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoader": "批量加载图片",
    "GetImageName": "获取图片名称",
    "FormatConverter": "格式转换",
    "SaveLabelToTxt": "保存标签到TXT",
}
