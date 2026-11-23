# AXLE AI — Android setup

## Read this first

This setup is experimental on a phone with 3 GB RAM. The selected GGUF model is approximately 753 MB on disk, but inference also needs extra RAM for the model runtime and context. The llama.cpp build can also use substantial memory. It may fail on this phone; that does not mean you did anything wrong.

Keep the phone cool, close other apps, and do not repeatedly retry a build that runs out of memory. Keep several GB of storage free.

## 1. Install Termux

Install Termux only from its official project distribution (F-Droid or the Termux GitHub releases). Do not use APK mirror sites.

Open Termux and run:

```sh
pkg update
pkg upgrade
pkg install python git
```

## 2. Get AXLE's files

```sh
git clone https://github.com/sajilandr-ux/Flappy-bird.git
cd Flappy-bird/AXLE-AI
```

## 3. Build llama.cpp

```sh
bash setup-termux.sh
```

This builds with one job to reduce peak memory use. Building may still fail or Android may stop the process on a 3 GB device.

## 4. Download the test model

```sh
bash download-model.sh
```

This downloads DeepSeek-R1-Distill-Qwen-1.5B in Q2_K quantization (about 753 MB). It is very compressed and loses some answer quality; it is only a low-storage test model.

## 5. Start AXLE's local model server

```sh
bash run-server.sh
```

Leave this Termux session running. The server listens on 127.0.0.1 only.

## 6. Chat with AXLE

Open a second Termux session and run:

```sh
cd ~/Flappy-bird/AXLE-AI
python axle.py
```

For optional voice mode, install the Termux:API app from the same official distribution source as Termux, then in Termux run:

```sh
pkg install termux-api
python axle.py --voice
```

Voice support is optional. Start with text chat first.

## If something fails

Copy the last 10–20 lines of the error and share them. Do not share private tokens or passwords. If the phone gets unusually hot or Android becomes unstable, stop the process.

## References

- llama.cpp Android/Termux build notes: https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md
- DeepSeek model card: https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
- Quantized GGUF model files: https://huggingface.co/tensorblock/DeepSeek-R1-Distill-Qwen-1.5B-GGUF
