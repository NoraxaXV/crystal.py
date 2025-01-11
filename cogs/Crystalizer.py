import discord
import discord.ext.commands as commands
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import io
import logging

# made with love by Nora Yumiya
class Crystalizer(commands.Cog):

    # Two methods: either ping a user or reply to their message
    @commands.hybrid_command()
    @discord.app_commands.describe(
        liberal="User to crystalize"
    )
#    @commands.has_any_role(ROLE_ID)
    async def crystal(self, ctx: commands.Context, *, liberal: discord.User=None):
        # If we did not ping a specific user, check if we replied to a message
        if liberal == None:
            if ctx.message.reference != None:
                reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                liberal = reply.author
            else:
                logging.error(f'Crystalizer failure for message <{ctx.message.id}>. liberal was "{liberal}" and reply was "{ctx.message.reference}"')
                return

        # await ctx.channel.send('Target aquired, engaging crystalizer...')
        # Fetch avatar bytes
        avatar = await liberal.display_avatar.read()
        # Crystalize the avatar into a bytes file in memory
        with io.BytesIO(self.crystalize(avatar)) as avatarfile:
            await ctx.channel.send(file=discord.File(fp=avatarfile, filename="crystalized_liberal.png"))

    def crystalize(self, avatar_bytes: bytes) -> bytes:
        # Open the file and the bytes
        with Image.open('./crystal.png') as crystal, Image.open(io.BytesIO(avatar_bytes)) as avatar:
            # Crop the avatar into a circle
            avatar = avatar.resize((450,450))
            # avatar.convert("RGBA")
            mask = Image.new('L', avatar.size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
            avatar.putalpha(mask)

            # Create a blank canvas and paste the avatar into position
            # crystal.convert("RGBA")
            canvas = Image.new("RGBA", crystal.size)
            canvas.paste(avatar, (185, 150))

            # Blend the crystal on top of the avatar canvas. The crystal image has hard-set alpha values.
            # NOTE add a multiplication to the alpha values of the crystal to adjust the darkness
            blend = Image.alpha_composite(canvas, crystal)

            # Formats the image as a png and then returns the bytes
            with io.BytesIO() as png:
                blend.save(png, 'PNG')
                png.seek(0)
                return png.read()