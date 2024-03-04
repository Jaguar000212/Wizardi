import disnake
from disnake.ext import commands

from bot import Bot


class Settings(commands.Cog):
    """Bot configurations (Must see)"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(description="Check Bot's latency")
    async def ping(self, ctx: disnake.AppCmdInter):
        """
        A command to check the latency of the bot.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.response.defer()

        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = "Pong!"
        embed.description = f"{self.bot.icons['stats']} Current Latency - **{round (self.bot.latency * 1000)}ms**"
        embed.color = 65389

        await ctx.send(embed=embed)

    @commands.slash_command(description="Get the voting link for the bot")
    async def vote(self, ctx: disnake.AppCmdInter):
        """
        A command to get the voting link for the bot.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.response.defer()
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = "Vote for me!"
        embed.description = f"The bot supports many useful features but are for premium users only!\nVote now to become one of them...\n[Discord Bot List](https://discordbotlist.com/bots/wizardi)"
        embed.color = 65389

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Settings(bot))
