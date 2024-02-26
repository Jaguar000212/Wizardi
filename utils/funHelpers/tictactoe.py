import disnake
from typing import List


class TicTacToeButton(disnake.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):

        super().__init__(style=disnake.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: disnake.Interaction):
        await interaction.response.defer()
        embed = disnake.Embed()
        embed.set_author(
            name=interaction.bot.user.display_name, icon_url=interaction.bot.user.avatar
        )
        embed.title = "Tic-Tac-Toe"
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        if view.player2.avatar is None:
            embed.set_footer(
                text=f"Challenged by {view.player2.display_name}",
                icon_url=view.player2.default_avatar.url,
            )
        else:
            embed.set_footer(
                text=f"Challenged by {view.player2.display_name}",
                icon_url=view.player2.avatar.url,
            )
        if view.current_player == view.X:

            if interaction.user == view.player1:
                self.style = disnake.ButtonStyle.danger
                self.emoji = f"{interaction.bot.icons['error']}"
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player2}```"
            elif interaction.user == view.player2:
                await interaction.send("This isn't your turn!", ephemeral=True)
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player1}```"
            else:
                await interaction.send("This isn't your game!", ephemeral=True)
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player1}```"
        else:

            if interaction.user == view.player2:
                self.style = disnake.ButtonStyle.success
                self.emoji = f"{interaction.bot.icons['online']}"
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                embed.description = f"`Challenger` - {view.player2.mention} 99kl)\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player1}```"

            elif interaction.user == view.player2:
                await interaction.send("This isn't your turn!", ephemeral=True)
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player2}```"
            else:
                await interaction.send("This isn't your game!", ephemeral=True)
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player2}```"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Winner - {view.player1}```"
            elif winner == view.O:
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Winner - {view.player2}```"
            else:
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- TIE```"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.edit_original_message(embed=embed, view=view)


class TicTacToe(disnake.ui.View):

    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1, player2):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None
