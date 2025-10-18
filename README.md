# ComfyUI-SaveLabelToTxt

A simple ComfyUI custom node that creates a `.txt` file with the same name in the same directory as an image, and saves the input label text (can overwrite or append).

## Features
- Supports absolute paths output by **SaveImage**.
- Supports ComfyUI annotated paths (e.g. `image.png [output]`) and resolves them via `folder_paths.get_annotated_filepath`.
- Supports writing to multiple files (semicolon, pipe, or comma-separated strings, or direct list input).

## Installation
1. Go to your ComfyUI installation directory and open the `custom_nodes` folder.
2. Clone this repository or copy the folder manually.

> ⚠️ **Note:** When placing this folder under `ComfyUI/custom_nodes`, make sure the folder name does **not** contain hyphens (`-`).  
> Recommended: clone to `ComfyUI_SaveLabelToTxt` (with an underscore).

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/DNPMBHC/ComfyUI-SaveLabelToTxt.git ComfyUI_SaveLabelToTxt
