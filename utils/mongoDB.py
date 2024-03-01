class BotDB:
    """
    A class representing a bot's database operations.
    """

    def __init__(self, bot):
        """
        Initialize the BotDB class.

        Args:
            bot: The bot instance.
        """
        self.bot = bot

    async def createConfig(self, _id: str):
        """
        Create a new configuration in the database.

        Args:
            _id: The ID of the configuration.

        Returns:
            The result of the insert operation.
        """
        try:
            return await self.bot.database.Configs.insert_one(
                {"_id": _id, "LogChannel": None, "TempChannels": []}
            )
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def deleteConfig(self, _id: str):
        """
        Delete a configuration from the database.

        Args:
            _id: The ID of the configuration.

        Returns:
            The result of the delete operation.
        """
        try:
            return await self.bot.database.Configs.delete_one({"_id": _id})
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def getLogChannel(self, _id: str):
        """
        Get the log channel for a configuration.

        Args:
            _id: The ID of the configuration.

        Returns:
            The log channel ID.
        """
        try:
            return (await self.bot.database.Configs.find_one({"_id": _id}))[
                "LogChannel"
            ]
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def updateLogChannel(self, _id: str, channelID: str = None):
        """
        Update the log channel for a configuration.

        Args:
            _id: The ID of the configuration.
            channelID: The ID of the new log channel.

        Returns:
            The number of modified documents.
        """
        try:
            return (
                await self.bot.database.Configs.update_one(
                    {"_id": _id}, {"$set": {"LogChannel": channelID}}
                )
            ).modified_count
        except Exception as e:
            self.bot.logger.error("Error", e)
