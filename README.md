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

## 快速开始（用户指南）

### 1. 安装
1. 把仓库克隆到 ComfyUI 的 custom_nodes 目录：
```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/DNPMBHC/ComfyUI-ZhiYu_LabelKit.git
