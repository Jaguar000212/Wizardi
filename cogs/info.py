import disnake
from disnake.ext import commands
from disnake.ext.commands.params import Param
import requests
import json

from utils.information import *
from utils.checks import voter
from bot import Bot


class Info(commands.Cog):
    """
    Get some useful information from the Internet
    """

    def __init__(self, bot: Bot):
        """
        Initialize the Info cog.

        Parameters:
        - bot (Bot): The instance of the Bot class.

        Returns:
        None
        """
        self.bot = bot

    @voter()
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="info-character",
        description="Find info about your favourite character",
    )
    async def character(
        self, ctx: disnake.AppCmdInter, name=Param(description="Name of the character")
    ):
        """
        Get information about a character.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - name (str): The name of the character.

        Returns:
        None
        """
        await ctx.response.defer()
        req = requests.get(
            f"https://superheroapi.com/api/{self.bot.config.api_keys['superhero_api']}/search/{name}",
            verify=False,
        )
        data = json.loads(req.text)
        if data["response"] == "success":
            embed = SuperheroInformation(data, ctx)
            await ctx.send(embed=embed)

        else:
            embed = disnake.Embed(
                description=f"{self.bot.icons['failed']} No such character found.",
                colour=1199267,
            )
            await ctx.send(embed=embed, delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="info-user", description="Get details of a server member"
    )
    async def user(
        self,
        ctx: disnake.AppCmdInter,
        user: disnake.Member = Param(None, description="User to check info of"),
    ):
        """
        Get details of a server member.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - user (disnake.Member): The member to get details of. (Optional)

        Returns:
        None
        """
        await ctx.response.defer()
        embed = UserInfo(ctx, user)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.slash_command(name="info-server", description="Get details of server")
    async def server(self, ctx: disnake.AppCmdInter):
        """
        Get details of the server.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.

        Returns:
        None
        """
        await ctx.response.defer()
        embed = await ServerInfo(ctx)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="info-translate", description="Translate anything to any language"
    )
    async def translate(
        self,
        ctx: disnake.AppCmdInter,
        language: str = Param(
            description="Language to translate in", autocomplete=language_options
        ),
        text: str = Param(description="Text to translate"),
    ):
        """
        Translate text to a specified language.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - language (str): The language to translate to.
        - text (str): The text to translate.

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            language = Languages[language.capitalize()]
        except KeyError:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['failed']} This languag is not suported.",
                    colour=1199267,
                )
            )
        req = requests.get(
            f"https://api.popcat.xyz/translate?to={language}&text={text}"
        )
        data = (json.loads(req.text))["translated"]
        embed = disnake.Embed()
        embed.add_field("Text", text)
        embed.add_field("Translation", data)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.slash_command(name="info-fact", description="Get a fact")
    async def fact(self, ctx: disnake.AppCmdInter):
        """
        Get a random fact.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.

        Returns:
        None
        """
        await ctx.response.defer()
        req = requests.get("https://api.popcat.xyz/fact")
        data = (json.loads(req.text))["fact"]
        await ctx.send(embed=disnake.Embed(description=data))

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(name="info-joke", description="Get a joke")
    async def joke(self, ctx: disnake.AppCmdInter):
        """
        Get a random joke.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.

        Returns:
        None
        """
        await ctx.response.defer()
        req = requests.get("https://api.popcat.xyz/joke")
        data = (json.loads(req.text))["joke"]
        await ctx.send(embed=disnake.Embed(description=data))

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(name="info-avatar", description="Get avatar of a user")
    async def avatar(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(None, description="whose avatar?"),
    ):
        """
        Get the avatar of a user.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - member (disnake.Member): The member whose avatar to get. (Optional)

        Returns:
        None
        """
        await ctx.response.defer()
        if member is None:
            member = ctx.author
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = f"{member.name}'s avatar."
        embed.set_image(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.user_command()
    async def Avatar(self, ctx: disnake.AppCmdInter, Member: disnake.Member = None):
        """
        Get the avatar of a user.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - Member (disnake.Member): The member whose avatar to get. (Optional)

        Returns:
        None
        """
        if Member is None:
            Member = ctx.author
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = f"{Member.name}'s avatar."
        embed.set_image(url=Member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.user_command(name="User Details")
    async def User(self, ctx: disnake.AppCmdInter, User: disnake.Member = None):
        """
        Get details of a user.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - User (disnake.Member): The user to get details of. (Optional)

        Returns:
        None
        """
        embed = UserInfo(ctx, User)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
