import { app } from "../../scripts/app.js";

const MAX_LORAS = 10;

function findWidget(node, name) {
  return node.widgets?.find((w) => w?.name === name);
}

function setWidgetVisible(widget, visible) {
  if (!widget) return;

  widget.hidden = !visible;
  widget.options = widget.options || {};
  widget.options.hidden = !visible;

  // Make hidden widgets take effectively no space.
  if (!widget.__origComputeSize) {
    widget.__origComputeSize = widget.computeSize;
  }
  widget.computeSize = visible
    ? widget.__origComputeSize
    : () => [0, -4];
}

function applyVisibility(node, count) {
  for (let i = 2; i <= MAX_LORAS; i++) {
    const visible = i <= count;
    setWidgetVisible(findWidget(node, `lora_${i}_name`), visible);
    setWidgetVisible(findWidget(node, `lora_${i}_weight`), visible);
  }
  node.setSize(node.computeSize());
  node.setDirtyCanvas(true, true);
}

app.registerExtension({
  name: "comfyui.lora_stacker",
  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData?.name !== "LoRA Stacker") return;

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const r = onNodeCreated?.apply(this, arguments);

      // Start with 1 LoRA row visible.
      this.properties = this.properties || {};
      this.properties.lora_count = this.properties.lora_count || 1;

      // Hide rows 2..N.
      applyVisibility(this, this.properties.lora_count);

      // Add button to reveal next LoRA row.
      this.addWidget("button", "Add LoRA", null, () => {
        const cur = this.properties.lora_count || 1;
        const next = Math.min(MAX_LORAS, cur + 1);
        this.properties.lora_count = next;
        applyVisibility(this, next);
      });

      return r;
    };
  },
});
