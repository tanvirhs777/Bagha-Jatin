import os
import discord
import asyncio
import requests
from discord.ext import commands

print("BOT FILE LOADED")

# -------- ENV --------
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("ENV CHECK:",
      bool(TOKEN),
      bool(API_KEY),
      bool(CHANNEL_ID))

if not TOKEN or not API_KEY or not CHANNEL_ID:
    raise RuntimeError("Missing ENV variables")

# -------- INTENTS --------
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# -------- BOT --------
bot = commands.Bot(command_prefix="!", intents=intents)

headers = {
    "X-Auth-Token": API_KEY
}

# -------- EVENTS --------
@bot.event
async def on_ready():
    print(f"LOGGED IN AS {bot.user}")
    bot.loop.create_task(live_loop())

# -------- LIVE LOOP --------
async def live_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNEL_ID))

    if not channel:
        print("❌ CHANNEL NOT FOUND")
        return

    print("✅ CHANNEL FOUND, STARTING LIVE LOOP")

    while not bot.is_closed():
        try:
            r = requests.get(
                "https://api.football-data.org/v4/matches?status=LIVE",
                headers=headers,
                timeout=10
            )
            data = r.json()

            if data.get("matches"):
                m = data["matches"][0]
                msg = (
                    f"⚽ **LIVE MATCH**\n"
                    f"{m['homeTeam']['name']} "
                    f"{m['score']['fullTime']['home']} - "
                    f"{m['score']['fullTime']['away']} "
                    f"{m['awayTeam']['name']}"
                )
                await channel.send(msg)

        except Exception as e:
            print("LOOP ERROR:", e)

        await asyncio.sleep(60)

# -------- RUN --------
print("STARTING BOT...")
bot.run(TOKEN)
