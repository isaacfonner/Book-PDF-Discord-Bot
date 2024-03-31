# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import os
from libgen_api import LibgenSearch
import discord
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$book'):
    await message.channel.send("PDF will now be sent. if none get sent, no book was found")

  if message.content.startswith('$book'):
    s = LibgenSearch()
    results = s.search_title(message.content)
    print(results)
    item_to_download = results[0]
    download_links = s.resolve_download_links(item_to_download)
    y = json.dumps(download_links)
    where = y.find('"Cloudflare":')
    where2 = y.find('"IPFS.io":')
    burger = len(y) - where2
    await message.channel.send(y[where+15:burger*-1])

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
