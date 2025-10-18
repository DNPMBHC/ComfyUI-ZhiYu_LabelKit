# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：批量加载图片
节点分类：ZhiYu/工具箱
功能：
- 从文件夹或多路径加载图片
- 支持分号/逗号/竖线分隔的多路径字符串或列表输入
- 支持通配符、递归、注记去除（如 "image.png [output]"）
"""

from modules import nodes
import os
import glob
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

def _resolve_path_candidate(item, strip_annotation=True):
    """解析路径候选项（绝对/相对路径、并去注记），不依赖外部库"""
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    # 优先存在的绝对或相对路径
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    # 最后返回原始字符串（caller 决定是否认为它是路径）
    return os.path.abspath(s)

class BatchImageLoaderNode(nodes.Node):
    """
    批量加载图片节点
    Inputs:
        folder (STRING)
        paths (ANY) - 支持 PATH / STRING / LIST
        pattern (STRING) - 多个 pattern 用分号分隔
        recursive (BOOLEAN)
        strip_annotation (BOOLEAN)
        absolute (BOOLEAN)
    Returns:
        file_paths (STRING) - 分号分隔的绝对路径
        file_names (STRING) - 分号分隔的文件名
        file_list (LIST) - Python 列表
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
                "paths": ("ANY", {"default": ""}),
                "pattern": ("STRING", {"default": "*.png;*.jpg;*.jpeg"}),
                "recursive": ("BOOLEAN", {"default": False}),
                "strip_annotation": ("BOOLEAN", {"default": True}),
                "absolute": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "LIST")
    RETURN_NAMES = ("file_paths", "file_names", "file_list")
    FUNCTION = "load"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "批量加载图片"

    def _glob_from_folder(self, folder, patterns, recursive=False):
        results = []
        if not folder:
            return results
        folder = os.path.abspath(folder)
        for pat in patterns:
            pat = pat.strip()
            if not pat:
                continue
            if recursive:
                glob_path = os.path.join(folder, "**", pat)
                found = glob.glob(glob_path, recursive=True)
            else:
                glob_path = os.path.join(folder, pat)
                found = glob.glob(glob_path)
            for f in found:
                if os.path.isfile(f):
                    results.append(os.path.abspath(f))
        return results

    def load(self, folder, paths, pattern="*.png;*.jpg;*.jpeg", recursive=False, strip_annotation=True, absolute=True):
        try:
            collected = []

            # 从文件夹匹配
            if folder and str(folder).strip():
                pats = [p.strip() for p in str(pattern).split(';') if p.strip()]
                collected.extend(self._glob_from_folder(folder, pats, recursive=recursive))

            # 从 paths 字段加载（支持多种格式）
            for it in _to_list(paths):
                resolved = _resolve_path_candidate(it, strip_annotation=strip_annotation)
                if resolved:
                    collected.append(os.path.abspath(resolved) if absolute else resolved)

            # 去重且保留顺序
            seen = set()
            unique = []
            for p in collected:
                norm = os.path.abspath(p) if absolute else p
                if norm not in seen:
                    seen.add(norm)
                    unique.append(norm)

            if not unique:
                return ("", "", [])

            file_paths = ";".join(unique)
            file_names = ";".join([os.path.basename(p) for p in unique])
            file_list = unique

            return (file_paths, file_names, file_list)
        except Exception as e:
            print("[BatchImageLoaderNode] 错误:", e)
            traceback.print_exc()
            return ("", "", [])

# 兼容老的注册方式（ComfyUI 会扫描）
NODE_CLASS_MAPPINGS = {
    "BatchImageLoaderNode": BatchImageLoaderNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoaderNode": "批量加载图片"
}
