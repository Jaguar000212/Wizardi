import disnake
from disnake.ext import commands
import datetime as dt
from disnake.ext.commands.params import Param
import sys

from utils.exceptions import NSFWChannel
from utils.helpers import BotInformationView, CogEmoji
from bot import Bot


class Help(commands.Cog):
    """Provides help commands for the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(description="Displays help information.")
    async def help(
        self,
        ctx: disnake.AppCmdInter,
        name: str = Param(None, description="Command or module"),
    ):
        """
        Displays help information.

        Parameters:
        - ctx (disnake.AppCmdInter): The interaction context.
        - name (str, optional): The name of the command or module to get help for. Defaults to None.
        """
        await ctx.response.defer()
        input = name
        if input is None:
            modules = ""
            menu = disnake.ui.Select(placeholder="Select a module")
            view = disnake.ui.View(timeout=15)
            view.add_item(item=menu)
            embed = disnake.Embed(
                title="Welcome :tada:",
                description=f"Heya! {ctx.author.mention}. Welcome to **{self.bot.user.display_name}**, a helper bot with some useful commands!\n\nThis is the Help Desk for Wizardi.\nAlso, try `/info` for bot's information.",
                color=14667786,
            )
            embed.set_author(
                name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
            )
            embed.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            for cog in self.bot.cogs:
                if cog in ("Listeners", "Help"):
                    continue
                modules += f"> \{CogEmoji[cog]} **{cog}**\n"
                cogs = self.bot.get_cog(cog)
                menu.add_option(
                    label=cog, description=cogs.description, emoji=CogEmoji[cog]
                )

            embed.add_field(name="Modules :-", value=modules)

            async def callback(interaction):
                if interaction.user != ctx.author:
                    await interaction.response.send_message(
                        "This isn't requested by you!", ephemeral=True
                    )
                else:
                    await interaction.response.defer()
                    input = interaction.values[0]
                    cogs = self.bot.get_cog(input.capitalize())
                    embed = disnake.Embed(
                        title=f"\{CogEmoji[cogs.qualified_name]} {cogs.qualified_name}",
                        description="Commands belonging this module -",
                        color=14667786,
                    )
                    embed.set_author(
                        name=self.bot.user.display_name,
                        icon_url=self.bot.user.avatar.url,
                    )
                    embed.set_footer(
                        text=f"Requested by {ctx.author.display_name}",
                        icon_url=ctx.author.display_avatar.url,
                    )

                    if cogs.qualified_name == "Nsfw":
                        if not ctx.channel.is_nsfw():
                            embed.add_field(
                                name="NSFW Module",
                                value="Only available in NSFW channels.",
                            )
                        else:
                            for command in cogs.get_slash_commands():
                                embed.add_field(
                                    name=f"**{command.name}**",
                                    value=f"> {command.description}",
                                    inline=False,
                                )
                    else:
                        for command in cogs.get_slash_commands():
                            embed.add_field(
                                name=f"**{command.name}**",
                                value=f"> {command.description}",
                                inline=False,
                            )
                    await ctx.edit_original_message(embed=embed)

            async def on_timeout(self=view):
                for button in self.children:
                    button.disabled = True
                await ctx.edit_original_message(view=view)

            menu.callback = callback
            view.timeout = 15
            view.on_timeout = on_timeout
            await ctx.send(embed=embed, view=view)
        else:
            if input.capitalize() in self.bot.cogs:
                cogs = self.bot.get_cog(input.capitalize())
                embed = disnake.Embed(
                    title=f"\{CogEmoji[cogs.qualified_name]} {cogs.qualified_name}",
                    description="Commands belonging this module -",
                    color=14667786,
                )
                embed.set_author(
                    name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url
                )
                embed.set_footer(
                    text=f"Requested by {ctx.author.display_name}",
                    icon_url=ctx.author.display_avatar.url,
                )
                if cogs.qualified_name == "Nsfw":
                    if not ctx.channel.is_nsfw():
                        raise NSFWChannel("Only available in NSFW channels.")
                    for command in cogs.get_slash_commands():
                        embed.add_field(
                            name=f"**/{command.body.name}**",
                            value=f"> {command.body.description}",
                            inline=False,
                        )
                else:
                    for command in cogs.get_slash_commands():
                        embed.add_field(
                            name=f"**/{command.body.name}**",
                            value=f"> {command.body.description}",
                            inline=False,
                        )
                await ctx.send(embed=embed)
            elif any(
                input.lower() == command.name for command in self.bot.slash_commands
            ):
                for command in self.bot.slash_commands:
                    if command.name == input.lower():
                        try:
                            embed = disnake.Embed(title="Command Help", color=14667786)
                            embed.set_author(
                                name=self.bot.user.display_name,
                                icon_url=self.bot.user.avatar.url,
                            )
                            embed.set_footer(
                                text=f"Requested by {ctx.author.display_name}",
                                icon_url=ctx.author.display_avatar.url,
                            )
                            for cmd in (command.all_commands).values():
                                embed.add_field(
                                    name=cmd.qualified_name, value=cmd.description
                                )
                        except AttributeError:
                            embed = disnake.Embed(
                                title="Command Help",
                                description=f"`{command.name}` - {command.description}",
                                color=14667786,
                            )
                            embed.set_author(
                                name=self.bot.user.display_name,
                                icon_url=self.bot.user.avatar.url,
                            )
                            embed.set_footer(
                                text=f"Requested by {ctx.author.display_name}",
                                icon_url=ctx.author.display_avatar.url,
                            )
                        await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    description=f"I've never heard from a module/command called `{input}` before",
                    color=14667786,
                )
                await ctx.send(embed=embed, delete_after=4)

    @commands.slash_command(
        name="info-bot", description="Shows information about the bot."
    )
    async def about(self, interaction: disnake.ApplicationCommandInteraction):
        """
        Shows information about the bot.

        Parameters:
        - interaction (disnake.ApplicationCommandInteraction): The interaction context.
        """
        await interaction.response.defer()
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
            icon_url="https://github.com/DisnakeDev/disnake/blob/master/docs/images/disnake_logo.ico?raw=True",
        )

        await interaction.edit_original_message(
            embed=embed,
            view=BotInformationView(bot=self.bot, interaction=interaction),
        )


def setup(bot):
    bot.add_cog(Help(bot))
