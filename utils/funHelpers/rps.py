from random import choice
import disnake

from bot import Bot


class RPS(disnake.ui.View):
    def __init__(self, bot: Bot, challenger: disnake.Member, opponent: disnake.Member):
        super().__init__(timeout=30)
        self.bot = bot
        self.challenger = challenger
        self.opponent = opponent
        self.opponentOP = None
        self.challengerOP = None
        if opponent.bot:
            self.opponentOP = choice(["Rock", "Paper", "Scissors"])

    @disnake.ui.button(label="Rock", emoji="🪨")
    async def rock(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embed = self.bot.Embed(interaction.bot, interaction, "Challenged")
        embed.title = "Rock-Paper-Scissors"
        if self.challenger.avatar is None:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.default_avatar.url,
            )
        else:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.avatar.url,
            )
        await interaction.response.defer()
        if not interaction.user in [self.challenger, self.opponent]:
            await interaction.send("This isn't your game!", ephemeral=True)
        else:
            if interaction.user == self.opponent:
                self.opponentOP = "Rock"
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.opponent} is ready```"
            else:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.challenger} is ready```"
                self.challengerOP = "Rock"
        if not self.challengerOP is None and not self.opponentOP is None:
            winner = self.winner()
            for button in self.children:
                button.disabled = True
            await interaction.edit_original_message(view=self)
            if winner:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {winner[0]} won!! Chose {winner[1]}```"
            else:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- DRAW```"
        await interaction.edit_original_message(embed=embed)

    @disnake.ui.button(label="Paper", emoji="🧻")
    async def paper(self, button, interaction):
        embed = self.bot.Embed(interaction.bot, interaction, "Challenged")
        embed.title = "Rock-Paper-Scissors"
        embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}"
        if self.challenger.avatar is None:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.default_avatar.url,
            )
        else:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.avatar.url,
            )
        await interaction.response.defer()
        if not interaction.user in [self.challenger, self.opponent]:
            await interaction.send("This isn't your game!", ephemeral=True)
        else:
            if interaction.user == self.opponent:
                self.opponentOP = "Paper"
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.opponent} is ready```"
            else:
                self.challengerOP = "Paper"
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.challenger} is ready```"
        if not self.challengerOP is None and not self.opponentOP is None:
            winner = self.winner()
            for button in self.children:
                button.disabled = True
            await interaction.edit_original_message(view=self)
            if winner:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {winner[0]} won!! Chose {winner[1]}```"
            else:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- DRAW```"
        await interaction.edit_original_message(embed=embed)

    @disnake.ui.button(label="Scissors", emoji="✂️")
    async def scissors(self, button, interaction):
        embed = self.bot.Embed(interaction.bot, interaction, "Challenged")
        embed.title = "Rock-Paper-Scissors"
        embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}"
        if self.challenger.avatar is None:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.default_avatar.url,
            )
        else:
            embed.set_footer(
                text=f"Challenged by {self.challenger.display_name}",
                icon_url=self.challenger.avatar.url,
            )
        await interaction.response.defer()
        if not interaction.user in [self.challenger, self.opponent]:
            await interaction.send("This isn't your game!", ephemeral=True)
        else:
            if interaction.user == self.opponent:
                self.opponentOP = "Scissors"
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.opponent} is ready```"
            else:
                self.challengerOP = "Scissors"
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {self.challenger} is ready```"
        if not self.challengerOP is None and not self.opponentOP is None:
            winner = self.winner()
            for button in self.children:
                button.disabled = True
            await interaction.edit_original_message(view=self)
            if winner:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- {winner[0]} won!! Chose {winner[1]}```"
            else:
                embed.description = f"`Challenger` - {self.challenger.mention}\n`Opponent` - {self.opponent.mention}\n\n```diff\n- DRAW```"
        await interaction.edit_original_message(embed=embed)

    def winner(self):
        if self.challengerOP == self.opponentOP:
            return False
        elif self.challengerOP == "Rock":
            if self.opponentOP == "Paper":
                return (self.opponent, self.opponentOP)
            elif self.opponentOP == "Scissors":
                return (self.challenger, self.challengerOP)
        elif self.challengerOP == "Paper":
            if self.opponentOP == "Scissors":
                return (self.opponent, self.opponentOP)
            elif self.opponentOP == "Rock":
                return (self.challenger, self.challengerOP)
        elif self.challengerOP == "Scissors":
            if self.opponentOP == "Rock":
                return (self.opponent, self.opponentOP)
            elif self.opponentOP == "Paper":
                return (self.challenger, self.challengerOP)
