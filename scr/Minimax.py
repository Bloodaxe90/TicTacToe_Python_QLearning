import sys

import numpy as np
from PySide6.QtWidgets import QPushButton

from scr.GameRules import GameRules


class Minimax:

    def __init__(self, game_controller, player1: str, player2: str) -> None:
        self.game_controller = game_controller
        self.maximiser: str = player1
        self.minimiser: str = player2
        pass

    def play(self, b :QPushButton) -> None:
         b.setText(self.maximiser)
         if not self.game_controller.check_game_over():
             best_moves: tuple = self.get_best_move(self.game_controller.get_string_board())
             self.game_controller.board[best_moves[0]][best_moves[1]].setText(self.minimiser)



    def get_best_move(self, board: np.ndarray[(3, 3), np.dtype[str]]) -> tuple[int ,int]:
        best_score: int = -sys.maxsize -1
        best_column: int = -1
        best_row: int = -1

        for column in range(3):
            for row in range(3):
                if board[column][row] == "":
                    board[column][row] = self.maximiser
                    score: int = self.minimax(board, 0, False)
                    board[column][row] = ""
                    if score > best_score:
                        best_score = score
                        best_column = column
                        best_row = row

        return best_column, best_row


    def minimax(self, board: np.array, depth: int, maximising: bool) -> int:

        result: str = GameRules.check_terminal(board)
        if result != "":
            if result == self.maximiser:
                return 10 - depth
            elif result == self.minimiser:
                return depth - 10
            return 0


        if maximising:
            best_score: int = -sys.maxsize -1
            for column in range(3):
                for row in range(3):
                    if board[column][row] == "":
                        board[column][row] = self.maximiser
                        score = self.minimax(board, depth +1, False)
                        board[column][row] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score: int = sys.maxsize
            for column in range(3):
                for row in range(3):
                    if board[column][row] == "":
                        board[column][row] = self.minimiser
                        score = self.minimax(board, depth +1, True)
                        board[column][row] = ""
                        best_score = min(score, best_score)
            return best_score


