import discord
from discord import app_commands
import asyncio
import aiohttp

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_NAME = "সাধারণ-ব্যক্তির-অসাধারণ-মতামত"  # change if needed

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

tracked_match = None
last_score = None
task_running = False


@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")
    print("✅ Slash commands synced")


@tree.command(name="ping", description="Check bot status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


@tree.command(name="live", description="Check live match (RMA/Barca)")
async def live(interaction: discord.Interaction):
    await interaction.response.send_message("🔍 Checking live matches...")
    start_tracking(interaction.guild)


@tree.command(name="laliga", description="Track La Liga (RMA/Barca)")
async def laliga(interaction: discord.Interaction):
    await interaction.response.send_message("🇪🇸 La Liga tracking started")
    start_tracking(interaction.guild)


@tree.command(name="epl", description="Track EPL (RMA/Barca)")
async def epl(interaction: discord.Interaction):
    await interaction.response.send_message("🏴 EPL tracking started")
    start_tracking(interaction.guild)


@tree.command(name="ucl", description="Track Champions League (RMA/Barca)")
async def ucl(interaction: discord.Interaction):
    await interaction.response.send_message("⭐ UCL tracking started")
    start_tracking(interaction.guild)


def start_tracking(guild):
    global task_running
    if not task_running:
        task_running = True
        asyncio.create_task(match_loop(guild))


async def match_loop(guild):
    global tracked_match, last_score, task_running

    channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
    if not channel:
        task_running = False
        return

    await channel.send("⚽ Match tracker started")

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("https://www.scorebat.com/video-api/v3/") as r:
                    data = await r.json()
                    matches = data.get("response", [])

                    for m in matches:
                        title = m["title"].lower()
                        if "real madrid" in title or "barcelona" in title:
                            score = m["competition"]
                            if score != last_score:
                                last_score = score
                                await channel.send(f"⚽ GOAL UPDATE\n{m['title']}")
                            break

            except Exception as e:
                print("ERROR:", e)

            await asyncio.sleep(45)


client.run(TOKEN)
