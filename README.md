# ComfyUI_SaveLabelToTxt

简洁的 ComfyUI 自定义节点：根据图片文件名在同目录下创建同名 `.txt` 并保存标签文本（覆盖或追加）。

## 特性
- 支持 SaveImage 的绝对路径输出。
- 支持 ComfyUI 注记路径（例如 `image.png [output]`），通过 `folder_paths.get_annotated_filepath` 解析。
- 支持多文件写入（分号、竖线或逗号分隔，或直接传入列表）。

## 安装
建议将目录名用下划线，避免 Python 导入问题：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/DNPMBHC/ComfyUI-SaveLabelToTxt.git ComfyUI_SaveLabelToTxt
