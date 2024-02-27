import disnake
from disnake.ext.commands.params import Param
from disnake.ext import commands
import requests
import json
import time
from itertools import repeat
from random import randint

from utils.funHelpers import *
from bot import Bot


class Fun(commands.Cog):
    """Some Fun Commands"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(name="fun-hack", description="A fun hack command")
    async def hack(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="Member to be hacked"),
    ):
        """
        Hacks the specified member by simulating a hacking process.

        Parameters:
        - ctx: The context of the command.
        - member: The member to be hacked.

        Returns:
        None
        """
        await ctx.response.defer()
        embed = disnake.Embed(
            description="Initialising injection", color=disnake.Colour.dark_teal()
        )
        await ctx.send(embed=embed)
        hacking = [
            "**[0%]** Bypassing 2FA...",
            "**[5%]** 2FA BYPASSED! Finding discord login...",
            "**[15%]** LOGIN FOUND! Finding IP...",
            "**[30%]** IP FOUND! Looking for email and password...",
            f"**[50%]** DONE! Email: `{(member.display_name).replace(' ', '')}@chummiwala.com` | Password: `XuIsjgi9cg`",
            "**[75%]** Injecting trojan virus...",
            f"**[100%]** Successfully hacked {member.mention}",
        ]
        for hack in hacking:
            time.sleep(3)
            embed.description = hack
            await ctx.edit_original_message(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(name="fun-slot", description="Roll the slot machine")
    async def slot(self, ctx: disnake.AppCmdInter):
        """
        Play a slot machine game.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        None
        """
        await ctx.response.defer()
        embed = slotGame(ctx)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(name="fun-beer", description="Give someone a beer! 🍻")
    async def beer(
        self,
        ctx: disnake.AppCmdInter,
        user: disnake.Member = Param(None, description="Member to celebrate with"),
        reason: str = Param(None, description="Reason for celebration"),
    ):
        """
        Sends a beer offer to a member and waits for their reaction.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - user (disnake.Member, optional): The member to celebrate with. Defaults to None.
        - reason (str, optional): The reason for the celebration. Defaults to None.
        """

        await ctx.response.defer()
        await beerOffer(self.bot, user, ctx, reason)

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(
        name="fun-gun", description="Get an embeded gun on your avatar"
    )
    async def gun(
        self,
        ctx: disnake.AppCmdInter,
        user: disnake.Member = Param(
            None, description="Member whose avatar is to be embedded"
        ),
    ):
        """
        Sends an embedded message with a gun image using the avatar of the specified member.

        Parameters:
        - ctx: The context of the command.
        - user: The member whose avatar is to be embedded. If not provided, the author of the command will be used.
        """

        await ctx.response.defer()
        if user is None:
            user = ctx.author
        embed = disnake.Embed(color=53759)
        try:
            embed.set_image(url=f"https://api.popcat.xyz/gun?image={user.avatar.url}")
        except AttributeError:
            embed.set_image(
                url=f"https://api.popcat.xyz/gun?image={user.default_avatar.url}"
            )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(2, 15, commands.BucketType.user)
    @commands.slash_command(
        name="fun-kitty", description="Translate your text into funny Lul Cat Language!"
    )
    async def kitty(
        self, ctx: disnake.AppCmdInter, text: str = Param(description="Text to covert")
    ):
        """
        Sends a kitty image with the specified text.

        Parameters:
        - ctx: The context of the command.
        - text: The text to be displayed on the kitty image.

        Returns:
        None
        """
        await ctx.response.defer()
        req = requests.get(f"https://api.popcat.xyz/lulcat?text={text}")
        data = (json.loads(req.text))["text"]
        await ctx.send(data)

    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(
        name="game-akinator", description="Simply akinator, you think it, we guess it"
    )
    async def akinator(self, ctx: disnake.AppCmdInter):
        """
        Starts an Akinator game.

        Parameters:
        - ctx: The context of the command.

        Returns:
        None
        """
        await ctx.response.defer()
        await AkinatorGame(self.bot, ctx)

    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.slash_command(
        name="game-ttt", description="Starts a tic-tac-toe game with yourself."
    )
    async def tic(
        self,
        ctx: disnake.AppCmdInter,
        player: disnake.Member = Param(description="Member to play with"),
    ):
        """
        Play a game of Tic-Tac-Toe with another member.

        Parameters:
        - ctx: The context of the command.
        - player: The member to play with.

        Returns:
        None
        """
        await ctx.response.defer()
        if player.bot:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['failed']} Bots can't play with you!!"
                ),
                ephemeral=True,
            )
            return
        if ctx.author == player:
            await ctx.send(
                embed=disnake.Embed(
                    description="Playing with yourself??? Drilling I guess..."
                ),
                ephemeral=True,
            )
        embed = self.bot.Embed(self.bot, ctx, "Challenged")
        embed.title = "Tic-Tac-Toe"
        embed.description = f"`Challenger` - {ctx.author.mention} ({self.bot.icons['online']})\n`Opponent` - {player.mention} ({self.bot.icons['error']})\n\n```diff\n- Current Turn - {player}```"
        await ctx.send(embed=embed, view=TicTacToe(player, ctx.author))

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="game-rps", description="Starts a rock-paper-scissors game with the bot."
    )
    async def rps(
        self,
        ctx=Param(),
        player: disnake.Member = Param(None, description="Member to play with"),
    ):
        """
        Play a game of Rock-Paper-Scissors with another member.

        Parameters:
        - ctx: The context of the command invocation.
        - player: The member to play with. If not provided, the bot will play against the command invoker.

        Returns:
        None
        """
        await ctx.response.defer()
        if player is None:
            player = self.bot.user
        if player.bot:
            if not player == self.bot.user:
                await ctx.send(
                    embed=disnake.Embed(description="Bots can't play with you!!"),
                    ephemeral=True,
                )
                return
            await ctx.send(
                embed=disnake.Embed(description="A challenge to me... Accepted"),
                ephemeral=True,
            )
        if ctx.author == player:
            await ctx.send(
                embed=disnake.Embed(description="You need someone else to play with!"),
                ephemeral=True,
            )
            return
        embed = self.bot.Embed(self.bot, ctx, "Challenged")
        embed.title = "Rock-Paper-Scissors"
        embed.description = (
            f"`Challenger` - {ctx.author.mention}\n`Opponent` - {player.mention}"
        )
        await ctx.send(embed=embed, view=RPS(self.bot, ctx.author, player))

    @commands.slash_command(
        name="game-minesweeper", description="Play minesweeper mini-game."
    )
    async def mine(self, ctx):
        """
        Play a minesweeper mini-game.

        Parameters:
        - ctx: The context of the command.

        Returns:
        None
        """
        board = [["\u200b"] * 5] * 5  # 5x5 buttoned rows
        bombs = 0
        bombpositions = []
        for x in repeat(None, randint(4, 11)):
            random_index = randint(0, 19)
            if random_index not in bombpositions and random_index not in [
                0,
                4,
                20,
                24,
            ]:
                bombpositions.append(random_index)
                bombs += 1

        def ExtractBlocks():
            new_b = []
            for x in board:
                for y in x:
                    new_b.append(y)
            return new_b

        await ctx.send(
            f"Total Bombs: `{len(bombpositions)}`",
            view=MineswiperView(ctx, ExtractBlocks(), bombpositions, board),
        )


def setup(bot):
    bot.add_cog(Fun(bot))
