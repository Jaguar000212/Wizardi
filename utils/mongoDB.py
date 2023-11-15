

class BotDB:
    def __init__(self, bot):
        self.bot = bot

    async def updateLogChannel(self, _id: str, channelID: str = None):
        try:
            return (
                await self.bot.database.Configs.update_one(
                    {"_id": _id}, {"$set": {"LogChannel": channelID}}
                )
            ).modified_count
        except Exception as e:
            self.bot.logger.error("Error", e)
