import os
import traceback
import folder_paths


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
    try:
        annotated = folder_paths.get_annotated_filepath(s)
        if annotated:
            return os.path.abspath(annotated)
    except Exception:
        pass
    return os.path.abspath(s)


def _build_txt_from_components(image_path=None, image_name=None, output_dir=None, strip_annotation=True):
    if image_path:
        p = _resolve_path(image_path, strip_annotation)
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
    CATEGORY = "IO/Label"
    FUNCTION = "save"

    def save(self, 图片路径, 图片名, 输出目录, 标签文本, 追加=False, 自动写入=True, 去除注记=True):
        targets = []

        # 从图片路径解析（支持多路径）
        items = _to_list(图片路径)
        for it in items:
            p = _resolve_path(it, strip_annotation=去除注记)
            if not p:
                continue
            base = os.path.splitext(os.path.basename(p))[0]
            if base:
                targets.append(os.path.join(os.path.dirname(p), base + ".txt"))

        # 若未解析到 target，尝试图片名 + 输出目录
        if not targets and 图片名:
            t = _build_txt_from_components(image_name=图片名, output_dir=输出目录, strip_annotation=去除注记)
            if t:
                targets.append(t)

        # 若同时给了图片名与输出目录，尝试补充
        if 图片名 and 输出目录:
            t2 = _build_txt_from_components(image_name=图片名, output_dir=输出目录, strip_annotation=去除注记)
            if t2 and t2 not in targets:
                targets.append(t2)

        if not targets:
            return ("",)

        # 自动写入且有标签文本时写入；否则返回解析出的目标路径
        if 自动写入 and str(标签文本).strip() != "":
            written = []
            for tgt in targets:
                try:
                    _write_text(tgt, str(标签文本), append=追加)
                    written.append(tgt)
                except Exception as e:
                    print("[SaveLabelToTxt] 写入失败:", tgt, e)
                    traceback.print_exc()
                    continue
            if not written:
                return ("",)
            return (";".join(written),)
        else:
            return (";".join(targets),)


NODE_CLASS_MAPPINGS = {
    "SaveLabelToTxt": SaveLabelToTxt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveLabelToTxt": "保存标签到TXT",
}
