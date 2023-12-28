import disnake
from disnake.ext.commands.params import Param
from disnake.ext import commands
import requests
import json
import time
import asyncio
import akinator as ak
from itertools import repeat
from random import *

from utils.fun_helper import RPS, TicTacToe, MineswiperView
from bot import Bot


class Fun(commands.Cog):
    """
    Some Fun Commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(description="A fun hack command")
    async def hack(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="Member to be hacked"),
    ):
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
    @commands.slash_command(description="Roll the slot machine")
    async def slot(self, ctx: disnake.AppCmdInter):
        await ctx.response.defer()
        embed = disnake.Embed()
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒🍈🍌🍍🥭🍏🍑🥝🥑"
        a, b, c = [choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n\n{ctx.author.name}**,"

        if a == b == c:
            embed.description = f"{slotmachine} All matching, you won! 🎉"
            embed.colour = disnake.Colour.green()
        elif (a == b) or (a == c) or (b == c):
            embed.description = f"{slotmachine} 2 in a row, you won! 🎉"
            embed.colour = disnake.Colour.yellow()
        else:
            embed.description = f"{slotmachine} No match, you lost 😢"
            embed.colour = disnake.Colour.red()

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(description="Give someone a beer! 🍻")
    async def beer(
        self,
        ctx: disnake.AppCmdInter,
        user: disnake.Member = Param(None, description="Member to celebrate with"),
        *,
        reason=Param(None, description="Reasone for celeb"),
    ):
        await ctx.response.defer()
        if not user or user.id == ctx.author.id:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"**{ctx.author.name}**: paaaarty!🎉🍺",
                    color=disnake.Colour.magenta(),
                )
            )
        if user.id == self.bot.user.id:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"*drinks beer with you* 🍻",
                    color=disnake.Colour.magenta(),
                )
            )
        if user.bot:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/",
                    color=disnake.Colour.magenta(),
                )
            )

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
        await ctx.send(
            embed=disnake.Embed(description=beer_offer, color=disnake.Colour.magenta())
        )

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            msg = await ctx.original_message()
            await msg.add_reaction("🍻")
            await self.bot.wait_for(
                "raw_reaction_add", timeout=30.0, check=reaction_check
            )
            await ctx.edit_original_message(
                embed=disnake.Embed(
                    description=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻",
                    color=disnake.Colour.magenta(),
                )
            )
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(
                embed=disnake.Embed(
                    description=f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;",
                    color=disnake.Colour.magenta(),
                )
            )
        except disnake.Forbidden:
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = (
                f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
            )
            await ctx.edit_original_message(
                embed=disnake.Embed(
                    description=beer_offer, color=disnake.Colour.magenta()
                )
            )

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(description="Get an embeded gun on your avatar")
    async def gun(
        self,
        ctx: disnake.AppCmdInter,
        user: disnake.Member = Param(
            None, description="Member whose avatar is to be embedded"
        ),
    ):
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
        description="Translate your text into funny Lul Cat Language!"
    )
    async def kitty(
        self, ctx: disnake.AppCmdInter, text=Param(description="Text to covert")
    ):
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
        await ctx.response.defer()
        intro = disnake.Embed(
            title="Akinator",
            description=f"Hello, {ctx.author.mention} I am Akinator!!!\nThink about a real or fictional character. I will try to guess who it is",
            color=disnake.Colour.blue(),
        )
        intro.set_thumbnail(
            url="https://en.akinator.com/bundles/elokencesite/images/akinator.png?v93"
        )
        intro.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        intro.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        bye = disnake.Embed(
            title="Akinator",
            description=f"\👋 B-Bye, {ctx.author.mention}\n\n*Akinator left the chat!!*",
            color=disnake.Colour.blue(),
        )
        bye.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        bye.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        bye.set_thumbnail(
            url="https://i.pinimg.com/originals/28/fc/0b/28fc0b88d8ded3bb8f89cb23b3e9aa7b.png"
        )
        await ctx.send(embed=intro)

        ans_emoji = {"👍🏻": "yes", "👎🏻": "no", "🤔": "probably", "🤷🏻": "idk", "🔙": "back"}

        aki = ak.Akinator()
        q = aki.start_game()
        n = 0
        while aki.progression <= 80:
            n = n + 1
            question = disnake.Embed(
                title=f"Question {n}",
                description=f"{q}\n\nAnswer:\n\n> `Yes(👍🏻)` | `No(👎🏻)`\n> `Probably(🤔)` | `Don't know(🤷🏻)`\n> `Back(🔙)`",
                color=disnake.Colour.blue(),
            )
            ques = [
                "https://i.imgflip.com/uojn8.jpg",
                "https://ih1.redbubble.net/image.297680471.0027/flat,750x1000,075,f.u1.jpg",
            ]
            question.set_thumbnail(url=ques[randint(0, 1)])
            question.set_author(
                name=self.bot.user.display_name,
                icon_url=f"{self.bot.user.avatar.url}",
            )
            question.set_footer(
                text=f"for {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            ques = await ctx.channel.send(embed=question)

            await ques.add_reaction("👍🏻")
            await ques.add_reaction("👎🏻")
            await ques.add_reaction("🤔")
            await ques.add_reaction("🤷🏻")
            await ques.add_reaction("🔙")

            def check(react: disnake.Reaction, user: disnake.User):
                if (
                    user == ctx.author
                    and react.message.id == ques.id
                    and (react.emoji in ["👍🏻", "👎🏻", "🤔", "🤷🏻", "🔙"])
                ):
                    return True
                return False

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=30
                )
            except asyncio.TimeoutError:
                await ctx.send("Sorry you took too long to respond!")
                await ctx.send(embed=bye)
                return
            if str(reaction.emoji) == "🔙":
                try:
                    q = aki.back()
                except ak.CantGoBackAnyFurther as e:
                    await ctx.send(e)
                    continue
            elif str(reaction.emoji) in ans_emoji.keys():
                try:
                    q = aki.answer(ans_emoji[str(reaction.emoji)])
                except ak.InvalidAnswerError as e:
                    await ctx.send(e)
                    continue
        aki.win()
        answer = disnake.Embed(
            title=aki.first_guess["name"],
            description=f"{aki.first_guess['description']}\nRanking - {aki.first_guess['ranking']}",
            color=disnake.Colour.blue(),
        )
        answer.set_image(url=aki.first_guess["absolute_picture_path"])
        answer.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        answer.set_footer(
            text=f"Was I correct? {ctx.author.display_name} (👍🏻/👎🏻)",
            icon_url=ctx.author.display_avatar.url,
        )
        ans_msg = await ctx.channel.send(embed=answer)
        await ans_msg.add_reaction("👍🏻")
        await ans_msg.add_reaction("👎🏻")

        def check(react: disnake.Reaction, user: disnake.User):
            if (
                user == ctx.author
                and react.message.id == ans_msg.id
                and (react.emoji in ["👍🏻", "👎🏻"])
            ):
                return True
            return False

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=check, timeout=30
            )
        except asyncio.TimeoutError:
            await ctx.send(
                embed=disnake.Embed(description="You took too long to respond!")
            )
            await ctx.send(embed=bye)
            return
        if ans_emoji[str(reaction.emoji)] == "yes":
            yes = disnake.Embed(
                title="Akinator",
                description="I did this again...\🫣",
                color=disnake.Colour.blue(),
            )
            yes.set_thumbnail(
                url="https://i.pinimg.com/originals/ae/aa/d7/aeaad720bd3c42b095c9a6788ac2df9a.png"
            )
            yes.set_author(
                name=self.bot.user.display_name,
                icon_url=f"{self.bot.user.avatar.url}",
            )
            yes.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            await ctx.channel.send(embed=yes)
        elif ans_emoji[str(reaction.emoji)] == "no":
            no = disnake.Embed(
                title="Akinator",
                description="Oops! I just missed \😢",
                color=disnake.Colour.blue(),
            )
            no.set_thumbnail(
                url="https://i.pinimg.com/originals/0a/8c/12/0a8c1218eeaadf5cfe90140e32558e64.png"
            )
            no.set_author(
                name=self.bot.user.display_name,
                icon_url=f"{self.bot.user.avatar.url}",
            )
            no.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            await ctx.channel.send(embed=no)
        await ctx.send(embed=bye)

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
