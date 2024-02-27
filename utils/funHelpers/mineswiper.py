from disnake import ui, ButtonStyle


class MineswiperButtons(ui.Button):
    """
    Represents a button used in a Minesweeper game.

    Attributes:
        ctx (Context): The context of the button.
        label (str): The label text of the button.
        custom_id (str): The custom ID of the button.
        bombs (list): The list of bomb positions in the game.
        board (list): The game board.

    Methods:
        callback(inter): Handles the button callback event.
    """

    def __init__(self, ctx, label, custom_id, bombs, board):
        super().__init__(label=label, style=ButtonStyle.grey, custom_id=custom_id)
        self.ctx = ctx
        self.bombs = bombs
        self.board = board

    async def callback(self, inter):
        """
        Callback method for handling button interactions in the Mineswiper game.

        Args:
            inter (discord.Interaction): The interaction object representing the button click.

        Returns:
            None
        """
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
                """
                Check the neighboring positions of a given position on the board.

                Args:
                    count (list): The list to store the neighboring positions.
                    rawpos (int): The raw position on the board.
                    pos (int): The processed position on the board.

                Returns:
                    list: The updated list of neighboring positions.
                """
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
    """
    Represents the view for the Minesweeper game.
    """

    def __init__(self, ctx, options, bombs, board):
        super().__init__()
        for i, op in enumerate(options):
            self.add_item(MineswiperButtons(ctx, op, f"block{i}", bombs, board))
        self.board = board
        self.bombs = bombs
        self.moves = []
        self.ctx = ctx

    async def EndGame(self):
        """
        Ends the game and displays a message indicating that the player has won.
        Disables all buttons and reveals the positions of the bombs on the game board.
        """
        await self.ctx.edit_original_message(content="Game Ended. You won!")
        for button in self.children:
            button.disabled = True
            pos = int(button.custom_id[5:])
            if pos in self.bombs:
                button.label = "💣"
                button.style = ButtonStyle.red
                self.board[self.GetBoardRow(pos)][self.GetBoardPos(pos)] = "💣"

    @staticmethod
    def GetBoardRow(pos):
        """
        Returns the row number of a given position on the board.

        Args:
            pos (int): The position on the board.

        Returns:
            int: The row number of the position.

        Raises:
            None

        Examples:
            >>> GetBoardRow(0)
            0
            >>> GetBoardRow(10)
            2
            >>> GetBoardRow(24)
            4
        """
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

    @staticmethod
    def GetBoardPos(pos):
        """
        Returns the board position index based on the given position.

        Parameters:
        pos (int): The position value.

        Returns:
        int or False: The board position index if pos is valid, False otherwise.
        """
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
        """
        Reveal the bombs on the game board.

        Args:
            b_id (str): The ID of the button that triggered the bomb reveal.
            board (list): The game board containing the positions of the bombs.

        Returns:
            None
        """
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
