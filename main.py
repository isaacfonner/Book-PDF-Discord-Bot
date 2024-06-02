# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import os
from libgen_api import LibgenSearch
import discord
import json
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.tree.sync()
  print('Synced slash commands with Discord')
  await client.change_presence(activity=discord.Activity(
    type=discord.ActivityType.listening, name="/book"))
  print('------')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$book'):
    await message.channel.send("PDF will now be sent. if none get sent, no book was found")
@client.tree.command(name="book", description = "Get a PDF of a certain book")
@app_commands.describe(book="The book title to search")
async def book(i: discord.Interaction, book: str):
   # await i.response.send_message("PDF will now be sent. if none get sent, no book was found")
    s = LibgenSearch()
    results = s.search_title(book)
    item_to_download = results[0]
    download_links = s.resolve_download_links(item_to_download)
    y = json.dumps(download_links)
    where = y.find('"Cloudflare":')
    where2 = y.find('"IPFS.io":')
    burger = len(y) - where2
    embed = discord.Embed(title="Book Found", description=y[where+15:burger*-1])
    await i.response.send_message(embed=embed)
@client.tree.error
async def on_app_command_error(i: discord.Interaction, error):
  if isinstance(error, app_commands.errors.CommandInvokeError):
    embed = discord.Embed(title="Error", description="No book was found for the search term you provided.")
    await i.response.send_message(embed=embed)  
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
