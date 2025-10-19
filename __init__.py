# -*- coding: utf-8 -*-

from .batch_image_loader import BatchLoadImagesWithNames

NODE_CLASS_MAPPINGS = {
    "BatchLoadImagesWithNames": BatchLoadImagesWithNames,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchLoadImagesWithNames": "批量加载图片并提取名称",
}
