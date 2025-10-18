# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：保存标签到 TXT 文件
节点分类：ZhiYu/工具箱
说明：
- 支持接收 PATH 列表或文件名列表
- 默认在图片同目录生成同名 .txt（可用 output_dir 覆盖）
- 支持覆盖或追加写入
- 不依赖第三方 folder_paths 包（避免安装失败）
"""

from modules import nodes
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
    if not s:
        return s
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
    # 若路径不存在，则把它当作基名处理（后续会在 output_dir 中创建）
    return s

def _write_text(path, text, append=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'a' if append else 'w'
    with open(path, mode, encoding='utf-8') as f:
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')

class SaveLabelToTxtNode(nodes.Node):
    """
    保存标签到 TXT 文件节点
    Inputs:
        file_list (LIST) - 路径/文件名列表
        label_text (STRING)
        output_dir (STRING) - 覆盖输出目录，留空则放图片同目录
        append (BOOLEAN)
        auto_write (BOOLEAN)
        strip_annotation (BOOLEAN)
    Returns:
        txt_paths (STRING) - 分号分隔的写入路径或解析路径
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_list": ("LIST", {"default": []}),
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
        for p in file_list:
            if not p:
                continue
            p = _strip_annotation(str(p)) if strip_annotation else str(p)
            resolved = _resolve_path(p, strip_annotation=False)
            if resolved:
                targets.append(resolved)

        if not targets:
            return ("",)

        if auto_write and str(label_text).strip() != "":
            written = []
            for tgt in targets:
                try:
                    # 如果看起来像图片路径（有扩展名），生成同名 txt
                    base_name = os.path.basename(tgt)
                    name_no_ext, ext = os.path.splitext(base_name)
                    if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff']:
                        folder = os.path.dirname(tgt)
                        txt_path = os.path.join(folder, name_no_ext + ".txt")
                    else:
                        # tgt 可能只是文件名或已是 txt 路径
                        txt_path = tgt if tgt.lower().endswith('.txt') else tgt + ".txt"

                    if output_dir and str(output_dir).strip():
                        base = os.path.splitext(os.path.basename(txt_path))[0]
                        txt_path = os.path.join(os.path.abspath(output_dir), base + ".txt")

                    _write_text(txt_path, str(label_text), append=append)
                    written.append(txt_path)
                except Exception as e:
                    print("[SaveLabelToTxtNode] 写入失败:", tgt, e)
                    traceback.print_exc()
                    continue

            if not written:
                return ("",)
            return (";".join(written),)
        else:
            return (";".join(targets),)

NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxtNode": SaveLabelToTxtNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxtNode": "保存标签到TXT"
}
