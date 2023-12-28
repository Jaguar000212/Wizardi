from itertools import repeat
from random import *

from disnake import *
import disnake
import random
from typing import List
from bot import Bot


class MineswiperButtons(ui.Button):
    def __init__(self, ctx, label, custom_id, bombs, board):
        super().__init__(label=label, style=ButtonStyle.grey, custom_id=custom_id)
        self.ctx = ctx
        self.bombs = bombs
        self.board = board

    async def callback(self, inter):
        assert self.view is not None
        view: MineswiperView = self.view
        await inter.response.defer()
        if inter.author.id != self.ctx.author.id:
            return await inter.send(
                "You cannot interact with these buttons.", ephemeral=True
            )

        b_id = self.custom_id
        if int(b_id[5:]) in view.moves:
            return await inter.send("That part is already taken.", ephemeral=True)
        if int(b_id[5:]) in self.bombs:
            await view.RevealBombs(b_id, view.board)
        else:
            count = []
            rawpos = int(b_id[5:])
            pos = view.GetBoardPos(rawpos)

            def checkpos(count, rawpos, pos):
                pos = view.GetBoardPos(rawpos)
                if not rawpos - 1 in self.bombs or pos == 0:
                    count.append(rawpos - 1)
                if not rawpos + 1 in self.bombs or pos == 4:
                    count.append(rawpos + 1)
                if not rawpos - 6 in self.bombs or pos == 0:
                    count.append(rawpos - 6)
                if not rawpos - 4 in self.bombs or pos == 4:
                    count.append(rawpos - 4)
                if not rawpos + 6 in self.bombs or pos == 4:
                    count.append(rawpos + 6)
                if not rawpos + 4 in self.bombs or pos == 0:
                    count.append(rawpos + 4)
                if not rawpos - 5 in self.bombs:
                    count.append(rawpos - 5)
                if not rawpos + 5 in self.bombs:
                    count.append(rawpos + 5)
                return count

            count = checkpos(count, rawpos, pos)
            self.label = f"  {8-len(count)}  "
            self.style = ButtonStyle.green
            pos = int(b_id[5:])
            view.board[view.GetBoardRow(pos)][
                view.GetBoardPos(pos)
            ] = f"  {8-len(count)}  "
            view.moves.append(pos)
            if len(view.moves) + len(self.bombs) == 25:
                await inter.edit_original_message(view=view)
                await view.EndGame()

        await inter.edit_original_message(view=view)


class MineswiperView(ui.View):
    def __init__(self, ctx, options, bombs, board):
        super().__init__()
        for i, op in enumerate(options):
            self.add_item(MineswiperButtons(ctx, op, f"block{i}", bombs, board))
        self.board = board
        self.bombs = bombs
        self.moves = []
        self.ctx = ctx

    async def EndGame(self):
        await self.ctx.edit_original_message(content="Game Ended. You won!")
        for button in self.children:
            button.disabled = True
            pos = int(button.custom_id[5:])
            if pos in self.bombs:
                button.label = "💣"
                button.style = ButtonStyle.red
                self.board[self.GetBoardRow(pos)][self.GetBoardPos(pos)] = "💣"

    def GetBoardRow(self, pos):
        if pos in [0, 1, 2, 3, 4]:
            return 0
        if pos in [5, 6, 7, 8, 9]:
            return 1
        if pos in [10, 11, 12, 13, 14]:
            return 2
        if pos in [15, 16, 17, 18, 19]:
            return 3
        if pos in [20, 21, 22, 23, 24]:
            return 4
        return False

    def GetBoardPos(self, pos):
        if pos in [0, 1, 2, 3, 4]:
            return pos
        if pos in [5, 6, 7, 8, 9]:
            for i, num in enumerate(range(5, 10)):
                if pos == num:
                    return i
        if pos in [10, 11, 12, 13, 14]:
            for i, num in enumerate(range(10, 15)):
                if pos == num:
                    return i
        if pos in [15, 16, 17, 18, 19]:
            for i, num in enumerate(range(15, 20)):
                if pos == num:
                    return i
        if pos in [20, 21, 22, 23, 24]:
            for i, num in enumerate(range(20, 25)):
                if pos == num:
                    return i
        return False

    async def RevealBombs(self, b_id, board):
        bombemo = "💣"
        for button in self.children:
            button.disabled = True
            if button.custom_id == b_id:
                button.label = bombemo
                button.style = ButtonStyle.red
                pos = int(b_id[5:])
                self.board[self.GetBoardRow(pos)][self.GetBoardPos(pos)] = bombemo

        for button in self.children:
            if int(button.custom_id[5:]) in self.bombs:
                button.label = bombemo
                button.style = ButtonStyle.red
                self.board[self.GetBoardRow(int(b_id[5:]))][
                    self.GetBoardPos(int(b_id[5:]))
                ] = bombemo


class RPS(disnake.ui.View):
    def __init__(self, bot: Bot, challenger: disnake.Member, opponent: disnake.Member):
        super().__init__(timeout=30)
        self.bot = bot
        self.challenger = challenger
        self.opponent = opponent
        self.opponentOP = None
        self.challengerOP = None
        if opponent.bot:
            self.opponentOP = random.choice(["Rock", "Paper", "Scissors"])

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
                await interaction.send(
                    "This isn't your turn!", ephemeral=True
                )
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player1}```"
            else:
                await interaction.send(
                    "This isn't your game!", ephemeral=True
                )
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
                await interaction.send(
                    "This isn't your turn!", ephemeral=True
                )
                embed.description = f"`Challenger` - {view.player2.mention} ({interaction.bot.icons['online']})\n`Opponent` - {view.player1.mention} ({interaction.bot.icons['error']})\n\n```diff\n- Current Turn - {view.player2}```"
            else:
                await interaction.send(
                    "This isn't your game!", ephemeral=True
                )
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
