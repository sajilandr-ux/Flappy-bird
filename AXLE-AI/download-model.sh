#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
MODEL_DIR="$HOME/models"
MODEL_NAME="DeepSeek-R1-Distill-Qwen-1.5B-Q2_K.gguf"
MODEL_URL="https://huggingface.co/tensorblock/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-1.5B-Q2_K.gguf"
mkdir -p "$MODEL_DIR"
if [ -s "$MODEL_DIR/$MODEL_NAME" ]; then
  echo "Model already exists: $MODEL_DIR/$MODEL_NAME"
  exit 0
fi
command -v curl >/dev/null 2>&1 || pkg install -y curl
echo "Downloading Q2_K test model (about 753 MB)..."
curl -fL --retry 2 "$MODEL_URL" -o "$MODEL_DIR/$MODEL_NAME"
echo "Saved to $MODEL_DIR/$MODEL_NAME"
