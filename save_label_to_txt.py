# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：保存标签到 TXT 文件
节点分类：ZhiYu/工具箱
"""

from modules import nodes
import os
import traceback

try:
    import folder_paths
except ImportError:
    folder_paths = None


def _to_list(x):
    """将输入转换为列表"""
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
    """去掉注记 [output] 等"""
    if not s:
        return s
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s


def _resolve_path(item, strip_annotation=True):
    """解析路径，支持 folder_paths 注记"""
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    if folder_paths:
        try:
            annotated = folder_paths.get_annotated_filepath(s)
            if annotated:
                return os.path.abspath(annotated)
        except Exception:
            pass
    return os.path.abspath(s)


def _write_text(path, text, append=False):
    """写入文本文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'a' if append else 'w'
    with open(path, mode, encoding='utf-8') as f:
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')


class SaveLabelToTxtNode(nodes.Node):
    """
    保存标签到 TXT 文件节点
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

    def save(
        self,
        file_list,
        label_text,
        output_dir="",
        append=False,
        auto_write=True,
        strip_annotation=True,
    ):
        """保存文本到目标路径"""
        targets = []

        # 解析 file_list
        for p in file_list:
            if p:
                resolved = _resolve_path(p, strip_annotation=strip_annotation)
                if resolved:
                    targets.append(resolved)

        if not targets:
            return ("",)

        # 自动写入
        if auto_write and label_text.strip():
            written = []
            for tgt in targets:
                try:
                    ext = os.path.splitext(tgt)[1].lower()
                    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff']:
                        folder = os.path.dirname(tgt)
                        base = os.path.splitext(os.path.basename(tgt))[0]
                        txt_path = os.path.join(folder, base + ".txt")
                    else:
                        txt_path = tgt if tgt.lower().endswith('.txt') else tgt + ".txt"

                    # 输出到指定目录
                    if output_dir:
                        base = os.path.splitext(os.path.basename(txt_path))[0]
                        txt_path = os.path.join(os.path.abspath(output_dir), base + ".txt")

                    _write_text(txt_path, str(label_text), append=append)
                    written.append(txt_path)
                except Exception as e:
                    print("[SaveLabelToTxt] 写入失败:", tgt, e)
                    traceback.print_exc()
                    continue

            if not written:
                return ("",)
            return (";".join(written),)
        else:
            # 如果不写入，仅返回解析后的路径
            return (";".join(targets),)


NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxtNode": SaveLabelToTxtNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxtNode": "保存标签到TXT"
}
