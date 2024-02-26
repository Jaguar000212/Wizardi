import disnake
import datetime as dt
from googletrans import LANGUAGES


Languages = {}
for key, value in LANGUAGES.items():
    Languages[value.capitalize] = key

def SuperheroInformation(data: dict, ctx: disnake.AppCmdInter):
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