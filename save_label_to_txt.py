# -*- coding: utf-8 -*-
"""
保存标签到 TXT（ZhiYu/工具箱）
"""

import os
import traceback

def _to_list(x):
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return [str(i) for i in x if i]
    s = str(x).strip()
    if not s:
        return []
    for sep in (';', '|', ','):
        if sep in s:
            return [p.strip() for p in s.split(sep) if p.strip()]
    return [s]

def _strip_annotation(s):
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s

def _resolve_path(item, strip_annotation=True):
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    # 若不存在，则返回原始字符串（作为基名处理）
    return s

def _write_text(path, text, append=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'a' if append else 'w'
    with open(path, mode, encoding='utf-8') as f:
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')

class SaveLabelToTxtNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_list": ("STRING", {"default": ""}),  # 分号分隔的路径或文件名
                "label_text": ("STRING", {"default": ""}),
                "output_dir": ("STRING", {"default": ""}),
                "append": ("BOOLEAN", {"default": False}),
                "auto_write": ("BOOLEAN", {"default": True}),
                "strip_annotation": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("txt_paths",)
    FUNCTION = "save"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "保存标签到TXT"

    def save(self, file_list, label_text, output_dir="", append=False, auto_write=True, strip_annotation=True):
        targets = []
        for p in _to_list(file_list):
            if not p:
                continue
            p2 = _strip_annotation(p) if strip_annotation else p
            resolved = _resolve_path(p2, strip_annotation=False)
            if resolved:
                targets.append(resolved)

        if not targets:
            return ("",)

        if auto_write and str(label_text).strip() != "":
            written = []
            for tgt in targets:
                try:
                    base = os.path.basename(tgt)
                    name_no_ext, ext = os.path.splitext(base)
                    if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff']:
                        folder = os.path.dirname(tgt)
                        txt_path = os.path.join(folder, name_no_ext + ".txt")
                    else:
                        txt_path = tgt if tgt.lower().endswith('.txt') else tgt + ".txt"

                    if output_dir and str(output_dir).strip():
                        base2 = os.path.splitext(os.path.basename(txt_path))[0]
                        txt_path = os.path.join(os.path.abspath(output_dir), base2 + ".txt")

                    _write_text(txt_path, str(label_text), append=append)
                    written.append(txt_path)
                except Exception as e:
                    print("[SaveLabelToTxtNode] 写入失败:", tgt, e)
                    traceback.print_exc()
                    continue

            return (";".join(written),)
        else:
            return (";".join(targets),)

NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxtNode": SaveLabelToTxtNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxtNode": "保存标签到TXT"
}
