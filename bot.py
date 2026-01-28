import os
import discord
import requests
import asyncio
from discord.ext import commands

print("BOT FILE LOADED")

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("ENV CHECK:", bool(TOKEN), bool(API_KEY), CHANNEL_ID)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

headers = {
    "X-Auth-Token": API_KEY
}

@bot.event
async def on_ready():
    print(f"✅ LOGGED IN AS {bot.user}")
    bot.loop.create_task(live_loop())

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

async def live_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNEL_ID))
    print("CHANNEL FOUND:", bool(channel))

    last_msg = None

    while True:
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

                if msg != last_msg:
                    await channel.send(msg)
                    last_msg = msg

        except Exception as e:
            print("LOOP ERROR:", e)

        await asyncio.sleep(60)

bot.run(TOKEN)
