import string
import disnake
from disnake.ext import commands
from disnake.ext.commands.params import Param
import requests
from bot import Bot
import json
import datetime as dt

deleted_msg = {}


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
            verify=False
        )
        data = json.loads(req.text)
        if data["response"] == "success":
            for result in data["results"]:
                chara_name = result["name"]
                chara_id = result["id"]
                intelli = result["powerstats"]["intelligence"]
                strength = result["powerstats"]["strength"]
                speed = result["powerstats"]["speed"]
                durability = result["powerstats"]["durability"]
                power = result["powerstats"]["power"]
                combat = result["powerstats"]["combat"]
                f_name = result["biography"]["full-name"]
                ego = result["biography"]["alter-egos"]
                aliases = ", ".join(result["biography"]["aliases"])
                pob = result["biography"]["place-of-birth"]
                f_appear = result["biography"]["first-appearance"]
                pub = result["biography"]["full-name"]
                align = result["biography"]["alignment"]
                gender = result["appearance"]["gender"]
                race = result["appearance"]["race"]
                height = (
                    result["appearance"]["height"][0]
                    + " or "
                    + data["results"][0]["appearance"]["height"][1]
                )
                weight = (
                    result["appearance"]["weight"][0]
                    + " or "
                    + data["results"][0]["appearance"]["weight"][1]
                )
                eye = result["appearance"]["eye-color"]
                hair = result["appearance"]["hair-color"]
                occu = result["work"]["occupation"]
                base = result["work"]["base"]
                grp = result["connections"]["group-affiliation"]
                relate = result["connections"]["relatives"]
                img = result["image"]["url"]

                embed = disnake.Embed(
                    title=chara_id + " " + chara_name,
                    description="Detailed information of your character is as follows -",
                    color=53759,
                    timestamp=dt.datetime.now(dt.timezone.utc),
                )
                embed.add_field(
                    name="Powerstats",
                    value=f"`Intelligence` {intelli}\n`Strength` {strength}\n`Speed`{speed}\n`Durability` {durability}\n`Power` {power}\n`Combat` {combat}",
                    inline=True,
                )
                embed.add_field(
                    name="Appearance",
                    value=f"`Gender` {gender}\n`Race` {race}\n`Height` {height}\n`Weight` {weight}\n`Eye-Color` {eye}\n`Hair-Color` {hair}",
                    inline=True,
                )
                embed.add_field(
                    name="Biography",
                    value=f"`Full Name` {f_name}\n`Alter-Egos` {ego}\n`Aliases` {aliases}\n`Place of Birth` {pob}\n`First Appearance` {f_appear}\n`Publisher` {pub}\n`Alignment` {align}",
                    inline=False,
                )
                embed.add_field(
                    name="Work",
                    value=f"`Occupation` {occu}\n`Base` {base}",
                    inline=False,
                )
                embed.add_field(
                    name="Connections",
                    value=f"`Group Affiliations` {grp}\n`Relations` {relate}",
                    inline=False,
                )
                embed.set_thumbnail(url=img)
                embed.set_author(
                    name=self.bot.user.display_name,
                    icon_url=f"{self.bot.user.avatar.url}",
                )
                embed.set_footer(
                    text=f"Requested by {ctx.author.display_name}",
                    icon_url=ctx.author.display_avatar.url,
                )
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
    @commands.slash_command(description="Translate anything to any language")
    async def translate(
        self,
        ctx: disnake.AppCmdInter,
        language=Param(description="Language to translate in"),
        input=Param(description="Text to translate"),
    ):
        await ctx.response.defer()
        req = requests.get(
            f"https://api.popcat.xyz/translate?to={language}&text={input}"
        )
        data = (json.loads(req.text))["translated"]
        embed = disnake.Embed()
        embed.add_field("Text", input)
        embed.add_field("Translation", data)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.slash_command(description="Get a fact")
    async def fact(self, ctx: disnake.AppCmdInter):
        await ctx.response.defer()
        req = requests.get("https://api.popcat.xyz/fact")
        data = (json.loads(req.text))["fact"]
        await ctx.send(embed=disnake.Embed(description=data))

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(description="Get a joke")
    async def joke(self, ctx: disnake.AppCmdInter):
        await ctx.response.defer()
        req = requests.get("https://api.popcat.xyz/joke")
        data = (json.loads(req.text))["joke"]
        await ctx.send(embed=disnake.Embed(description=data))

    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(description="Snipe recently deleted messages channel-wise.")
    async def snipe(
        self,
        ctx: disnake.AppCmdInter,
        channel: disnake.TextChannel = Param(None, description="Channel to check in"),
    ):
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        try:
            msg = deleted_msg[channel.id]
            if not len(msg[1]) == 0:
                embed = self.bot.Embed(self.bot, ctx, "Requested")
                embed.title = "Last Message"
                embed.description = f"`Author` - {msg[0].mention}\n`Channel` - {channel.mention}\n`Time` - {msg[2]}\n\n```{msg[1]}```"
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    embed=disnake.Embed(
                        description="No recently deleted message, might be a media or an embed."
                    ),
                    delete_after=4,
                )
        except KeyError:
            await ctx.send(
                embed=disnake.Embed(description="No recently deleted message."),
                delete_after=4,
            )

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(description="Get avatar of a user")
    async def avatar(
        self, ctx: disnake.AppCmdInter, member: disnake.Member = Param(None, description = "whose avatar?")
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

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        global deleted_msg
        deleted_msg[ctx.channel.id] = (
            ctx.author,
            ctx.content,
            ctx.created_at.strftime("%d %B, %Y, %H:%M:%S"),
        )


def setup(bot):
    bot.add_cog(Info(bot))
