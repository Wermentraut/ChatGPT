import discord
from google import genai

DISCORD_TOKEN = ""
GEMINI_API_KEY = ""

# Настраиваем новый клиент Gemini
client_ai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f"Бот {discord_client.user} запущен!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return
    
    if message.content.startswith("!gem"):
        prompt = message.content[5:]

        try:
            response = client_ai.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            await message.reply(response.text)
        except Exception as e:
            await message.reply(f"Ошибка: {e}")

discord_client.run(DISCORD_TOKEN)
