import disnake
import akinator as ak
from random import randint
import asyncio

async def AkinatorGame(bot, ctx: disnake.AppCmdInter):
        intro = disnake.Embed(
            title="Akinator",
            description=f"Hello, {ctx.author.mention} I am Akinator!!!\nThink about a real or fictional character. I will try to guess who it is",
            color=disnake.Colour.blue(),
        )
        intro.set_thumbnail(
            url="https://en.akinator.com/bundles/elokencesite/images/akinator.png?v93"
        )
        intro.set_author(
            name=bot.user.display_name, icon_url=f"{bot.user.avatar.url}"
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
            name=bot.user.display_name, icon_url=f"{bot.user.avatar.url}"
        )
        bye.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        bye.set_thumbnail(
            url="https://i.pinimg.com/originals/28/fc/0b/28fc0b88d8ded3bb8f89cb23b3e9aa7b.png"
        )
        await ctx.send(embed=intro)

        ans_emoji = {
            "👍🏻": "yes",
            "👎🏻": "no",
            "🤔": "probably",
            "🤷🏻": "idk",
            "🔙": "back",
        }

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
                name=bot.user.display_name,
                icon_url=f"{bot.user.avatar.url}",
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
                reaction, user = await bot.wait_for(
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
            elif str(reaction.emoji) in ans_emoji:
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
            name=bot.user.display_name, icon_url=f"{bot.user.avatar.url}"
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
            reaction, user = await bot.wait_for(
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
                name=bot.user.display_name,
                icon_url=f"{bot.user.avatar.url}",
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
                name=bot.user.display_name,
                icon_url=f"{bot.user.avatar.url}",
            )
            no.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            await ctx.channel.send(embed=no)
        await ctx.send(embed=bye)