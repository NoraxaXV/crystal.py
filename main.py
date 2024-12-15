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
        application_id = os.getenv('APPLICATION_ID'),
    )

    @bot.event
    async def on_ready():
        guild = discord.Object(id=os.getenv('MY_GUILD_ID'))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)

        print(f'Logged in as a bot {bot.user}')

    @bot.command()
    async def ping(ctx):
        await ctx.send('Pong!')

    await bot.add_cog(Crystalizer.Crystalizer())
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())