# ComfyUI-ZhiYu_LabelKit

本节点包为 ComfyUI 自定义节点，提供以下功能：

- **批量加载图片**：支持文件夹、单路径、多路径（字符串/列表/PATH），可递归子目录，输出路径列表和文件名列表。
- **保存标签到 TXT 文件**：支持根据图片路径或文件名生成同名 TXT，支持追加、自动写入和去除注记。

## 节点路径

| 节点文件 | 类名 | 功能 |
|-----------|------|------|
| `ZhiYu/工具箱/batch_image_loader.py` | `BatchImageLoaderNode` | 批量加载图片 |
| `ZhiYu/工具箱/save_label_to_txt.py` | `SaveLabelToTxtNode` | 保存标签到 TXT 文件 |
| `ZhiYu/工具箱/get_image_name.py` | `GetImageNameNode` | 获取图片名称 |
| `ZhiYu/工具箱/format_converter.py` | `FormatConverterNode` | 路径/字符串/列表格式转换 |

## 安装

1. 克隆仓库到 ComfyUI `custom_nodes` 目录：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/DNPMBHC/ComfyUI-ZhiYu_LabelKit.git
```
## 使用说明

节点均位于分类 ZhiYu/工具箱 下。

输出类型统一支持 STRING / LIST / PATH，方便节点链式对接。

批量加载图片节点可与格式转换节点和获取图片名称节点连用，实现快速标签写入工作流。
