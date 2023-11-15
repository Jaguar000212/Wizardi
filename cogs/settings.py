import disnake
from disnake.ext import commands
import datetime as dt
from bot import Bot
from disnake.ext.commands.params import Param


class Settings(commands.Cog):
    """
    Bot configurations (Must see)
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        
    @commands.slash_command(description="Check Bot's latency")
    async def ping(self, ctx: disnake.AppCmdInter):
        await ctx.response.defer()
        embed = disnake.Embed(
            title="Pong!",
            description=f"{self.bot.icons['stats']} Current Latency - **{round (self.bot.latency * 1000)}ms**",
            color=65389,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Settings(bot))
