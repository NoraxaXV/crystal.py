import discord
import discord.ext.commands as commands
import PIL.Image as Image
import PIL
import io

class Crystalizer(commands.Cog):
    def __init__(self):
        print('Crystalizer Armed!')

    @commands.command()
    async def crystal(self, ctx: commands.Context, *, liberal: discord.User=None):
        if liberal == None:
            try:
                liberal = (await ctx.channel.fetch_message(ctx.message.reference.message_id)).author
            except Exception as e:
                print(f'Crystalization error occured: {e}')
                return
        await ctx.channel.send(f'Ready to crystalize {liberal.display_name}!')
        try:
            with io.BytesIO() as image_binary:
                self.crystalize(await liberal.display_avatar.read()).save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.channel.send(file=discord.File(fp=image_binary, filename="crystalized_liberal.png"))
        except Exception as e:
            print(f'Error sending file: {e}')

        print('Crystalized!')


    def crystalize(self, avatar_bytes: bytes) -> Image.Image:
        print('Target aquired, engaging crystalizer...')
        with Image.open('./crystal.png') as crystal, Image.open(io.BytesIO(avatar_bytes)) as avatar:
            crystal.convert("RGBA")
            avatar.convert("RGBA")
            canvas = Image.new("RGBA", crystal.size)
            canvas.paste(avatar.resize((400,400)), (200, 200))
            return Image.alpha_composite(canvas, crystal)