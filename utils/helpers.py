import asyncio
import json
from loguru import logger
import disnake
import sys
import humanize
import time
import datetime as dt
from motor.motor_asyncio import AsyncIOMotorClient
from os import system, name


CogEmoji = {
    "Anime": "🎎",
    "Fun": "🎭",
    "Info": "🌐",
    "Moderator": "👮🏻",
    "Music": "🎶",
    "Nsfw": "🔞",
    "Settings": "🛠️",
    "Help": "🆘",
}


def Embed(bot, ctx, footer):
    embed = disnake.Embed()
    embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar)
    embed.set_footer(
        text=f"{footer} by  {ctx.author.display_name}",
        icon_url=ctx.author.display_avatar.url,
    )

    return embed


def Log(bot, ctx, action, detail, guilty: disnake.Member, mod: disnake.Member):
    channel = ""
    hour = time.time()
    stamp = dt.datetime.fromtimestamp(hour).strftime("%Y-%m-%d %H:%M:%S")
    embed = disnake.Embed(title=action, description=detail, color=16711680)
    embed.add_field(name="Evidence", value=ctx.content, inline=False)
    embed.add_field(name="Guilty", value=guilty.mention, inline=True)
    embed.add_field(name="Channel", value=f"<#{str(ctx.channel.id)}>", inline=True)
    embed.add_field(name="Time", value=stamp, inline=True)
    embed.add_field(name="Moderator", value=mod.display_name, inline=True)
    embed.set_author(name=bot.user.display_name, icon_url=f"{bot.user.avatar.url}")
    embed.set_footer(text=f"Punished by {mod.display_name}")
    return embed


