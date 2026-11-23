#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
SERVER="$HOME/llama.cpp/build/bin/llama-server"
MODEL="$HOME/models/DeepSeek-R1-Distill-Qwen-1.5B-Q2_K.gguf"
if [ ! -x "$SERVER" ]; then
  echo "llama-server missing. Run: bash setup-termux.sh"
  exit 1
fi
if [ ! -s "$MODEL" ]; then
  echo "Model missing. Run: bash download-model.sh"
  exit 1
fi
echo "Starting local server at 127.0.0.1:8080"
exec "$SERVER" -m "$MODEL" --host 127.0.0.1 --port 8080 --ctx-size 512 --threads 2
