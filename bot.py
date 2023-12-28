import pkgutil
import sys
import traceback

import disnake
from disnake import AllowedMentions, Intents
from disnake.ext import commands

from utils.helpers import Config, Embed
from utils.exceptions import *


intents = Intents.default()
intents.members = True
intents.message_content = True
config = Config()


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned,
            strip_after_prefix=True,
            allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False),
            intents=intents,
            reload=True,
            *args,
            **kwargs,
        )
        self.config = config
        self.logger = self.config.logger
        self.name = self.config.name
        self.version = self.config.version
        self.owned = self.config.owner
        self.icons = self.config.icons
        self.Embed = Embed

        self.start_time = disnake.utils.utcnow()

        self.add_check(
            commands.bot_has_permissions(
                read_messages=True,
                send_messages=True,
                embed_links=True,
                read_message_history=True,
                external_emojis=True,
                add_reactions=True,
            ).predicate
        )

    def load_cogs(self, exts):
        self.logger.info("LOADING COGS...")
        for cog in pkgutil.iter_modules([exts]):
            module = f"cogs.{cog.name}"
            try:
                self.load_extension(module)
                self.logger.success(f"{cog.name.upper()} loaded")
            except Exception as error:
                self.logger.warning(f"{cog.name.upper()} failed to load")
                self.logger.exception(error)

    async def on_connect(self):
        print(
            f"|----------Bot Connected---------|\n"
            f"|  Bot name: {self.name}\n"
            f"|  Bot Version: {self.version}\n"
            f"|  Bot ID: {self.user.id}\n"
            f"|  Total Guilds: {len(self.guilds)}\n"
            f"|  Total Shards: {self.shard_count}\n"
            f"|--------------------------------|"
        )

    async def on_ready(self):
        pass

    async def on_shard_connect(self, shard_id: int):
        self.logger.info(
            f"SHARD {shard_id} CONNECTED @{round(self.get_shard(shard_id).latency * 1000)} ms"
        )

    async def on_shard_diconnect(self, shard_id: int):
        self.logger.warning(f"SHARD {shard_id} DISCONNECTED")

    async def on_shard_resumed(self, shard_id: int):
        self.logger.success(
            f"SHARD {shard_id} RESUMED @{round(self.get_shard(shard_id).latency * 1000)} ms"
        )

    async def on_slash_command_error(self, ctx: disnake.AppCmdInter, error: Exception):
        ctx.application_command.reset_cooldown(ctx)

        if isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.send(
                embed=disnake.Embed(description=f"{self.icons['error']} `{error}`"),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(
                embed=disnake.Embed(description=f"{self.icons['failed']} `{error}`"),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.ChannelNotReadable):
            await ctx.author.send(
                embed=disnake.Embed(
                    description=f"{self.icons['failed']} `No permissions to read channel's content`"
                ),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(
                embed=disnake.Embed(description=f"{self.icons['error']} `{error}`"),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.icons['failed']} `This command is on cooldown, try again after {round(error.retry_after)} seconds`"
                ),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.NoPrivateMessage):
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.icons['error']} `{error}`",
                ),
                delete_after=4,
            )

        elif isinstance(error, commands.errors.CommandInvokeError):
            if type(error.__cause__) is disnake.errors.Forbidden:
                await ctx.send(
                    embed=disnake.Embed(
                        description=f"{self.icons['failed']} `My role's hierarchy and/or permissions don't allow me to do so.`"
                    ),
                    delete_after=4,
                )

            elif type(error.__cause__) is disnake.errors.NotFound:
                pass

            else:
                await ctx.send(
                    embed=disnake.Embed(
                        description=f"{self.icons['error']} `An unknown error occured and the same has been reported to the team.`"
                    ),
                    delete_after=4,
                )
                print(
                    f"Ignoring exception in command {ctx.application_command.name}: ",
                    file=sys.stderr,
                )
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
                owner = await self.fetch_user(self.owned)
                await owner.send(
                    f"Ignoring exception in command {ctx.application_command.name}:\n{type(error.__cause__)}"
                )

        elif isinstance(error, NSFWChannel):
            await ctx.send(
                embed=disnake.Embed(description=f"{self.icons['failed']} `{error}`"),
                delete_after=4,
            )

        elif isinstance(error, NoNeko):
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.icons['failed']} `{error}`",
                ),
                delete_after=4,
            )
        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.icons['error']} `An unknown error occured and the same has been reported to the team.`"
                ),
                delete_after=4,
            )
            print(
                f"Ignoring exception in command {ctx.application_command.name}: ",
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )
            owner = await self.fetch_user(self.owned)
            await owner.send(
                f"Ignoring exception in command {ctx.application_command.name}:\n{error}\n{type(error)}\n{error.__traceback__.tb_frame.f_trace}"
            )
