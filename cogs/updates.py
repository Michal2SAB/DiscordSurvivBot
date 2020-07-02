import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup as soupify

class Update(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.name = 'Update'
    self.args = 0
    self.url = 'http://surviv.io/'
    self.msg = '**Example**: `s$update`'
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Update Cog Loaded')

  @commands.command(aliases=['releases', 'release', 'update', 'new', 'news'])
  async def updates(self, ctx):
    prefix = '$'
    msg = f'**Example**: `{prefix}updates`'
    args = ctx.message.content.split()
    arg_count = len(args) - 1
    if arg_count != self.args:
      await ctx.send(f'**{self.name}** command only takes an argument count of **{self.args}** \n{msg}')
    else:
      try:
        async with aiohttp.ClientSession() as session:
          async with session.get(self.url) as r:
            raw = await r.read()
      except:
        ctx.send('Failed to connect to surviv.io website.')
      html = soupify(raw, 'html.parser')
      news_wrapper = html.find('div', {'id':'news-current'})
      tags = news_wrapper.find_all('p', {'class': 'news-paragraph'})
      tags2 = news_wrapper.find('small').text
      tags3 = []
      for i in tags:
        tags3.append(i.text)
     #if len(tags3[0]) > 30:
      #description = tags3[0]
      #title = f'⏫({tags2})⏫'
      #else:
      title = f'⏫ "{tags3[0]}" ({tags2}) ⏫'
      del tags3[0]
      description = ' \n \n '.join(tags3) 
      desc = f'{description}'
      print(desc)
      embed = discord.Embed(title=title, description=desc, color=0x00b037)
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Update(bot))
