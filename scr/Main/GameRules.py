
import numpy as np


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
        if cls.check_full(board):
            return "D"

        return ""


    @classmethod
    def check_full(cls, board: np.array) -> bool:
        return all(value != "" for value in board.flat)


    @classmethod
    def check_equal(cls, v1: str, v2: str, v3: str) -> bool:
        return v1 != "" and v1 == v2 == v3
