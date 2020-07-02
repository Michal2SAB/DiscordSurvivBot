import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup as soupify

class Player(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.url = 'https://surviv.io/api/user_stats'
    self.headers = {'content-type': 'application/json; charset=UTF-8'}
    self.name = 'Player'
    self.msg = "**Argument #1**: Player Name \n**Example**: `s!player obsidian_mb`\n**NOTE**: You must put in the **user's account name** which might differ with their in game name."
    self.args = 1

  @commands.Cog.listener()
  async def on_ready(self):
    print('Player Cog Loaded')
  
  @commands.command(aliases=['players', 'user', 'users'])
  async def stats(self, ctx):
    args = ctx.message.content.split()
    arg_count = len(args) - 1
    msg = f"**Argument #1**: Player Name \n**Example**: `{prefix}player obsidian_mb`\n**NOTE**: You must put in the **user's account name** which might differ with their in game name."
    if arg_count != self.args:
     await ctx.send(f'**{self.name}** command only takes an argument count of **{self.args}**\n{msg}')
    else:
      player_name = args[1]
      b = player_name.lower()
      data = {"slug":f"{b}","interval":"all","mapIdFilter":"-1"}
      try:
        async with aiohttp.ClientSession() as session:
          async with session.post(self.url, headers=self.headers, json=data) as r:
            c = await r.json()
      except:
        await ctx.send('Connection Error.')
      if c == None:
        embed = discord.Embed(description=f'**{player_name}** is not a valid player of surviv.io', color=0x00b037)
        await ctx.send(embed=embed)
      else:
        c = await r.json()
        kills =  str(c['kills'])
        wins = str(c['wins'])
        games = str(c['games'])
        kg = str(c['kpg'])
        print(c)
        mostkills = str(max([i['mostKills'] for i in c['modes']]))
        maxdamage = str(max([i['mostDamage'] for i in c['modes']]))
        # max_kills
        embed = discord.Embed(title = f"**{c['username']}'s Stats**", description=f'**Wins**: {wins} \n **Kills**: {kills} \n **Games**: {games} \n **Kill Per Game Avg**: {kg} \n **Max Kills**: {mostkills} \n **Most Damage**: {maxdamage}', color=0x00b037)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Player(bot))
