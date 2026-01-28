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

posted_scores = {}

# ---------------- FETCH ----------------
async def fetch_live():
    async with aiohttp.ClientSession() as session:
        async with session.get(SOFA_URL) as r:
            return await r.json()

def is_target(match):
    return (
        match["homeTeam"]["name"] in TARGET_TEAMS or
        match["awayTeam"]["name"] in TARGET_TEAMS
    )

# ---------------- SLASH ----------------
@tree.command(name="live", description="Live RM / Barca match")
async def live(interaction: discord.Interaction):
    data = await fetch_live()
    events = data.get("events", [])

    matches = [m for m in events if is_target(m)]

    if not matches:
        await interaction.response.send_message("❌ এখন কোনো লাইভ ম্যাচ নেই", ephemeral=True)
        return

    msg = []
    for m in matches:
        msg.append(
            f"⚽ **LIVE**\n"
            f"{m['homeTeam']['name']} {m['homeScore']['current']} - "
            f"{m['awayScore']['current']} {m['awayTeam']['name']}\n"
            f"⏱ {m['time']['current']}′"
        )

    await interaction.response.send_message("\n\n".join(msg))

# ---------------- AUTO GOAL ----------------
async def goal_loop():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        try:
            data = await fetch_live()
            events = data.get("events", [])

            for m in events:
                if not is_target(m):
                    continue

                eid = m["id"]
                score = f"{m['homeScore']['current']}-{m['awayScore']['current']}"

                if posted_scores.get(eid) != score:
                    posted_scores[eid] = score
                    await channel.send(
                        f"🚨 **GOAL UPDATE**\n"
                        f"{m['homeTeam']['name']} {m['homeScore']['current']} - "
                        f"{m['awayScore']['current']} {m['awayTeam']['name']}\n"
                        f"⏱ {m['time']['current']}′"
                    )

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(30)

# ---------------- READY ----------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(goal_loop())

client.run(TOKEN)
