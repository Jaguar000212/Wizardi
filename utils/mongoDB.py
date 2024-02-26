class BotDB:
    def __init__(self, bot):
        self.bot = bot

    async def createConfig(self, _id: str):
        try:
            return await self.bot.database.Configs.insert_one(
                {"_id": _id, "LogChannel": None, "TempChannels": []}
            )
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def deleteConfig(self, _id: str):
        try:
            return await self.bot.database.Configs.delete_one({"_id": _id})
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def getLogChannel(self, _id: str):
        try:
            return (await self.bot.database.Configs.find_one({"_id": _id}))[
                "LogChannel"
            ]
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def updateLogChannel(self, _id: str, channelID: str = None):
        try:
            return (
                await self.bot.database.Configs.update_one(
                    {"_id": _id}, {"$set": {"LogChannel": channelID}}
                )
            ).modified_count
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def createTempChannel(self, _id: str,  memberID: str, channelID: str):
        try:
            return await self.bot.database.Configs.update_one(
                {"_id": _id}, {"$push": {"TempChannels": {channelID : memberID}}}
            )
        except Exception as e:
            self.bot.logger.error("Error", e)

    async def getTempChannel(self, _id: str, channelID: str):
        try:
            return (await self.bot.database.Configs.find_one({"_id": _id}))[
                "TempChannels"
            ][channelID]
        except Exception as e:
            self.bot.logger.error("Error", e)
