"""
Discord bot with ChatGPT-style replies via local Ollama (free, local LLM).

Setup:
1) Install deps: pip install -U discord.py requests
2) Создайте бота и возьмите токен: https://discord.com/developers/applications
3) Задайте переменную с токеном:
   PowerShell:  $env:DISCORD_BOT_TOKEN="your_token_here"
   CMD:         set DISCORD_BOT_TOKEN=your_token_here
4) Установите Ollama и модель (пример — llama3):
   - Скачать: https://ollama.com/download
   - Подтянуть модель: ollama pull llama3
   (по умолчанию ожидается сервер на http://127.0.0.1:11434)
   Можно переопределить: OLLAMA_URL, OLLAMA_MODEL.
5) Запуск бота: python discord_bot.py

Команды (префикс "!"):
- !ping                -> Pong
- !roll [max]          -> случайное 1..max (по умолчанию 100)
- !gpt <текст>         -> ответ через локальный Ollama (с краткой историей в канале)
"""

import asyncio
import os
import random
from collections import defaultdict, deque
from typing import Deque, Dict, List, Tuple

import discord
import requests
from discord.ext import commands

Message = Tuple[str, str]  # (role, content)


def make_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    history: Dict[int, Deque[Message]] = defaultdict(lambda: deque(maxlen=10))
    ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user} (id={bot.user.id})")

    @bot.command(name="ping")
    async def ping(ctx: commands.Context) -> None:
        await ctx.reply("Pong!")

    @bot.command(name="roll")
    async def roll(ctx: commands.Context, max_value: int = 100) -> None:
        if max_value < 1:
            await ctx.reply("Max must be >= 1.")
            return
        value = random.randint(1, max_value)
        await ctx.reply(f"🎲 {value} (1-{max_value})")

    @bot.command(name="gpt")
    async def gpt(ctx: commands.Context, *, text: str | None = None) -> None:
        if not text:
            await ctx.reply("Usage: !gpt <message>")
            return

        chan_hist = history[ctx.channel.id]
        chan_hist.append(("user", text))
        prompt = build_prompt(chan_hist)

        try:
            reply_text = await asyncio.to_thread(
                query_ollama, prompt, model=ollama_model, url=ollama_url
            )
        except Exception as exc:  # noqa: BLE001
            await ctx.reply(f"Ошибка запроса к модели: {exc}")
            return

        chan_hist.append(("assistant", reply_text))
        await ctx.reply(reply_text[:1800])

    return bot


def build_prompt(history: Deque[Message]) -> str:
    """Construct a simple conversational prompt."""
    parts: List[str] = [
        "You are a helpful assistant in a Discord chat. Keep answers concise."
    ]
    for role, content in history:
        prefix = "User" if role == "user" else "Assistant"
        parts.append(f"{prefix}: {content}")
    parts.append("Assistant:")
    return "\n".join(parts)


def query_ollama(prompt: str, model: str, url: str) -> str:
    """
    Call local Ollama HTTP API for a completion.
    Requires Ollama running locally with the specified model pulled.
    """
    payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    text = data.get("response") or ""
    return text.strip()


def main() -> None:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("Set DISCORD_BOT_TOKEN environment variable with your bot token.")
    bot = make_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
