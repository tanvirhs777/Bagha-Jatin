import os
import discord
import requests
import asyncio

print("BOT FILE LOADED")

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("ENV CHECK:",
      bool(TOKEN),
      bool(API_KEY),
      CHANNEL_ID)

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)

headers = {
    "X-Auth-Token": API_KEY
}

@client.event
async def on_ready():
    print(f"LOGGED IN AS {client.user}")
    asyncio.create_task(live_loop())

async def live_loop():
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))
    print("CHANNEL FOUND:", bool(channel))

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
                    f"⚽ LIVE\n"
                    f"{m['homeTeam']['name']} "
                    f"{m['score']['fullTime']['home']} - "
                    f"{m['score']['fullTime']['away']} "
                    f"{m['awayTeam']['name']}"
                )
                await channel.send(msg)

        except Exception as e:
            print("LOOP ERROR:", e)

        await asyncio.sleep(60)

if __name__ == "__main__":
    print("STARTING BOT...")
    client.run(TOKEN)
