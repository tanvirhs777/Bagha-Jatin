import os
import discord
from discord.ext import commands

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True

# ===== BOT =====
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== READY =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# ===== COMMAND =====
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ===== RUN =====
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN not found in environment variables")

bot.run(TOKEN)
