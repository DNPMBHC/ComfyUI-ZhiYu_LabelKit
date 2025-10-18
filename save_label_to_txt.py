"""        ComfyUI custom node: SaveLabelToTxt

功能：根据图片路径创建同名 .txt 文件并写入标签文本（支持覆盖/追加）。
兼容：接收单条路径、分号分隔的多路径字符串、或者列表类型（若上游节点返回 list）。
"""

import os
import sys
import traceback

# ComfyUI 自带模块，节点运行时会从 ComfyUI 路径中找到它
import folder_paths

class SaveLabelToTxt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 接受单字符串、分号分隔的字符串或 list/tuple
                "files": ("STRING", {"default": ""}),
                # 要写入的文本内容
                "label": ("STRING", {"default": ""}),
                # True = 追加到已有文件，False = 覆盖
                "append": ("BOOLEAN", {"default": False}),
                # 是否在写入前去除文件名中的注记（如 [output]），通常不需要改
                "strip_annotation": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("txt_paths",)
    CATEGORY = "IO/Label"
    FUNCTION = "save_label"

    def _normalize_to_list(self, files):
        # 支持 list/tuple 直接传入
        if isinstance(files, (list, tuple)):
            return [str(f) for f in files if f]

        # 空字符串
        if not files:
            return []

        s = str(files)
        # 常见分隔符：; | ,
        for sep in (';', '|', ','):
            if sep in s:
                parts = [p.strip() for p in s.split(sep) if p.strip()]
                return parts

        return [s]

    def _resolve_path(self, f, strip_annotation=True):
        """解析路径或注记路径，返回绝对路径（如果无法解析，尽量返回合理的相对/注记解析结果）。
        支持的输入示例：
          - C:\\path\\to\\image.png
          - images/image.png [output]
          - image.png
        """
        if not f:
            return None

        f = str(f).strip()

        # 有注记时移除注记（可选）
        if strip_annotation and '[' in f and ']' in f:
            # 只去掉最后一个注记部分，如 "a.png [output]"
            try:
                base = f.split('[')[0].strip()
                if base:
                    f = base
            except Exception:
                pass

        # 1) 绝对路径且存在
        if os.path.isabs(f):
            return os.path.abspath(f)

        # 2) 相对路径存在
        if os.path.exists(f):
            return os.path.abspath(f)

        # 3) 尝试使用 ComfyUI 提供的 folder_paths 解析注记路径为真正路径
        try:
            annotated = folder_paths.get_annotated_filepath(f)
            if annotated:
                # annotated 可能是相对或绝对，返回绝对形式
                return os.path.abspath(annotated)
        except Exception:
            # 忽略解析错误，继续后续尝试
            pass

        # 4) 最后退回到相对路径（文件可能将在 later 节点生成）
        return os.path.abspath(f)

    def _safe_write(self, path, text, append=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as fo:
            fo.write(text)
            if not text.endswith('\n'):
                fo.write('\n')

    def save_label(self, files, label, append=False, strip_annotation=True):
        written = []

        try:
            items = self._normalize_to_list(files)
            if not items:
                return ("",)

            for item in items:
                resolved = self._resolve_path(item, strip_annotation)
                if not resolved:
                    continue

                folder = os.path.dirname(resolved)
                base = os.path.splitext(os.path.basename(resolved))[0]
                if not base:
                    # 跳过无法正确解析文件名的项
                    continue

                txt_name = base + ".txt"
                txt_path = os.path.join(folder, txt_name)

                try:
                    self._safe_write(txt_path, label, append=append)
                    written.append(txt_path)
                except Exception as e:
                    # 单文件写入失败不影响其他文件，记录到 stdout
                    print(f"[SaveLabelToTxt] 写入失败: {txt_path} -> {e}")
                    traceback.print_exc()
                    continue

        except Exception as e:
            print("[SaveLabelToTxt] 未处理的异常:", e)
            traceback.print_exc()
            return ("",)

        if not written:
            return ("",)

        # 返回以分号分隔的路径字符串，兼容大多数 ComfyUI 节点
        return (";".join(written),)


# ComfyUI 所需的节点映射（必须存在）
NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxt": SaveLabelToTxt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxt": "📝 Save Label To Txt"
}
