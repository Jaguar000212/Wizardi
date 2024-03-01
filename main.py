from os import system
from bot import Bot
from disnake.errors import HTTPException


def launch():
    """
    Launches the bot and handles exceptions.

    This function creates an instance of the Bot class, loads the necessary cogs,
    and runs the bot using the token from the configuration. It also handles
    HTTPException and other exceptions, logging any errors that occur.

    If the bot is temporarily banned by Discord, it attempts to fix the issue
    by restarting the bot.

    Note: This function assumes that the Bot class and its dependencies are properly imported.
    """
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
