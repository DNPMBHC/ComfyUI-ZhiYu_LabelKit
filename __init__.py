# -*- coding: utf-8 -*-

from .get_image_name import GetImageNameNode
from .save_label_to_txt import SaveLabelToTxtNode

NODE_CLASS_MAPPINGS = {
    "GetImageNameNode": GetImageNameNode,
    "SaveLabelToTxtNode": SaveLabelToTxtNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageNameNode": "获取图片名称",
    "SaveLabelToTxtNode": "保存标签到TXT",
}