class BotInformation:
    def __init__(
        self,
        bot,
    ):
        self.bot = bot

    async def get_bot_info(
        self, interaction: disnake.ApplicationCommandInteraction
    ) -> disnake.Embed:
        version = sys.version_info
        em = disnake.Embed(color=disnake.Colour.random())

        em.add_field(
            name="Bot",
            value=f"{self.bot.icons['arrow']} **Guilds**: `{len(self.bot.guilds)}`\n{self.bot.icons['arrow']} **Users**: `{len(self.bot.users)}`\n{self.bot.icons['arrow']} **Commands**: `{len([cmd for cmd in list(self.bot.walk_commands())if not cmd.hidden])}`",
            inline=True,
        )
        em.add_field(
            name="Bot Owner",
            value=f"{self.bot.icons['arrow']} **Name**: `{self.bot.owner}`\n{self.bot.icons['arrow']} **ID**: `{self.bot.owner.id}`",
            inline=True,
        )
        em.add_field(
            name="Developers",
            value=f"{self.bot.icons['arrow']} `{await self.bot.fetch_user(1015643292593029210)}`",
            inline=True,
        )
        em.set_thumbnail(url=self.bot.user.display_avatar.url)
        em.set_footer(
            text=f"Python {version[0]}.{version[1]}.{version[2]} • disnake {disnake.__version__}"
        )
        return em

    async def get_uptime(
        self, ctx: disnake.ApplicationCommandInteraction
    ) -> disnake.Embed:
        uptime = disnake.utils.utcnow() - self.bot.start_time
        time_data = humanize.precisedelta(uptime)
        embed = disnake.Embed(
            title="Uptime", description=time_data, colour=disnake.Colour.random()
        ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        return embed

    async def get_latency(
        self, ctx: disnake.ApplicationCommandInteraction
    ) -> disnake.Embed:
        times = []
        counter = 0
        embed = disnake.Embed(colour=disnake.Colour.random())
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await ctx.edit_original_message(
                content=f"Trying Ping {('.' * counter)} {counter}/3"
            )
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            if speed < 160:
                embed.add_field(
                    name=f"Ping {counter}:",
                    value=f"{self.bot.icons['online']} | {speed}ms",
                    inline=True,
                )
            elif speed > 170:
                embed.add_field(
                    name=f"Ping {counter}:",
                    value=f"{self.bot.icons['away']} | {speed}ms",
                    inline=True,
                )
            else:
                embed.add_field(
                    name=f"Ping {counter}:",
                    value=f"{self.bot.icons['dnd']} | {speed}ms",
                    inline=True,
                )

        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(
            name="Normal Speed",
            value=f"{round((round(sum(times)) + round(self.bot.latency * 1000)) / 4)}ms",
        )

        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.display_avatar.url)
        return embed

    async def get_commands(self, ctx: disnake.AppCommandInteraction) -> disnake.Embed:
        embed = disnake.Embed(colour=disnake.Colour.random())
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.display_avatar.url)
        for cog in self.bot.cogs:
            if cog in ("Message", "Help"):
                continue
            cogs = self.bot.get_cog(cog)
            cmds = ""
            for command in cogs.get_slash_commands():
                cmds += f"`{command.name}` "

            embed.add_field(name=f"\{CogEmoji[cog]} {cog}", value=cmds, inline=False)

        return embed

    async def home(self, ctx: disnake.AppCommandInteraction) -> disnake.Embed:
        owner = await self.bot.fetch_user(self.bot.owned)
        t_members = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member in t_members and not member.bot:
                    t_members.append(member)
        cmds = 0
        for cmd in self.bot.slash_commands:
            cmds += len(cmd.children)
        cmds += len(self.bot.application_commands)

        version = sys.version_info
        embed = disnake.Embed(
            description=f"{self.bot.config.about['info']}\n\n__**BOT VERSION**__\n{self.bot.config.about['cur_version']}\n__**KNOWN BUGS**__\n{self.bot.config.about['known_bugs']}\n__**NEW RELEASE**__\n{self.bot.config.about['updates']}",
            colour=53759,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )

        embed.add_field(
            name="Bot",
            value=f"{self.bot.icons['arrow']} **Servers**: `{len(self.bot.guilds)}`\n{self.bot.icons['arrow']} **Users**: `{len(self.bot.users)}`\n{self.bot.icons['arrow']} **Commands**: `{cmds}`",
            inline=True,
        )

        embed.add_field(
            name="Bot Owner",
            value=f"{self.bot.icons['arrow']} **Name**: `{owner}`\n{self.bot.icons['arrow']} **ID**: `{owner.id}`\n{self.bot.icons['arrow']} **Server**: [{self.bot.config.data['bot']['server']['name']}]({self.bot.config.data['bot']['server']['invite']})",
            inline=True,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(
            text=f"Python {version[0]}.{version[1]}.{version[2]} • Disnake {disnake.__version__}",
            icon_url="https://spng.subpng.com/20180712/jrh/kisspng-professional-python-programmer-computer-programmin-python-logo-download-5b47725bdc5820.2110724115314089879026.jpg",
        )

        return embed


class BotInformationView(disnake.ui.View):
    def __init__(self, interaction: disnake.ApplicationCommandInteraction, bot):
        super().__init__(timeout=30)
        self.interaction = interaction
        self.bot = bot
        self.BotInformation = BotInformation(bot=bot)
        self.is_message_deleted = False
        self.add_item(
            item=disnake.ui.Button(
                label="Invite",
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions={self.bot.config.data['bot']['permissions']}&scope=bot%20applications.commands",
                emoji=f"{self.bot.icons['dev']}",
                row=1,
            )
        )
        self.add_item(
            item=disnake.ui.Button(
                label="Support",
                url=f"{self.bot.config.data['bot']['server']['invite']}",
                emoji=f"{self.bot.icons['discovery']}",
                row=1,
            )
        )

    @disnake.ui.button(label="Home", emoji="🏠", style=disnake.ButtonStyle.green, row=0)
    async def home(
        self, button: disnake.ui.Button, interaction: disnake.AppCommandInteraction
    ):
        try:
            await interaction.response.defer()
        except disnake.errors.NotFound:
            pass
        embed = await self.BotInformation.home(ctx=self.interaction)
        await self.interaction.edit_original_message(embed=embed)

    @disnake.ui.button(
        label="Latency", emoji="🤖", style=disnake.ButtonStyle.green, row=0
    )
    async def latency(
        self,
        button: disnake.ui.Button,
        interaction: disnake.ApplicationCommandInteraction,
    ):
        try:
            await interaction.response.defer()
        except disnake.errors.NotFound:
            pass
        embed = await self.BotInformation.get_latency(ctx=self.interaction)
        await self.interaction.edit_original_message(embed=embed)

    @disnake.ui.button(
        label="Uptime", emoji="⏳", style=disnake.ButtonStyle.green, row=0
    )
    async def uptime(
        self,
        button: disnake.ui.Button,
        interaction: disnake.ApplicationCommandInteraction,
    ):
        try:
            await interaction.response.defer()
        except disnake.errors.NotFound:
            pass
        await self.interaction.edit_original_message(
            embed=await self.BotInformation.get_uptime(ctx=self.interaction)
        )

    @disnake.ui.button(
        label="Commands", emoji="📃", style=disnake.ButtonStyle.secondary, row=1
    )
    async def Commands(
        self,
        button: disnake.ui.Button,
        interaction: disnake.ApplicationCommandInteraction,
    ):
        try:
            await interaction.response.defer()
        except disnake.errors.NotFound:
            pass
        await self.interaction.edit_original_message(
            embed=await self.BotInformation.get_commands(ctx=self.interaction)
        )

    @disnake.ui.button(
        label="Quit", style=disnake.ButtonStyle.danger, emoji="✖️", row=2
    )
    async def quit(
        self,
        button: disnake.ui.Button,
        interaction: disnake.ApplicationCommandInteraction,
    ):
        try:
            await interaction.response.defer()
        except disnake.errors.NotFound:
            pass
        self.is_message_deleted = True
        await self.interaction.delete_original_message()

    async def on_timeout(self) -> None:
        if self.is_message_deleted:
            return

        for button in self.children:
            button.disabled = True

        try:
            await self.interaction.edit_original_message(view=self)
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
            return


class Config:
    def __init__(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")

        with open("./config/config.json", "r") as f:
            self.data = json.load(f)

        with open("./config/icons.json", "r", encoding="utf-8") as f:
            self.icons = json.load(f)
        
        self.initDB()

    async def logChannel(self, ctx) -> int:
        return (await self.database.Configs.find_one({"_id": str(ctx.guild.id)}))[
            "logchannel"
        ]

    def initDB(self) -> None:

        logger.info(f"CONNECTING TO DATABASE...")

        self.loop = asyncio.get_event_loop()
        try:
            self.client = AsyncIOMotorClient(
                self.data["api"]["mongoDB"], io_loop=self.loop
            )
            logger.success(f"Connected to Database")
        except Exception as error:
            logger.error(f"Failed to connect to Database")
            logger.exception(error)
            exit(code=1)

    @property
    def token(self):
        try:
            return self.data["bot"]["token"]
        except AttributeError:
            logger.error("No token found.")
            exit(code=1)

    @property
    def name(self):
        try:
            return self.data["bot"]["name"]
        except AttributeError:
            logger.error("Please specify bot's name first.")
            exit(code=1)

    @property
    def version(self):
        try:
            return self.data["bot"]["version"]
        except AttributeError:
            logger.error("Please specify bot's version first.")
            exit(code=1)

    @property
    def owner(self):
        try:
            return self.data["bot"]["owner"]
        except AttributeError:
            logger.error(
                "No owners found in config.\nIf you are the bot owner,\nplease add yourself to the owners list."
            )
            exit(code=1)

    @property
    def api_keys(self):
        return self.data["api"]

    @property
    def logger(self):
        return logger

    @property
    def about(self):
        return self.data["bot"]["about"]

    @property
    def database(self):
        return self.client.GuildData
