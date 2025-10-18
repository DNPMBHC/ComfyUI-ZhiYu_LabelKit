# -*- coding: utf-8 -*-
"""
批量加载图片节点（ZhiYu/工具箱）
"""

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
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    # 优先返回存在的路径，否则返回绝对化的字符串
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    return os.path.abspath(s)

class BatchImageLoaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
                "paths": ("STRING", {"default": ""}),  # 多路径字符串（分号/逗号/竖线）或单一路径
                "pattern": ("STRING", {"default": "*.png;*.jpg;*.jpeg"}),
                "recursive": ("BOOLEAN", {"default": False}),
                "strip_annotation": ("BOOLEAN", {"default": True}),
                "absolute": ("BOOLEAN", {"default": True}),
            }
        }

    # 全部用 STRING 返回（包含原本的 list），方便 ComfyUI 标准兼容
    RETURN_TYPES = ("STRING", "STRING", "STRING")
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

            # 从文件夹按 pattern 收集
            if folder and str(folder).strip():
                pats = [p.strip() for p in str(pattern).split(';') if p.strip()]
                collected.extend(self._glob_from_folder(folder, pats, recursive=recursive))

            # 从 paths 字段加载，支持分号/逗号/竖线分隔
            for it in _to_list(paths):
                resolved = _resolve_path_candidate(it, strip_annotation=strip_annotation)
                if resolved:
                    collected.append(os.path.abspath(resolved) if absolute else resolved)

            # 去重并保持顺序
            seen = set()
            unique = []
            for p in collected:
                norm = os.path.abspath(p) if absolute else p
                if norm not in seen:
                    seen.add(norm)
                    unique.append(norm)

            if not unique:
                return ("", "", "")

            file_paths = ";".join(unique)
            file_names = ";".join([os.path.basename(p) for p in unique])
            file_list = ";".join(unique)  # 也以分号拼接返回

            # 调试输出（如需可在启动时用 --verbose 查看）
            # print("[BatchImageLoaderNode] collected:", collected)

            return (file_paths, file_names, file_list)
        except Exception as e:
            print("[BatchImageLoaderNode] 错误:", e)
            traceback.print_exc()
            return ("", "", "")

NODE_CLASS_MAPPINGS = {
    "BatchImageLoaderNode": BatchImageLoaderNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoaderNode": "批量加载图片"
}
