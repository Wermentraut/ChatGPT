import os
import discord
import google.generativeai as genai

# ================= НАСТРОЙКИ =================

DISCORD_TOKEN = "MTQ0Mjg3OTk0MzA5OTk0NTA5MQ.GtDlgW.kEVKqN8pzsTSTxqiIJOGHOgIDJhPurr7dRXnPk"
GEMINI_API_KEY = "AIzaSyB4uQQ36W3BF0PgR5jhCqR2Xj7D_DzPogs"

MODEL_NAME = "gemini-1.5-flash-latest"


# =============================================

genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

# История сообщений для каждого пользователя
user_history = {}
user_personas = {}

DEFAULT_SYSTEM_PROMPT = "Ты дружелюбный и полезный ассистент."
MAX_HISTORY = 10


# ================== ФУНКЦИИ ==================

def build_prompt(history):
    """
    Конвертация истории сообщений в один текстовый prompt.
    Gemini принимает обычный текст, а не список {"role": "..."}.
    """
    final = ""
    for msg in history:
        if msg["role"] == "system":
            final += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            final += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            final += f"Assistant: {msg['content']}\n"
    final += "Assistant:"
    return final


# ================== ЛОГИКА БОТА ==================

@discord_client.event
async def on_ready():
    print(f"Бот {discord_client.user} запущен!")


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    user_id = str(message.author.id)
    content = message.content.strip()

    # ---------- HELP ----------
    if content.startswith("!help"):
        await message.reply(
            "**Команды:**\n"
            "`!ai текст` — спросить ИИ\n"
            "`!persona текст` — задать стиль\n"
            "`!reset` — сбросить историю\n"
            "`!help` — помощь"
        )
        return

    # ---------- RESET ----------
    if content.startswith("!reset"):
        user_history.pop(user_id, None)
        user_personas.pop(user_id, None)
        await message.reply("🔄 История и личность сброшены.")
        return

    # ---------- PERSONA ----------
    if content.startswith("!persona"):
        new_persona = content[len("!persona"):].strip()

        if not new_persona:
            await message.reply("❗ Использование: `!persona текст личности`")
            return

        user_personas[user_id] = new_persona
        await message.reply(f"Личность обновлена: **{new_persona}**")
        return

    # ---------- AI ----------
    if not content.startswith("!ai"):
        return

    prompt = content[3:].strip()
    if not prompt:
        await message.reply("❗ Напиши: `!ai текст`")
        return

    # Создаём историю если нет
    if user_id not in user_history:
        persona = user_personas.get(user_id, DEFAULT_SYSTEM_PROMPT)
        user_history[user_id] = [
            {"role": "system", "content": persona}
        ]

    # Добавляем новое сообщение
    user_history[user_id].append({"role": "user", "content": prompt})

    # Ограничиваем историю
    if len(user_history[user_id]) > MAX_HISTORY:
        user_history[user_id] = user_history[user_id][-MAX_HISTORY:]

    # ---------- GENERATION ----------
    try:
        full_prompt = build_prompt(user_history[user_id])

        model = genai.GenerativeModel("gemini-1.5-flash-latest")


        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=512
            )
        )

        answer = response.text

        # Добавляем ответ в историю
        user_history[user_id].append({"role": "assistant", "content": answer})

    except Exception as e:
        print("🔥 ERROR:", e)
        answer = "⚠️ Ошибка модели Gemini."

    if len(answer) > 1900:
        answer = answer[:1900] + "…"

    await message.reply(answer)


# Запуск
discord_client.run(DISCORD_TOKEN)
