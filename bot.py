import discord
from discord import app_commands
import aiohttp

TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")
    print("✅ Slash commands synced")


@tree.command(name="ping", description="Check bot status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


async def get_matches(keyword: str):
    url = "https://www.scorebat.com/video-api/v3/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.json()
            matches = data.get("response", [])

            result = []
            for m in matches:
                title = m["title"].lower()
                if keyword in title:
                    result.append(m["title"])
            return result


@tree.command(name="live", description="Show live matches")
async def live(interaction: discord.Interaction):
    await interaction.response.defer()
    matches = await get_matches("")
    if not matches:
        await interaction.followup.send("❌ এখন কোনো লাইভ ম্যাচ নাই")
    else:
        await interaction.followup.send("⚽ LIVE MATCHES:\n" + "\n".join(matches[:5]))


@tree.command(name="laliga", description="La Liga matches")
async def laliga(interaction: discord.Interaction):
    await interaction.response.defer()
    matches = await get_matches("real madrid") + await get_matches("barcelona")
    if not matches:
        await interaction.followup.send("❌ La Liga ম্যাচ নাই")
    else:
        await interaction.followup.send("🇪🇸 La Liga:\n" + "\n".join(matches))


@tree.command(name="epl", description="EPL matches")
async def epl(interaction: discord.Interaction):
    await interaction.response.send_message("🏴 EPL command ready (future upgrade)")


@tree.command(name="ucl", description="UCL matches")
async def ucl(interaction: discord.Interaction):
    await interaction.response.send_message("⭐ UCL command ready (future upgrade)")


client.run(TOKEN)
