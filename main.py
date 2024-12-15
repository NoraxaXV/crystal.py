import discord
from discord.ext import commands

import os

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(
   command_prefix='!',
   intents = discord.Intents.default() | discord.Intents(message_content=True)
)

@bot.event
async def on_ready():
    print(f'Logged in as a bot {bot.user}')

@bot.command()
async def ping(ctx):
   await ctx.send('Pong!')

@bot.command()
async def crystalize(ctx: commands.Context, *, the_doomed: discord.Member=None):
    if the_doomed == None:
        try:
            the_doomed = (await ctx.channel.fetch_message(ctx.message.reference.message_id)).author
        except:
            print(f'Crystalization error occured')
            return
    await ctx.channel.send(f'Ready to crystalize {the_doomed.display_name}!')
    await ctx.channel.send(the_doomed.display_avatar.url)


token = os.getenv('TOKEN')
print(f'Authenticating with token {token}')
bot.run(token)