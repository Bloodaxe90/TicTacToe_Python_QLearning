
import numpy as np
from PySide6.QtWidgets import QPushButton


class GameRules:

    @classmethod
    def check_win(cls, board: np.array) -> bool:

        for i in range(3):
                #checking columns
            if (cls.check_equal(board[i][0], board[i][1], board[i][2]) or
                #checking rows
                cls.check_equal(board[0][i], board[1][i], board[2][i])):
                return True

        #checking diagonals
        if (cls.check_equal(board[0][0], board[1][1], board[2][2]) or
            cls.check_equal(board[2][0], board[1][1], board[0][2])):
            return True

        return False

    @classmethod
    def check_draw(cls, board: np.array) -> bool:
        for button in board.flat:
            if button.text() == "":
                return False
        return True

    @classmethod
    def check_equal(cls, b1: QPushButton, b2: QPushButton, b3: QPushButton) -> bool:
        return b1.text() != "" and b1.text() == b2.text() == b3.text()
