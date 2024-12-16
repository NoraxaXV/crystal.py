import discord
import discord.ext.commands as commands
import dotenv
import asyncio
import os

import cogs.Crystalizer as Crystalizer

async def main():
    dotenv.load_dotenv()

    bot = commands.Bot(
        command_prefix='!',
        intents = discord.Intents(
            message_content=True,
            guilds = True,
            guild_messages = True,
        ),
    )

    @bot.event
    async def on_ready():
        print(f'Logged in as a bot {bot.user}')

    @bot.command()
    async def ping(ctx):
        await ctx.send('Pong!')
    discord.utils.setup_logging()
    await bot.add_cog(Crystalizer.Crystalizer())
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())