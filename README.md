# ComfyUI-ZhiYu_LabelKit

一个面向 ComfyUI 的小型节点包。  
**功能核心**：从目录批量加载图片并同时提取图片文件名（可直接返回路径列表 / 文件名列表）的工具节点。

> 说明：为了避免命名冲突，本仓库把“加载 + 提取名称”合并为一个节点 — 推荐在工作流中直接使用该节点的路径/名称输出连线到后续保存或标注节点。

---

## 包内主要节点（当前版本）
- `ZhiYu/工具箱/BatchLoadImagesWithNames`  
  - 类名（内部）：`BatchLoadImagesWithNames`  
  - 显示名（UI）：`批量加载图片并提取名称`  
  - 功能：从指定目录加载图片（支持 `.jpg` `.jpeg` `.png` `.webp`，可选 `.jxl`），输出：
    - `IMAGE`：单张或 batch 图像张量
    - `MASK`：单张或 batch mask
    - `FILE_PATHS`：以换行分隔的路径字符串（每行一个路径）
    - `FILE_NAMES`：以换行分隔的不含扩展名的文件名字符串（每行一个名称）
    - `COUNT`：加载图片数量（INT）
  - 参数：`directory`、`image_load_cap`、`start_index`、`load_always`、`sort_method`

- `ZhiYu/工具箱/SaveLabelToTxt`（可选）  
  - 类名：`SaveLabelToTxtNode`  
  - 功能：把传入的标签文本写入与图片同目录的同名 `.txt`（支持追加或覆盖），支持传入路径列表或换行字符串。

---

## 与源码的一致性说明
- 本 README 已与仓库中实际暴露的节点类名/显示名匹配；若你后来改动类名（或文件名），也请同步更新 `__init__.py` 中的 `NODE_CLASS_MAPPINGS`。  
- 仓库根目录目前含有：`__init__.py`、`get_image_name.py`、`requirements.txt` 等文件。若要合并或删除旧文件，请把不再使用的脚本归档或重命名，以避免导入冲突。:contentReference[oaicite:1]{index=1}

---

## 安装（推荐步骤）
1. 把仓库克隆到 ComfyUI 的 `custom_nodes` 目录下：  
