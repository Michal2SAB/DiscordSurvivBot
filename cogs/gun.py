import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup as soupify

class Gun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.args = 1
    self.name = 'Gun'
    self.url = 'https://survivio.fandom.com/wiki/Weapons'
    self.in_guns = False
    
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Gun Cog Loaded')
  
  @commands.command(aliases=['guns'])
  async def gun(self, ctx):
    args = ctx.message.content.split()
    prefix = '$'
    msg = f'**Argument #1**: Gun Name \n**Example**: `{prefix}gun scar-h`\n**NOTE**: Typing an incorrect gun will result in a list of valid guns.'
    arg_count = len(args) - 1
    if arg_count != self.args:
     await ctx.send(f'**{self.name}** command only takes an argument count of **{self.args}**\n{msg}')
    else:
      gun_name = args[1]
      async with aiohttp.ClientSession() as session:
        async with session.get(self.url) as r:
          try:
            assert r.status == 200
          except:
            ctx.send('Bad Web Request to the surviv.io API.')
          unparsed =  await r.read()
      try:
        b = soupify(unparsed, 'html.parser').find_all('table', {'class': 'article-table'})[1].find_all('tr')
      except:
        await ctx.send("Looks like the bot couldn't find what you were looking for.")
      for i in range(len(b)):
        imAge = b[i].find('img')
        b[i] = b[i].find('a')
      guns = {}
      for i in b:
        if i != None:
            guns[i.text] = i['href']
      gun_dict = guns.copy()
      for b in guns:
        if b == 'M9':
          break
        else:
          del gun_dict[b]
      for i in gun_dict.keys():
        if gun_name.lower() == i.lower():
          act_gun = i
          self.in_guns = True
      if not self.in_guns:
        big_concat = ''
        for i in gun_dict.keys():
          if big_concat == '':
            big_concat += i
          else:
            place = ', ' + i
            big_concat += place
        embed = discord.Embed(description=f'**"{gun_name}"** is not a valid gun in **surviv.io**. \n \n  **Valid Guns**: ' + big_concat, color=0x00b037)
        await ctx.send(embed=embed)
      else:
        async with aiohttp.ClientSession() as session:
          async with session.get('https://survivio.fandom.com/wiki/' + act_gun) as r:
            content = await r.read()
        html = soupify(content, 'html.parser')
        fire_delay = html.find('div', {'data-source': 'fireDelay'}).text
        rel_time = html.find('div', {'data-source': 'reloadTime'}).text
        spread = html.find('div', {'data-source': 'shotSpread'}).text
        damage = html.find('div', {'data-source': 'dmg'}).text
        embed = discord.Embed(title= f"{act_gun}'s Stats", description=f'**Bullet Damage**: {damage} \n **Shot Spread**: {spread} \n **Reload Time**: {rel_time} \n **Firing Delay**: {fire_delay}', color=0x00b037)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Gun(bot))
