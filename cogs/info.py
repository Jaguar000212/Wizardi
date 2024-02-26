import string
import disnake
from disnake.ext import commands
from disnake.ext.commands.params import Param
import requests
import json
import datetime as dt

from utils.information import *
from bot import Bot


class Info(commands.Cog):
    """
    Get some useful information from the Internet
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="info-character",
        description="Find info about your favourite character",
    )
    async def character(
        self, ctx: disnake.AppCmdInter, name=Param(description="Name of the character")
    ):
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
        await ctx.response.defer()
        if user is None:
            user = ctx.author
        perms = ""
        badges = ""
        roles = ", ".join([role.mention for role in user.roles])
        for perm in user.guild_permissions:
            if perm[1]:
                perm = perm[0].replace("_", " ")
                perm = perm.capitalize()
                perms += f"{perm}, "
        for flag, value in user.public_flags:
            if value:
                badges += f"{flag.replace('_', ' ').capitalize()}, "
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = user.name
        embed.add_field(
            "__General Info__",
            f"`Username` - {user}\n`UserID` - {user.id}\n`Nickname` - {user.nick}\n`Badges` - {badges[:-2]}\n`Created at` - {user.created_at.strftime('%d %B, %Y, %H:%M:%S')}\t`{(dt.date.today() - user.created_at.date()).days}` days ago\n`Joined at` - {user.joined_at.strftime('%d %B, %Y, %H:%M:%S')}\t`{(dt.date.today() - user.joined_at.date()).days}` days ago",
            inline=False,
        )
        embed.add_field(
            "__Role Info__",
            f"`Highest Role` - {user.top_role.mention}\n`Roles` - \n> {roles}",
            inline=False,
        )
        embed.add_field("__Permissions__", f"> {perms[:-2]}", inline=False)
        embed.set_thumbnail(user.display_avatar.url)
        try:
            embed.set_image(user.banner.url)
        except AttributeError:
            pass
        embed.color = int(user.color)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.slash_command(name="info-server", description="Get details of server")
    async def server(self, ctx: disnake.AppCmdInter):
        await ctx.response.defer()
        guild_features = ""
        for feature in ctx.guild.features:
            guild_features += f'{string.capwords((feature.replace("ENABLED", "")).replace("_", " "))} {self.bot.icons["check"]}\n'

        if len(guild_features) == 0:
            guild_features = "None"

        embed = self.bot.Embed(self.bot, ctx, "Requested")

        if not ctx.guild.description is None:
            embed.description = f"{ctx.guild.description}"

        embed.title = ctx.guild.name
        embed.add_field(
            name="__Owner__",
            value=f"{ctx.guild.owner.mention} | {ctx.guild.owner.id}",
            inline=False,
        )
        embed.add_field(
            name="__General__",
            value=f"`ID` - {ctx.guild.id}\n`Date Created` - {ctx.guild.created_at.strftime('%d %B, %Y, %H:%M:%S')}",
            inline=False,
        )
        embed.add_field(
            name="__Channels__",
            value=f"`Total` - {len(ctx.guild.channels)}\n`Text` - {len(ctx.guild.text_channels)}\n`Voice` - {len(ctx.guild.voice_channels)}\n`Categories` - {len(ctx.guild.categories)}",
        )
        embed.add_field(
            name="__Members__",
            value=f"`Total` - {ctx.guild.member_count}\n`Human` - {len([member for member in ctx.guild.members if not member.bot])}\n`Bot` -  {len([member for member in ctx.guild.members if member.bot])}",
        )
        embed.add_field(
            name="__Misc__",
            value=f"`Roles` - {len(ctx.guild.roles)}\n`Emojis` - {len(await ctx.guild.fetch_emojis())}\n`Verification Level` - {ctx.guild.verification_level.name.capitalize()}\n`Notifications` - {ctx.guild.default_notifications.name.replace('_', ' ').capitalize()}",
        )
        embed.add_field(name="__Features__", value=guild_features, inline=False)
        try:
            embed.set_thumbnail(ctx.guild.icon.url)
        except AttributeError:
            pass

        try:
            embed.set_image(ctx.guild.banner.url)
        except AttributeError:
            pass

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="info-translate", description="Translate anything to any language"
    )
    async def translate(
        self,
        ctx: disnake.AppCmdInter,
        language:str=Param(description="Language to translate in"),
        text:str=Param(description="Text to translate", choices=Languages),
    ):
        await ctx.response.defer()
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
        await ctx.response.defer()
        req = requests.get("https://api.popcat.xyz/fact")
        data = (json.loads(req.text))["fact"]
        await ctx.send(embed=disnake.Embed(description=data))

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(name="info-joke", description="Get a joke")
    async def joke(self, ctx: disnake.AppCmdInter):
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
        await ctx.response.defer()
        if member is None:
            member = ctx.author
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = f"{member.name}'s avatar."
        embed.set_image(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.user_command()
    async def Avatar(self, ctx: disnake.AppCmdInter, Member: disnake.Member = None):
        if Member is None:
            Member = ctx.author
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = f"{Member.name}'s avatar."
        embed.set_image(url=Member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.user_command(name="User Details")
    async def User(self, ctx: disnake.AppCmdInter, User: disnake.Member = None):
        if User is None:
            User = ctx.author
        perms = ""
        badges = ""
        roles = ", ".join([role.mention for role in User.roles])
        for perm in User.guild_permissions:
            if perm[1]:
                perm = perm[0].replace("_", " ")
                perm = perm.capitalize()
                perms += f"{perm}, "
        for flag, value in User.public_flags:
            if value:
                badges += f"{flag.replace('_', ' ').capitalize()} "
        embed = self.bot.Embed(self.bot, ctx, "Requested")
        embed.title = User.name
        embed.add_field(
            "__General Info__",
            f"`Username` - {User}\n`UserID` - {User.id}\n`Nickname` - {User.nick}\n`Badges` - {badges}\n`Created at` - {User.created_at.strftime('%d %B, %Y, %H:%M:%S')}\t`{(dt.date.today() - User.created_at.date()).days}` days ago\n`Joined at` - {User.joined_at.strftime('%d %B, %Y, %H:%M:%S')}\t`{(dt.date.today() - User.joined_at.date()).days}` days ago",
            inline=False,
        )
        embed.add_field(
            "__Role Info__",
            f"`Highest Role` - {User.top_role.mention}\n`Roles` - \n> {roles}",
            inline=False,
        )
        embed.add_field("__Permissions__", f"> {perms[:-2]}", inline=False)
        embed.set_thumbnail(User.display_avatar.url)
        try:
            embed.set_image(User.banner.url)
        except AttributeError:
            pass
        embed.color = int(User.color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
