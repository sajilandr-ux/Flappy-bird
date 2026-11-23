# AXLE AI

A lightweight, local-first voice and text assistant for Android, powered by an open-weight DeepSeek model through [llama.cpp](https://github.com/ggml-org/llama.cpp).

> **Device note:** The target phone has 3 GB RAM. A 1.5B quantized model is only a cautious experiment, not a guarantee. Android, the runtime, and the model's working memory all need RAM. Close other apps and stop if the phone becomes unstable or overheats.

## What this first version does

- Sends text prompts to a local llama.cpp server on the same phone.
- Keeps a short conversation history in memory.
- Optional voice input and spoken replies using Termux:API.
- Does not need a cloud API key; prompts stay on the local device when configured as documented.

## Project layout

- `axle.py` — terminal chat client and optional voice controls.
- `requirements.txt` — no third-party Python packages required.
- `config.example.json` — safe example settings.

## Android setup (Termux)

1. Install Termux from its official F-Droid or GitHub distribution. Avoid unofficial APK download sites.
2. In Termux, update packages and install the basic tools:

   ```sh
   pkg update && pkg upgrade
   pkg install python git
   ```

3. Install Termux:API from the same trusted distribution source as Termux. Then run:

   ```sh
   pkg install termux-api
   ```

   Voice features are optional. Text chat works without Termux:API.

4. Clone your repository and enter the project folder:

   ```sh
   git clone https://github.com/sajilandr-ux/Flappy-bird.git
   cd Flappy-bird/AXLE-AI
   ```

5. Set up llama.cpp and a compatible GGUF model by following the official llama.cpp Android/Termux build instructions: https://github.com/ggml-org/llama.cpp

   Choose a small DeepSeek-R1-Distill-Qwen GGUF quantization only if you understand that model size is not the same as total RAM use. Keep context small (start around 512–1024 tokens). A 1.5B model may still be too demanding for a 3 GB phone.

6. Start the local server. The exact executable path depends on how llama.cpp was built:

   ```sh
   ./llama-server -m /path/to/model.gguf --host 127.0.0.1 --port 8080 -c 1024 -t 2
   ```

7. Open a second Termux session, enter `AXLE-AI`, and start AXLE:

   ```sh
   python axle.py
   ```

   For voice mode:

   ```sh
   python axle.py --voice
   ```

## Commands

- Type a message and press Enter.
- Type `/clear` to clear the conversation.
- Type `/voice` to toggle voice mode (requires Termux:API).
- Type `/exit` to quit.

## Troubleshooting

- **Cannot connect:** Make sure `llama-server` is running on port 8080 in another Termux session.
- **Slow or out of memory:** Stop the server, close other apps, reduce context size, and consider a smaller model. Do not keep retrying if the phone overheats or becomes unstable.
- **Voice not working:** Check microphone permission and install Termux:API. Text mode does not need it.

## Privacy

AXLE connects only to the local address `127.0.0.1` by default. Do not expose the model server to your Wi-Fi network or the public internet. No telemetry or account login is included in this starter.

## Current status

This is an initial working starter, not a finished APK. The next stage is a proper Android interface and testing on the target phone.
