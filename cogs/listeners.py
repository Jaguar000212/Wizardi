import disnake
from disnake.ext import commands
import datetime as dt


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await self.bot.database.Configs.insert_one(
                {"_id": str(guild.id), "LogChannel": None}
            )
        except Exception as e:
            self.bot.logger.error("Error", e)

        me = await self.bot.fetch_user(self.bot.owned)
        embed = disnake.Embed(
            title="Joined Guild",
            description=f"Joined guild `{guild.name}`, owned by **{guild.owner}**",
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.add_field(
            name="__Members__",
            value=f"`Total Members` - {guild.member_count}\n`Bots` - {len([member for member in guild.members if member.bot])}",
        )
        embed.add_field(
            name="__Channels__",
            value=f"`Total Channels` - {len(guild.channels)}\n`Text Channels` - {len(guild.text_channels)}\n`Voice Channels` - {len(guild.voice_channels)}",
        )
        embed.add_field(
            name="__Misc__",
            value=f"`Total Roles` = {len(guild.roles)}\n`Total Emojis` - {len(guild.emojis)}",
        )
        try:
            embed.set_thumbnail(url=f"{guild.icon.url}")
        except:
            pass

        await me.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            await self.bot.database.Configs.delete_one({"_id": str(guild.id)})
        except Exception as e:
            self.bot.logger.error("Error", e)

        me = await self.bot.fetch_user(self.bot.owned)
        embed = disnake.Embed(
            title="Left Guild",
            description=f"Left guild `{guild.name}`, owned by **{guild.owner}**",
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.add_field(
            name="__Members__",
            value=f"`Total Members` - {guild.member_count}\n`Bots` - {len([member for member in guild.members if member.bot])}",
        )
        try:
            embed.set_thumbnail(url=f"{guild.icon.url}")
        except:
            pass

        await me.send(embed=embed)


def setup(bot):
    bot.add_cog(Listeners(bot))
