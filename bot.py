import os
import discord
import aiohttp
import asyncio
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SOFA_URL = "https://api.sofascore.com/api/v1/sport/football/events/live"

TARGET_TEAMS = ["Real Madrid", "Barcelona"]
posted_events = {}

# -------------------- UTIL --------------------
async def fetch_live():
    async with aiohttp.ClientSession() as session:
        async with session.get(SOFA_URL) as r:
            return await r.json()

def is_target_match(match):
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    return home in TARGET_TEAMS or away in TARGET_TEAMS

# -------------------- SLASH COMMANDS --------------------
@tree.command(name="live", description="Show live matches (RM / Barca)")
async def live(interaction: discord.Interaction):
    data = await fetch_live()
    matches = [m for m in data["events"] if is_target_match(m)]

    if not matches:
        await interaction.response.send_message("❌ এখন কোনো লাইভ ম্যাচ নেই", ephemeral=True)
        return

    msgs = []
    for m in matches:
        msgs.append(
            f"⚽ **LIVE**\n"
            f"{m['homeTeam']['name']} {m['homeScore']['current']} - "
            f"{m['awayScore']['current']} {m['awayTeam']['name']}\n"
            f"⏱ {m['time']['current']}′"
        )

    await interaction.response.send_message("\n\n".join(msgs))

@tree.command(name="laliga", description="La Liga live (RM / Barca)")
async def laliga(interaction: discord.Interaction):
    await live(interaction)

@tree.command(name="epl", description="EPL live")
async def epl(interaction: discord.Interaction):
    await interaction.response.send_message("⚠️ এখন শুধু RM / Barca enabled", ephemeral=True)

@tree.command(name="ucl", description="UCL live (RM / Barca)")
async def ucl(interaction: discord.Interaction):
    await live(interaction)

# -------------------- AUTO GOAL LOOP --------------------
async def goal_watcher():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        try:
            data = await fetch_live()
            for m in data["events"]:
                if not is_target_match(m):
                    continue

                event_id = m["id"]
                score = f"{m['homeScore']['current']}-{m['awayScore']['current']}"

                if posted_events.get(event_id) != score:
                    posted_events[event_id] = score
                    await channel.send(
                        f"🚨 **GOAL UPDATE**\n"
                        f"{m['homeTeam']['name']} {m['homeScore']['current']} - "
                        f"{m['awayScore']['current']} {m['awayTeam']['name']}\n"
                        f"⏱ {m['time']['current']}′"
                    )
        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(30)

# -------------------- READY --------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(goal_watcher())

client.run(TOKEN)
