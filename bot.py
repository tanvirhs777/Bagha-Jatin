import os
import discord
from discord.ext import commands

print("BOT STARTING...")

TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN FOUND:", bool(TOKEN))

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("================================")
    print(f"LOGGED IN AS {bot.user}")
    print("BOT IS ONLINE ✅")
    print("================================")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Bot is alive.")

if not TOKEN:
    print("❌ TOKEN MISSING")
    exit(1)

bot.run(TOKEN)
