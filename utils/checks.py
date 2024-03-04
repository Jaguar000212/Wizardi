from disnake.ext import commands
import disnake
import requests

from utils.exceptions import NoVote


def voter():
    async def dbl_check(ctx: disnake.AppCommandInter):
        header = {"authorization": f"{ctx.bot.config.api_keys['dbl']}"}
        get = requests.get(
            f"https://discordbotlist.com/api/v1/bots/{ctx.bot.user.id}/upvotes",
            headers=header,
        )
        data = get.json()
        try:
            for i in data["upvotes"]:
                if i["user_id"] == str(ctx.author.id):
                    return True
            raise NoVote("No Vote")
        except KeyError:
            ctx.bot.logger.error(f"Failed to fetch Discord Bot List votes: {get.status_code}")
            return True
    return commands.check(dbl_check)
