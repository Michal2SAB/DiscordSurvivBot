import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import *
import aiohttp
from bs4 import BeautifulSoup as soupify
import aiosqlite
import os

Client = discord.Client()
bot_prefix= "$"
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
  activity = discord.Game(name="Mind Yo Business.")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Mind Yo Business.'))
  print("Name: {}".format(client.user.name))
  print("ID: {}".format(client.user.id))
  print('Servers connected to:')
  for server in client.guilds:
    print(server.name + " = " + str(server.id))

exceptioN = []
# Loading cogs
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
      if file not in exceptioN:
        bot.load_extension(f'cogs.{file[:-3]}')

    
bot.run(os.environ['bot_token'])
