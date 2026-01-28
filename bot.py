import discord
import requests
import asyncio

TOKEN = "DUMMY"
API_KEY = "DUMMY"
CHANNEL_ID = 0


intents = discord.Intents.default()
client = discord.Client(intents=intents)

headers = {
    "X-Auth-Token": API_KEY
}

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(live_match_loop())

async def live_match_loop():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    last_msg = ""

    while True:
        try:
            url = "https://api.football-data.org/v4/matches?status=LIVE"
            res = requests.get(url, headers=headers).json()

            if res.get("matches"):
                match = res["matches"][0]

                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]
                score = match["score"]["fullTime"]
                minute = match.get("minute", "LIVE")
                competition = match["competition"]["name"]

                msg = (
                    f"⚽ **LIVE MATCH**\n"
                    f"{home} {score['home']} - {score['away']} {away}\n"
                    f"🏆 {competition}"
                )

                if msg != last_msg:
                    last_msg = msg
                    await channel.send(msg)

        except Exception as e:
            print("❌ Error:", e)

        await asyncio.sleep(60)  # প্রতি 60 সেকেন্ডে চেক

client.run(TOKEN)
