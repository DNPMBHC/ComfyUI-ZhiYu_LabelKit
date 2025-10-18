# save_label_to_txt.py
import os
import traceback
try:
    import folder_paths
except Exception:
    folder_paths = None

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
    if os.path.isabs(s):
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

def _build_txt_from_components(image_path=None, image_name=None, output_dir=None, strip_annotation=True):
    if image_path:
        p = _resolve_path(image_path, strip_annotation=strip_annotation)
        if p:
            base = os.path.splitext(os.path.basename(p))[0]
            if base:
                return os.path.join(os.path.dirname(p), base + ".txt")
    if image_name:
        name = _strip_annotation(image_name) if strip_annotation else image_name
        base = os.path.splitext(os.path.basename(name))[0]
        if base:
            out = output_dir or os.getcwd()
            return os.path.join(os.path.abspath(out), base + ".txt")
    return None

def _write_text(path, text, append=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'a' if append else 'w'
    with open(path, mode, encoding='utf-8') as f:
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')

class SaveLabelToTxt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_list": ("LIST", {"default": []}),
                "file_paths": ("STRING", {"default": ""}),
                "图片路径": ("STRING", {"default": ""}),
                "图片名": ("STRING", {"default": ""}),
                "输出目录": ("STRING", {"default": ""}),
                "标签文本": ("STRING", {"default": ""}),
                "追加": ("BOOLEAN", {"default": False}),
                "自动写入": ("BOOLEAN", {"default": True}),
                "去除注记": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("txt_paths",)
    CATEGORY = "ZhiYu/Label"
    FUNCTION = "save"

    def save(self, file_list, file_paths, 图片路径, 图片名, 输出目录, 标签文本, 追加=False, 自动写入=True, 去除注记=True):
        targets = []

        # 优先使用 file_list（LIST）
        if file_list and isinstance(file_list, (list, tuple)) and len(file_list) > 0:
            for p in file_list:
                if p:
                    targets.append(os.path.abspath(str(p)))

        # 其次使用 file_paths（分号分隔字符串）
        if not targets and file_paths and str(file_paths).strip():
            for p in str(file_paths).split(';'):
                p = p.strip()
                if p:
                    targets.append(os.path.abspath(p))

        # 兼容旧的 图片路径 字段（可为多路径字符串）
        if not targets and 图片路径:
            for p in _to_list(图片路径):
                resolved = _resolve_path(p, strip_annotation=去除注记)
                if resolved:
                    targets.append(resolved)

        # 图片名 + 输出目录 组合
        if not targets and 图片名:
            t = _build_txt_from_components(image_name=图片名, output_dir=输出目录, strip_annotation=去除注记)
            if t:
                targets.append(t)

        # 如果仍未解析到任何目标，返回空
        if not targets:
            return ("",)

        # 自动写入（默认）或仅返回解析路径
        if 自动写入 and str(标签文本).strip() != "":
            written = []
            for tgt in targets:
                try:
                    # 若 tgt 是图片路径（有图片扩展名），把其同名 txt 作为目标
                    ext = os.path.splitext(tgt)[1].lower()
                    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff']:
                        folder = os.path.dirname(tgt)
                        base = os.path.splitext(os.path.basename(tgt))[0]
                        txt_path = os.path.join(folder, base + ".txt")
                    else:
                        # tgt 可能已经是 txt 路径或由图片名生成
                        txt_path = tgt if tgt.lower().endswith('.txt') else tgt + ".txt"
                    _write_text(txt_path, str(标签文本), append=追加)
                    written.append(txt_path)
                except Exception as e:
                    print("[SaveLabelToTxt] 写入失败:", tgt, e)
                    traceback.print_exc()
                    continue
            if not written:
                return ("",)
            return (";".join(written),)
        else:
            # 返回预解析的目标路径（分号分隔）
            return (";".join(targets),)

NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxt": SaveLabelToTxt
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxt": "保存标签到TXT"
}
