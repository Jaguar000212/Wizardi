import disnake
import datetime as dt
from googletrans import LANGUAGES
import string

Languages = {}
for key, value in LANGUAGES.items():
    Languages[value.capitalize] = key


def SuperheroInformation(data: dict, ctx: disnake.AppCmdInter):
    """
    Generates an embed with detailed information about a superhero character.

    Args:
        data (dict): The data containing information about the superhero character.
        ctx (disnake.AppCmdInter): The context of the command.

    Returns:
        disnake.Embed: The embed containing the detailed information of the character.
    """
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
            name=ctx.bot.user.display_name,
            icon_url=f"{ctx.bot.user.avatar.url}",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        return embed


def UserInfo(ctx: disnake.AppCmdInter, user: disnake.User = None):
    """
    Generates an embed with detailed information about a user.

    Args:
        ctx (disnake.AppCmdInter): The context of the command.
        user (disnake.User, optional): The user to get the information of. Defaults to None.

    Returns:
        disnake.Embed: The embed containing the detailed information of the user.
    """
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
    embed = ctx.bot.Embed(ctx.bot, ctx, "Requested")
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
    return embed


async def ServerInfo(ctx: disnake.AppCmdInter):
    """
    Generates an embed with detailed information about a server.

    Args:
        ctx (disnake.AppCmdInter): The context of the command.

    Returns:
        disnake.Embed: The embed containing the detailed information of the server.
    """
    guild_features = ""
    for feature in ctx.guild.features:
        guild_features += f'{string.capwords((feature.replace("ENABLED", "")).replace("_", " "))} {ctx.bot.icons["check"]}\n'

    if len(guild_features) == 0:
        guild_features = "None"

    embed = ctx.bot.Embed(ctx.bot, ctx, "Requested")

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
    return embed
