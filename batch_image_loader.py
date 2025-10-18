# batch_image_loader.py
import os
import glob
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
    s = str(s)
    if '[' in s and ']' in s:
        return s.split('[')[0].strip()
    return s

def _annotated_to_path(s):
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
    if annotated and os.path.exists(annotated):
        return annotated
    if annotated:
        return annotated
    return os.path.abspath(s)

class BatchImageLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
                "paths": ("STRING", {"default": ""}),
                "pattern": ("STRING", {"default": "*.png;*.jpg;*.jpeg"}),
                "recursive": ("BOOLEAN", {"default": False}),
                "strip_annotation": ("BOOLEAN", {"default": True}),
                "absolute": ("BOOLEAN", {"default": True}),
            }
        }

    # 返回三路：路径字符串、文件名字符串、以及 Python 列表
    RETURN_TYPES = ("STRING", "STRING", "LIST")
    RETURN_NAMES = ("file_paths", "file_names", "file_list")
    CATEGORY = "ZhiYu/Loader"
    FUNCTION = "load"

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

            if folder and str(folder).strip():
                pats = [p.strip() for p in str(pattern).split(';') if p.strip()]
                collected.extend(self._glob_from_folder(folder, pats, recursive=recursive))

            path_items = _to_list(paths)
            for it in path_items:
                resolved = _resolve_path_candidate(it, strip_annotation=strip_annotation)
                if resolved:
                    collected.append(os.path.abspath(resolved) if absolute else resolved)

            # 保持顺序去重
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
            print("[BatchImageLoader] error:", e)
            traceback.print_exc()
            return ("", "", [])

NODE_CLASS_MAPPINGS = {
    "BatchImageLoader": BatchImageLoader
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageLoader": "批量加载图片"
}
