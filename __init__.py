# ZhiYu/__init__.py
from . import batch_image_loader
from . import save_label_to_txt

NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(batch_image_loader.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(save_label_to_txt.NODE_CLASS_MAPPINGS)

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(batch_image_loader.NODE_DISPLAY_NAME_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(save_label_to_txt.NODE_DISPLAY_NAME_MAPPINGS)
