import disnake
from disnake.ext import commands
import requests
import json
from bot import Bot

from utils.exceptions import NSFWChannel


class Nsfw(commands.Cog):
    """
    NSFW commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    def neko_api(self, ctx, x):
        req = requests.get(f"http://api.nekos.fun:8080/api/{x}")
        if req.status_code != 200:
            print("Could not get a neko")
        if not ctx.channel.is_nsfw():
            raise NSFWChannel("These commands work only in NSFW channels.")
        else:
            embed = disnake.Embed(colour=0x428DFF)
            try:
                embed.set_image(url=json.loads(req.text)["image"])
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
                )
            except KeyError:
                embed.description = "No image found"
            return embed

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="fourk", description="4K", nsfw=True)
    async def fourk(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "4k"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="ass", description="A sexy ass", nsfw=True)
    async def ass(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "ass"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="blowjob", description="For a blowjob", nsfw=True)
    async def blowjob(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "blowjob"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="boobs", description="Boobies", nsfw=True)
    async def boobs(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "boobs"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="cum", description="The baby-gravy", nsfw=True)
    async def cum(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "cum"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="feet", description="bottom view...", nsfw=True)
    async def feet(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "feet"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="hentai", description="Random hentai", nsfw=True)
    async def hentai(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "hentai"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="spank", description="booty spank", nsfw=True)
    async def spank(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "spank"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="gasm", description="Or-Gasm", nsfw=True)
    async def gasm(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "gasm"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="lesbian", description="lesbian fuck", nsfw=True)
    async def lesbian(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "lesbian"), ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(name="pussy", description="Pussy, not a cat", nsfw=True)
    async def pussy(self, ctx: disnake.AppCmdInter):
        await ctx.send(embed=self.neko_api(ctx, "pussy"), ephemeral=True)


def setup(bot):
    bot.add_cog(Nsfw(bot))
