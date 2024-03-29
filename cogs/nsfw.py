import disnake
from disnake.ext import commands
import requests
import json

from bot import Bot
from utils.exceptions import NSFWChannel
from utils.checks import voter


class Nsfw(commands.Cog):
    """
    NSFW commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    ...


class Nsfw(commands.Cog):
    """
    NSFW commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def neko_api(ctx: disnake.AppCmdInter, x: str):
        """
        Fetches a neko image from the nekos.fun API and creates an embed with the image.

        Args:
            ctx (disnake.AppCmdInter): The context of the command.
            x (str): The type of neko image to fetch.

        Returns:
            disnake.Embed: The embed containing the neko image.
        """
        req = requests.get(f"http://api.nekos.fun:8080/api/{x}")
        if req.status_code != 200:
            print("Could not get a neko")
        if not ctx.channel.is_nsfw():
            raise NSFWChannel("These commands work only in NSFW channels.")
        embed = disnake.Embed(colour=0x428DFF)
        try:
            embed.set_image(url=json.loads(req.text)["image"])
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )
        except KeyError:
            embed.description = "No image found"
        return embed

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-fourk", description="4K", nsfw=True)
    async def fourk(self, ctx: disnake.AppCmdInter):
        """
        Sends a 4k image using the neko API.

        Parameters:
        - ctx: The disnake.AppCmdInter object representing the command context.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "4k"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-ass", description="A sexy ass", nsfw=True)
    async def ass(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of an ass.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "ass"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-blowjob", description="For a blowjob", nsfw=True)
    async def blowjob(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of a blowjob.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "blowjob"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-boobs", description="Boobies", nsfw=True)
    async def boobs(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of boobs.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "boobs"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-cum", description="The baby-gravy", nsfw=True)
    async def cum(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of cum.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "cum"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-feet", description="bottom view...", nsfw=True)
    async def feet(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of feet.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "feet"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-hentai", description="Random hentai", nsfw=True)
    async def hentai(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of an hentai.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "hentai"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-spank", description="booty spank", nsfw=True)
    async def spank(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of a spank.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "spank"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-gasm", description="Or-Gasm", nsfw=True)
    async def gasm(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random orgasmic image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "gasm"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="nsfw-lesbian", description="lesbian fuck", nsfw=True)
    async def lesbian(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of lesbians.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "lesbian"), ephemeral=True)

    @voter()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(
        name="nsfw-pussy", description="Pussy, not a cat", nsfw=True
    )
    async def pussy(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random image of a pussy.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.send(embed=self.neko_api(ctx, "pussy"), ephemeral=True)


def setup(bot):
    bot.add_cog(Nsfw(bot))
