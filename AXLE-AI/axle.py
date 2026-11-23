#!/usr/bin/env python3
"""AXLE AI: small local chat client for a llama.cpp OpenAI-compatible server."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "http://127.0.0.1:8080/v1/chat/completions"
SYSTEM_PROMPT = (
    "You are AXLE, a helpful, clear, and friendly personal AI assistant. "
    "Be honest about uncertainty. Keep answers concise unless asked for detail."
)


def termux_command(name: str, *, capture: bool = False, input_text: str | None = None) -> str:
    """Run an optional Termux:API command. Return captured text when requested."""
    if shutil.which(name) is None:
        raise RuntimeError(
            f"{name} was not found. Install Termux:API and its Android companion app."
        )
    result = subprocess.run(
        [name],
        input=input_text,
        text=True,
        capture_output=capture,
        check=False,
        timeout=90,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "command failed").strip()
        raise RuntimeError(message)
    return (result.stdout or "").strip() if capture else ""


class Axle:
    def __init__(self, url: str, max_tokens: int = 160, history_turns: int = 3):
        self.url = url
        self.max_tokens = max_tokens
        self.history: list[dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.max_messages = max(2, history_turns * 2 + 1)

    def ask(self, prompt: str) -> str:
        self.history.append({"role": "user", "content": prompt})
        # Keep the system prompt and only the most recent messages.
        self.history = [self.history[0]] + self.history[-(self.max_messages - 1):]
        payload = {
            "model": "local-model",
            "messages": self.history,
            "temperature": 0.7,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data: dict[str, Any] = json.loads(response.read().decode("utf-8"))
            answer = data["choices"][0]["message"]["content"].strip()
            if not answer:
                raise ValueError("The model returned an empty answer.")
        except urllib.error.URLError as exc:
            self.history.pop()
            raise RuntimeError(
                "Could not reach the local model. Is llama-server running at "
                f"{self.url}? Details: {exc}"
            ) from exc
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self.history.pop()
            raise RuntimeError(f"Unexpected response from the local model: {exc}") from exc

        self.history.append({"role": "assistant", "content": answer})
        return answer

    def clear(self) -> None:
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with your local AXLE AI model.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Local llama.cpp chat-completions URL")
    parser.add_argument("--max-tokens", type=int, default=160, help="Maximum reply tokens")
    parser.add_argument("--voice", action="store_true", help="Enable optional Termux voice input/output")
    args = parser.parse_args()

    if args.max_tokens < 1 or args.max_tokens > 512:
        parser.error("--max-tokens must be between 1 and 512 for this low-memory starter")

    voice = args.voice
    axle = Axle(args.url, max_tokens=args.max_tokens)

    print("\nAXLE AI — local assistant")
    print("Type /help for commands, /exit to quit.\n")
    if voice:
        print("Voice mode enabled. Type /voice to switch it off.\n")

    while True:
        try:
            if voice:
                print("Listening...")
                prompt = termux_command("termux-speech-to-text", capture=True)
                if not prompt:
                    print("No speech detected. Try typing instead.")
                    continue
                print(f"You: {prompt}")
            else:
                prompt = input("You: ").strip()

            if not prompt:
                continue
            command = prompt.lower()
            if command in {"/exit", "/quit"}:
                print("AXLE: See you!")
                return 0
            if command == "/help":
                print("Commands: /help, /clear, /voice, /exit")
                continue
            if command == "/clear":
                axle.clear()
                print("AXLE: Conversation cleared.")
                continue
            if command == "/voice":
                voice = not voice
                print(f"AXLE: Voice mode {'on' if voice else 'off'}.")
                continue

            answer = axle.ask(prompt)
            print(f"\nAXLE: {answer}\n")
            if voice:
                try:
                    termux_command("termux-tts-speak", input_text=answer)
                except RuntimeError as exc:
                    print(f"(Speech output unavailable: {exc})")
        except KeyboardInterrupt:
            print("\nAXLE: Stopped.")
            return 0
        except EOFError:
            return 0
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"\nAXLE error: {exc}\n", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
