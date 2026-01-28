import os
import discord
import requests
from discord.ext import commands

print("BOT FILE LOADED")

# ENV
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")

print("ENV CHECK:", bool(TOKEN), bool(API_KEY))

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

# BOT
bot = commands.Bot(command_prefix="!", intents=intents)

HEADERS = {
    "X-Auth-Token": API_KEY
}

# READY
@bot.event
async def on_ready():
    print(f"✅ LOGGED IN AS {bot.user}")

# PING
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# LIVE MATCH COMMAND
@bot.command()
async def live(ctx):
    try:
        r = requests.get(
            "https://api.football-data.org/v4/matches?status=LIVE",
            headers=HEADERS,
            timeout=10
        )
        data = r.json()

        if not data.get("matches"):
            await ctx.send("❌ এখন কোনো লাইভ ম্যাচ নেই")
            return

        msgs = []
        for m in data["matches"][:5]:  # max 5 match
            msgs.append(
                f"⚽ **LIVE**\n"
                f"{m['homeTeam']['name']} "
                f"{m['score']['fullTime']['home']} - "
                f"{m['score']['fullTime']['away']} "
                f"{m['awayTeam']['name']}"
            )

        await ctx.send("\n\n".join(msgs))

    except Exception as e:
        print("LIVE CMD ERROR:", e)
        await ctx.send("⚠️ API error, পরে আবার try করো")

# RUN
bot.run(TOKEN)
