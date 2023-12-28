from os import system, name
from bot import Bot
from disnake.errors import HTTPException


def launch():
    bot = Bot()
    config = bot.config

    bot.remove_command("help")
    bot.load_cogs("cogs")
    try:
        bot.run(config.token)
    except HTTPException:
        print("Bot has been temporarily banned by Discord")
        system("kill 1")
        print("Trying fix...")
        try:
            bot.run(config.token)
        except HTTPException:
            bot.logger.error("Temporarily banned!")
    except Exception as error:
        bot.logger.exception(error)

launch()
