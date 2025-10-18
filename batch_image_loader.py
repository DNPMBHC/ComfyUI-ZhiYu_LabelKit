# -*- coding: utf-8 -*-
"""
ComfyUI 自定义节点：批量加载图片
路径：ZhiYu/工具箱/batch_image_loader.py
"""

import os
import glob
import traceback

try:
    import folder_paths
except Exception:
    folder_paths = None


def _to_list(x):
    """将输入规范化为列表"""
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
    """去掉注记字符，例如 'xxx[注记]' -> 'xxx'"""
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s


def _annotated_to_path(s):
    """通过 folder_paths 获取注记路径"""
    if not folder_paths:
        return None
    try:
        p = folder_paths.get_annotated_filepath(s)
        if p:
            return os.path.abspath(p)
    except Exception:
        return None
    return None


def _resolve_path_candidate(item, strip_annotation=True):
    """解析路径候选项，优先使用绝对路径和注记路径"""
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    annotated = _annotated_to_path(s)
    if annotated:
        return os.path.abspath(annotated)
    return os.path.abspath(s)


class BatchImageLoaderNode:
    """
    批量加载图片节点
    输入：
        folder: 文件夹路径
        paths: PATH / STRING / LIST
        pattern: 文件匹配模式，如 *.png;*.jpg
        recursive: 是否递归子文件夹
        strip_annotation: 是否去除注记
        absolute: 是否返回绝对路径
    输出：
        file_paths: 分号分隔的文件路径
        file_names: 分号分隔的文件名
        file_list: Python 列表形式的路径
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
        """根据匹配模式从文件夹获取文件列表"""
        results = []
        if not folder:
            return results
        folder = os.path.abspath(folder)
        for pat in patterns:
            pat = pat.strip()
            if not pat:
                continue
            glob_path = os.path.join(folder, "**", pat) if recursive else os.path.join(folder, pat)
            found = glob.glob(glob_path, recursive=recursive)
            results.extend([os.path.abspath(f) for f in found if os.path.isfile(f)])
        return results

    def load(self, folder, paths, pattern="*.png;*.jpg;*.jpeg", recursive=False, strip_annotation=True, absolute=True):
        """执行图片加载"""
        try:
            collected = []

            # 从文件夹加载
            if folder and folder.strip():
                pats = [p.strip() for p in str(pattern).split(';') if p.strip()]
                collected.extend(self._glob_from_folder(folder, pats, recursive=recursive))

            # 从 paths 加载
            path_items = _to_list(paths)
            for it in path_items:
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
                return ("", "", [])

            file_paths = ";".join(unique)
            file_names = ";".join([os.path.basename(p) for p in unique])
            file_list = unique

            return (file_paths, file_names, file_list)

        except Exception as e:
            print("[BatchImageLoader] 错误:", e)
            traceback.print_exc()
            return ("", "", [])


NODE_CLASS_MAPPINGS = {
    "BatchImageLoaderNode": BatchImageLoaderNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoaderNode": "批量加载图片"
}
