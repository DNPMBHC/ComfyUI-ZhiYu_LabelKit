from .batch_image_loader import (
    BatchLoadImagesWithNames,
    LoadImagesFromDirList,  # 等
    # ... 其他
)

NODE_CLASS_MAPPINGS = {
    "BatchLoadImagesWithNames": BatchLoadImagesWithNames,
    "LoadImagesFromDirList": LoadImagesFromDirList,
    # ... 更多键
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchLoadImagesWithNames": "批量加载图片并提取名称",
    "LoadImagesFromDirList": "列表加载目录图片",
    # ... 更多，建议用中文
}
