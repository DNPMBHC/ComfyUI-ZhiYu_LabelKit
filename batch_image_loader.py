# -*- coding: utf-8 -*-
"""
批量加载图片节点（ZhiYu/工具箱）

说明：
- 支持 folder（文件夹）和 paths（多路径字符串或单一路径）两种输入方式
- pattern 支持多个以分号分隔，例如 "*.png;*.jpg"
- paths 支持分号/逗号/竖线分隔或单一路径
- 返回多种格式，方便与其他节点对接：
    - file_paths (STRING): 分号分隔的绝对路径字符串
    - file_names (STRING): 分号分隔的文件名字符串
    - file_list (LIST): Python 列表（每项为绝对路径）——可直接连到接受 LIST / PATH 的节点
    - file_qwen_json (STRING): Qwen 风格的 JSON 字符串，格式为 [{"type":"image","image":"<path>"} , ...]
"""

import os
import glob
import json
import traceback

def _to_list(x):
    """将输入规范为列表；支持 list/tuple 或 多路径字符串（; , |）"""
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
    """去掉注记，例如 'image.png [output]' -> 'image.png'"""
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s

def _resolve_path_candidate(item, strip_annotation=True):
    """解析输入为路径候选项：优先存在的绝对/相对路径；否则返回绝对化字符串"""
    if not item:
        return None
    s = str(item).strip()
    if strip_annotation:
        s = _strip_annotation(s)
    # 已存在的绝对/相对路径优先
    if os.path.isabs(s) and os.path.exists(s):
        return os.path.abspath(s)
    if os.path.exists(s):
        return os.path.abspath(s)
    # 最后把它转为绝对路径字符串（caller 决定是否接受此路径）
    try:
        return os.path.abspath(s)
    except Exception:
        return s

class BatchImageLoaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),   # 文件夹路径（可空）
                "paths": ("STRING", {"default": ""}),    # 多路径字符串（分号/逗号/竖线）或单一路径
                "pattern": ("STRING", {"default": "*.png;*.jpg;*.jpeg"}),
                "recursive": ("BOOLEAN", {"default": False}),
                "strip_annotation": ("BOOLEAN", {"default": True}),
                "absolute": ("BOOLEAN", {"default": True}),
                "return_qwen_json": ("BOOLEAN", {"default": True}),  # 是否生成 Qwen 风格 JSON 字符串
            }
        }

    # 返回多种格式（STRING/STRING/LIST/STRING）
    RETURN_TYPES = ("STRING", "STRING", "LIST", "STRING")
    RETURN_NAMES = ("file_paths", "file_names", "file_list", "file_qwen_json")
    FUNCTION = "load"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "批量加载图片（ZhiYu）"

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

    def load(self, folder, paths, pattern="*.png;*.jpg;*.jpeg", recursive=False, strip_annotation=True, absolute=True, return_qwen_json=True):
        """
        返回值：
            file_paths (STRING)       -> 分号分隔的绝对路径字符串
            file_names (STRING)       -> 分号分隔的文件名字符串
            file_list (LIST)          -> Python 列表（绝对路径）
            file_qwen_json (STRING)   -> Qwen 风格 JSON 字符串（如果 return_qwen_json=True）
        """
        try:
            collected = []

            # 从 folder 按 pattern 收集
            if folder and str(folder).strip():
                pats = [p.strip() for p in str(pattern).split(';') if p.strip()]
                collected.extend(self._glob_from_folder(folder, pats, recursive=recursive))

            # 从 paths 字段加载（支持多格式）
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
                return ("", "", [], "")  # 空返回

            file_paths = ";".join(unique)
            file_names = ";".join([os.path.basename(p) for p in unique])
            file_list = unique  # Python 列表，RETURN_TYPES 中为 LIST，可直接连接到接受 LIST 的节点

            # 构建 Qwen 风格 JSON 字符串（如果需要）
            file_qwen_json = ""
            if return_qwen_json:
                qwen_items = []
                for p in unique:
                    qwen_items.append({"type": "image", "image": p})
                try:
                    file_qwen_json = json.dumps(qwen_items, ensure_ascii=False)
                except Exception:
                    # 兜底：用 str()
                    file_qwen_json = str(qwen_items)

            return (file_paths, file_names, file_list, file_qwen_json)

        except Exception as e:
            print("[BatchImageLoaderNode] 错误:", e)
            traceback.print_exc()
            return ("", "", [], "")

NODE_CLASS_MAPPINGS = {
    "BatchImageLoaderNode": BatchImageLoaderNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoaderNode": "批量加载图片（ZhiYu）"
}
