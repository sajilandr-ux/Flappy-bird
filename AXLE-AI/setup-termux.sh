#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
echo "Installing build tools..."
pkg update
pkg install -y git cmake clang make libandroid-spawn
if [ ! -d "$HOME/llama.cpp/.git" ]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp "$HOME/llama.cpp"
else
  echo "Using existing llama.cpp checkout."
fi
echo "Building with one job to reduce memory pressure..."
cmake -S "$HOME/llama.cpp" -B "$HOME/llama.cpp/build" -DCMAKE_BUILD_TYPE=Release -DGGML_OPENMP=OFF
cmake --build "$HOME/llama.cpp/build" --config Release -j1 --target llama-server
echo "Build complete. Next: bash download-model.sh"
