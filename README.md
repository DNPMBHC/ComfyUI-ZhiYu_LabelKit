# ComfyUI-SaveLabelToTxt

A simple ComfyUI custom node is used to create a '.txt 'with the same name in the same directory based on the image file name and save the input tag text (which can be overwritten or appended).

## Features
- Supports the absolute path output by SaveImage.
- Support ComfyUI for annotating paths (such as' image.png [output] ') and parsing through 'folder_paths.get_annotated_filepath'.
- Supports multi-file writing (semicolons, vertical lines or comma-separated strings, or directly passing into a list).

## Installation
1. Enter your ComfyUI installation directory and open the 'custom_nodes' folder.
2. Clone this repository or copy the folder to 'custom_nodes' :

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/ DNPMBHC /ComfyUI-SaveLabelToTxt.git
` ` `

3. Restart ComfyUI (or reload the custom node), and find the '📝 Save Label To Txt' node under the 'IO/Label' category in the left node column.

## Use
- 'files' : Image paths from SaveImage or other nodes, supporting single or multiple.
- 'label' : Text to be written.
- 'append' : True indicates append, and False indicates overwrite.
- 'strip_annotation' : Whether to remove annotations such as' [output] ', usually set to True.

The node will return the written '.txt 'path (multiple separated by'; ').

Frequently Asked Questions
- ** Nodes do not appear ** : Ensure that the folder name is a valid Python package name (without hyphens or Spaces), the directory contains' __init__.py 'and' NODE_CLASS_MAPPINGS '.
- **ModuleNotFoundError: folder_paths** : Please place the nodes under 'ComfyUI/custom_nodes/<folder>' and restart ComfyUI; Do not run node files directly outside the project.

"Permission"
MIT


# ComfyUI-SaveLabelToTxt

一个简单的 ComfyUI 自定义节点，用于根据图片文件名在同目录下创建同名 `.txt` 并把输入的标签文本保存进去（可覆盖或追加）。

## 特性
- 支持 SaveImage 输出的绝对路径。
- 支持 ComfyUI 注记路径（例如 `image.png [output]`）并通过 `folder_paths.get_annotated_filepath` 解析。
- 支持多文件写入（分号、竖线或逗号分隔的字符串，或直接传入列表）。

## 安装
1. 进入你的 ComfyUI 安装目录，打开 `custom_nodes` 文件夹。
2. 克隆本仓库或把文件夹复制到 `custom_nodes` 下：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/DNPMBHC/ComfyUI-SaveLabelToTxt.git
```

3. 重启 ComfyUI（或重载自定义节点），在左侧节点栏的 `IO/Label` 分类下找到 `📝 Save Label To Txt` 节点。

## 使用
- `files`：来自 SaveImage 或其他节点的图片路径，支持单个或多个。
- `label`：要写入的文本。
- `append`：True 表示追加，False 覆盖。
- `strip_annotation`：是否去掉诸如 `[output]` 的注记，通常设为 True。

节点会返回写入的 `.txt` 路径（多个以 `;` 分隔）。

## 常见问题
- **节点不出现**：确保文件夹名是合法的 Python 包名（无连字符、空格），目录下有 `__init__.py`，并含有 `NODE_CLASS_MAPPINGS`。
- **ModuleNotFoundError: folder_paths**：请把节点放到 `ComfyUI/custom_nodes/<folder>` 下并重启 ComfyUI；不要直接在项目外部运行节点文件。

## 许可
MIT
