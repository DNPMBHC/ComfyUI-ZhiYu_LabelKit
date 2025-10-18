# -*- coding: utf-8 -*-

import os
from typing import Iterable, List, Union

def _split_paths_string(s: Union[str, Iterable]) -> List[str]:
    """把 ';' ',' '|' 分隔的字符串拆成列表；若为空返回空列表。
    如果传入的是可迭代（非字符串），将其逐项转换为字符串并返回非空项列表。
    """
    if s is None:
        return []
    # 如果是非字符串的可迭代（如 list/tuple），逐项处理
    if not isinstance(s, str):
        try:
            return [str(item).strip() for item in s if item is not None and str(item).strip()]
        except Exception:
            s = str(s)
    s = s.strip()
    if not s:
        return []
    for sep in (';', ',', '|'):
        if sep in s:
            return [p.strip() for p in s.split(sep) if p.strip()]
    if s.startswith('[') and s.endswith(']'):
        inner = s[1:-1].strip()
        if inner:
            items = [p.strip(" \"'") for p in inner.split(',') if p.strip()]
            return items
        return []
    # 多行文本也可能作为输入：按行拆分
    if '\n' in s:
        return [line.strip() for line in s.splitlines() if line.strip()]
    return [s]

def _strip_annotation(s: str) -> str:
    """去掉注记 '[xxx]'（如 'image.png [output]' -> 'image.png'）"""
    if not s:
        return s
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s

def _basename_no_ext(path_or_name: str) -> str:
    """返回文件名（不含扩展名）。如果传入的是路径，会取 basename 再去扩展名。"""
    try:
        name = os.path.basename(str(path_or_name))
        base = os.path.splitext(name)[0]
        return base
    except Exception:
        return str(path_or_name)

class GetImageNameNode:
    """
    单输入单输出节点（对外使用的类名：GetImageNameNode）
    INPUT: input (STRING) - 路径字符串或文件名或分隔的多路径（也支持 list/tuple）
    OUTPUT: text (STRING) - 每行一个文件名（不含扩展名）
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "process"
    CATEGORY = "ZhiYu/工具箱"
    NODE_DISPLAY_NAME = "获取图片名称 -> 文本 (简洁)"

    def process(self, input):
        parts = _split_paths_string(input)
        names = []
        for p in parts:
            if p is None:
                continue
            s = str(p).strip()
            if not s:
                continue
            s = _strip_annotation(s)
            n = _basename_no_ext(s)
            if n:
                names.append(n)
        # 去重且保持顺序
        seen = set()
        unique = []
        for n in names:
            if n not in seen:
                seen.add(n)
                unique.append(n)
        if not unique:
            return ("",)
        out_text = "\n".join(unique)
        return (out_text,)

# 导出给 ComfyUI 的映射（保持与 __init__.py 对应）
NODE_CLASS_MAPPINGS = {
    "GetImageNameNode": GetImageNameNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageNameNode": "获取图片名称 -> 文本"
}
