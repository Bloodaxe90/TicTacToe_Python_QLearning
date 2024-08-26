
import numpy as np
from PySide6.QtWidgets import QPushButton


class GameRules:

    @classmethod
    def check_terminal(cls, board: np.array) -> str:
        for i in range(3):
            # Checking columns
            if cls.check_equal(board[i][0], board[i][1], board[i][2]):
                return board[i][0]

            # Checking rows
            if cls.check_equal(board[0][i], board[1][i], board[2][i]):
                return board[0][i]

        # Checking diagonals
        if (cls.check_equal(board[0][0], board[1][1], board[2][2]) or
                cls.check_equal(board[2][0], board[1][1], board[0][2])):
            return board[1][1]

        # Checking for draw
        counter = 0
        for b in board.flat:
            if b != "":
                counter += 1
        if counter == 9:
            return "D"

        return ""


    @classmethod
    def check_equal(cls, b1: str, b2: str, b3: str) -> bool:
        return b1 != "" and b1 == b2 == b3
