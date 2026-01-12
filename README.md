![LoRA Stacker](images/lora-stacker.png)

# ComfyUI LoRA Stacker

A simple ComfyUI custom node that lets you apply multiple LoRAs (up to 10) to a `MODEL` + `CLIP` in one node.

## Features

- Stack up to 10 LoRAs with individual weights
- UI button **Add LoRA** to reveal additional LoRA rows
- Uses the standard ComfyUI LoRA folder (`models/loras`)

## Installation

1. Go to your ComfyUI `custom_nodes` folder.
2. Clone this repository:

   ```bash
   git clone https://github.com/zwaigani/ComfyUI-LoRA-stacker.git
   ```

3. Restart ComfyUI.

## Usage

- Add the node **LoRA Stacker (multi)** (node id: `LoRA Stacker`) from category `loaders`.
- Connect your `MODEL` and `CLIP`.
- Select `lora_1_name` + set `lora_1_weight`.
- Click **Add LoRA** to show `lora_2_*` … `lora_10_*`.
- Setting a LoRA name to `None` or weight to `0` skips it.

Note: The screenshot path in this README expects an image at `images/lora-stacker.png`.

---

# ComfyUI LoRA Stacker（日本語）

`MODEL` と `CLIP` に対して、複数の LoRA（最大 10 個）を 1 つのノードで適用できる ComfyUI カスタムノードです。

## 特徴

- 最大 10 個の LoRA を個別の重みで積み重ね可能
- **Add LoRA** ボタンで LoRA 行を追加表示
- ComfyUI 標準の LoRA フォルダ（`models/loras`）を利用

## インストール

1. ComfyUI の `custom_nodes` フォルダへ移動します。
2. このリポジトリを clone します：

   ```bash
   git clone https://github.com/zwaigani/ComfyUI-LoRA-stacker.git
   ```

3. ComfyUI を再起動します。

## 使い方

- カテゴリ `loaders` の **LoRA Stacker (multi)**（ノードID: `LoRA Stacker`）を追加します。
- `MODEL` と `CLIP` を接続します。
- `lora_1_name` と `lora_1_weight` を設定します。
- **Add LoRA** を押すと `lora_2_*` 〜 `lora_10_*` が表示されます。
- LoRA 名が `None`、または重みが `0` のものはスキップされます。

注：この README の先頭画像は `images/lora-stacker.png` を参照しています。
