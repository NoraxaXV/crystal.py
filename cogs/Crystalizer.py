# Created with love by Nora Yumiya
import discord
import discord.ext.commands as commands
import PIL.Image as Image
import io

# made with love by Nora Yumiya
class Crystalizer(commands.Cog):
    # Two methods: either ping a user or reply to their message
    @commands.hybrid_command()
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
            # Create a bytes file in memory
            with io.BytesIO() as image_binary:
                # Read the avatar bytes, crystalize, and save the image object to the bytes file
                self.crystalize(await liberal.display_avatar.read()).save(image_binary, 'PNG')
                # Move back to the beginning of the file and send it to discord
                image_binary.seek(0)
                await ctx.channel.send(file=discord.File(fp=image_binary, filename="crystalized_liberal.png"))
        except Exception as e:
            print(f'Error sending file: {e}')

    def crystalize(self, avatar_bytes: bytes) -> Image.Image:
        print('Target aquired, engaging crystalizer...')
        # Open the file and the bytes
        with Image.open('./crystal.png') as crystal, Image.open(io.BytesIO(avatar_bytes)) as avatar:
            # Convert each one to RGBA with alpha channel
            crystal.convert("RGBA")
            avatar.convert("RGBA")
            # Create a blank canvas and paste the avatar into position
            canvas = Image.new("RGBA", crystal.size)
            canvas.paste(avatar.resize((400,400)), (200, 200))
            # Blend the crystal on top of the avatar canvas. The crystal image has hard-set alpha values.
            # NOTE add a multiplication to the alpha values of the crystal to adjust the darkness
            return Image.alpha_composite(canvas, crystal)