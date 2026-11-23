# AXLE AI

A local-first Android assistant using a small DeepSeek model through [llama.cpp](https://github.com/ggml-org/llama.cpp).

> **Important:** The target phone has 3 GB RAM. This is an experiment, not a guaranteed setup. The smallest test model is about 753 MB on disk, but inference needs additional memory for the runtime and context. Building llama.cpp on the phone may also fail from low memory. Stop if the phone becomes unstable or unusually hot.

## Project files

- `axle.py` — local text chat client, optional Termux voice input/output.
- `setup-termux.sh` — builds llama.cpp with one build job.
- `download-model.sh` — downloads the small Q2_K test model.
- `run-server.sh` — starts the local model server.
- `ANDROID-SETUP.md` — full step-by-step Android instructions.

## Quick start

Install Termux from its official project distribution, then run:

```sh
pkg update
pkg upgrade
pkg install python git
git clone https://github.com/sajilandr-ux/Flappy-bird.git
cd Flappy-bird/AXLE-AI
bash setup-termux.sh
bash download-model.sh
bash run-server.sh
```

Keep the server session open. In a second Termux session:

```sh
cd ~/Flappy-bird/AXLE-AI
python axle.py
```

For optional voice mode, install the Termux:API app from the same official distribution source as Termux, then run `pkg install termux-api` and `python axle.py --voice`.

See [ANDROID-SETUP.md](ANDROID-SETUP.md) for details and troubleshooting.

## Privacy

AXLE connects to `127.0.0.1` only. Do not expose the local model server to your Wi-Fi network or the public internet. This starter does not use a cloud AI API.

## References

- [llama.cpp Android instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md)
- [DeepSeek model card](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)
- [Quantized GGUF model](https://huggingface.co/tensorblock/DeepSeek-R1-Distill-Qwen-1.5B-GGUF)
