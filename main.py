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
    pass

token = os.getenv('TOKEN')
print(f'Authenticating with token {token}')
bot.run(token)