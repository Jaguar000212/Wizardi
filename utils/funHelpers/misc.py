import disnake
from random import choice
import asyncio


def slotGame(ctx: disnake.AppCmdInter):
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


async def beerOffer(bot, user: disnake.Member, ctx: disnake.AppCmdInter, reason: str = None):
    if not user or user.id == ctx.author.id:
        return await ctx.send(
            embed=disnake.Embed(
                description=f"**{ctx.author.name}**: paaaarty!🎉🍺",
                color=disnake.Colour.magenta(),
            )
        )
    if user.id == bot.user.id:
        return await ctx.send(
            embed=disnake.Embed(
                description="*drinks beer with you* 🍻",
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
        await bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
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
        beer_offer = f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
        await ctx.edit_original_message(
            embed=disnake.Embed(description=beer_offer, color=disnake.Colour.magenta())
        )
