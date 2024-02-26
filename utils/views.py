import disnake

from utils.helpers import BotInformation


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
            self.bot.logger.error(f"Failed to edit message: {e}")
            return
