from __future__ import annotations

from typing import Any

try:
    import folder_paths
    import comfy.sd
    import comfy.utils
except Exception as e:  # pragma: no cover
    folder_paths = None  # type: ignore
    comfy = None  # type: ignore
    _import_error = e
else:
    _import_error = None


MAX_LORAS = 10


def _lora_choices() -> list[str]:
    if folder_paths is None:
        return ["None"]
    return ["None"] + list(folder_paths.get_filename_list("loras"))


def _load_lora_file(path: str) -> Any:
    # ComfyUI versions differ: some accept safe_load=, some don't.
    try:
        return comfy.utils.load_torch_file(path, safe_load=True)
    except TypeError:
        return comfy.utils.load_torch_file(path)


class LoraStacker:
    @classmethod
    def INPUT_TYPES(cls):
        loras = _lora_choices()

        required: dict[str, Any] = {
            "model": ("MODEL",),
            "clip": ("CLIP",),
            "lora_1_name": (loras, {"default": "None"}),
            "lora_1_weight": (
                "FLOAT",
                {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
            ),
        }

        optional: dict[str, Any] = {}
        for i in range(2, MAX_LORAS + 1):
            optional[f"lora_{i}_name"] = (loras, {"default": "None"})
            optional[f"lora_{i}_weight"] = (
                "FLOAT",
                {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
            )

        return {"required": required, "optional": optional}

    RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_NAMES = ("model", "clip")
    FUNCTION = "apply"
    CATEGORY = "loaders"

    def apply(self, model, clip, **kwargs):
        if _import_error is not None:
            raise RuntimeError(
                "ComfyUI modules are not available. This node must be run inside ComfyUI. "
                f"Import error: {_import_error!r}"
            )

        # Collect inputs in order.
        lora_items: list[tuple[str, float]] = []

        name1 = kwargs.get("lora_1_name")
        weight1 = float(kwargs.get("lora_1_weight", 1.0))
        lora_items.append((name1, weight1))

        for i in range(2, MAX_LORAS + 1):
            name = kwargs.get(f"lora_{i}_name", "None")
            weight = float(kwargs.get(f"lora_{i}_weight", 1.0))
            lora_items.append((name, weight))

        for (lora_name, weight) in lora_items:
            if lora_name in (None, "", "None"):
                continue
            if weight == 0:
                continue

            lora_path = folder_paths.get_full_path("loras", lora_name)
            if not lora_path:
                raise FileNotFoundError(f"LoRA not found: {lora_name}")

            lora = _load_lora_file(lora_path)
            model, clip = comfy.sd.load_lora_for_models(model, clip, lora, weight, weight)

        return (model, clip)


NODE_CLASS_MAPPINGS = {
    "LoRA Stacker": LoraStacker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoRA Stacker": "LoRA Stacker (multi)"
}
