import discord
import discord.ext.commands as commands
import PIL.Image as Image
import dotenv
import asyncio
import io
import os

class Crystalizer(commands.Cog):
    def __init__(self):
        print('Crystalizer Armed!')

    @commands.hybrid_command()
    async def crystal(self, ctx: commands.Context, *, liberal: discord.User=None):
        if liberal == None:
            try:
                liberal = (await ctx.channel.fetch_message(ctx.message.reference.message_id)).author
            except:
                print(f'Crystalization error occured')
                return
        await ctx.channel.send(f'Ready to crystalize {liberal.display_name}!')
        try:
          self.crystalize(await liberal.display_avatar.read(), './crystalized.jpg')
        except Exception as e:
            print(f'Failed to crystalize avatar image: {e}')

    def crystalize(self, avatar_bytes: bytes, outputfp: str):
        print('Target aquired, engaging crystalizer...')
        with Image.open('./crystal-cut.jpg') as image1, Image.open(io.BytesIO(avatar_bytes)) as image2:
            image1.convert("RGBA")
            image2.convert("RGBA")

            image1.putalpha(255)

            image3 = image1.copy()
            image3.putalpha(127)

            width, height = image1.size
            canvas = Image.new("RGBA", (width, height))

            # Paste images onto the canvas
            canvas.paste(image1, (0, 0))
            canvas.paste(image2, (475, 425))
            canvas = Image.blend(canvas, image1, 0.65)

            # Save the final image
            canvas.save(outputfp)
        print('Crystalized 😏')


async def main():
    dotenv.load_dotenv()
    bot = commands.Bot(
        command_prefix='!',
        intents = discord.Intents(
            message_content=True,
            guilds = True,
            guild_messages = True,
        )
    )

    @bot.event
    async def on_ready():
        print(f'Logged in as a bot {bot.user}')

    @bot.command()
    async def ping(ctx):
        await ctx.send('Pong!')

    await bot.add_cog(Crystalizer())
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())