import discord
import discord.ext.commands as commands
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import io

# made with love by Nora Yumiya
class Crystalizer(commands.Cog):
    # Two methods: either ping a user or reply to their message
    @commands.command(name="crystal")
    async def crystal(self, ctx: commands.Context, *, liberal: discord.User=None):
        # If we did not ping a specific user, check if we replied to a message
        if liberal == None:
            try:
                liberal = (await ctx.channel.fetch_message(ctx.message.reference.message_id)).author
            except Exception as e:
                # No reply or ping was found
                print(f'Crystalization error occured: {e}')
                return
        try:
            await ctx.channel.send('Target aquired, engaging crystalizer...')
            await ctx.channel.send(file=discord.File(fp=self.crystalize(await liberal.display_avatar.read()), filename="crystalized_liberal.png"))
        except Exception as e:
            print(f'Error sending file: {e}')

    def crystalize(self, avatar_bytes: bytes) -> Image.Image:
        # NOTE add a multiplication to the alpha values of the crystal to adjust the darkness
        # Open the file and the bytes
        with Image.open('./crystal.png') as crystal, Image.open(io.BytesIO(avatar_bytes)) as avatar:
            # Crop the avatar into a circle
            avatar = avatar.resize((450,450))
            avatar.convert("RGBA")
            mask = Image.new('L', avatar.size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
            avatar.putalpha(mask)

            # Create a blank canvas and paste the avatar into position
            crystal.convert("RGBA")
            canvas = Image.new("RGBA", crystal.size)
            canvas.paste(avatar, (185, 150))

            # Create a bytes file in memory
            with io.BytesIO() as result_binary:
                # Blend the crystal on top of the avatar canvas. The crystal image has pre-set alpha values.
                Image.alpha_composite(canvas, crystal).save(result_binary, 'PNG')
                result_binary.seek(0)
                return result_binary