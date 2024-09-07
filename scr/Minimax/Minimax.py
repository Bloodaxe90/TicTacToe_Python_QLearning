import sys

import numpy as np
from PySide6.QtWidgets import QPushButton

from scr.Main.GameRules import GameRules
from scr.Main.TicTacToe import TicTacToe


class Minimax(TicTacToe):

    def __init__(self, game_controller) -> None:
        super().__init__(game_controller)
        self.maximiser: str = self.P2 #AI
        self.minimiser: str = self.P1 #Human

    def play(self, b :QPushButton) -> None:
         b.setText(self.minimiser)
         self.board = self.GAME_CONTROLLER.get_string_actual_board()
         if not self.check_game_over():
             best_move: tuple[int, int] = self.get_best_move(self.GAME_CONTROLLER.get_string_actual_board())
             self.GAME_CONTROLLER.actual_board[best_move].setText(self.maximiser)
             self.board = self.GAME_CONTROLLER.get_string_actual_board()
             self.check_game_over()


    def get_best_move(self, board: np.ndarray[(3, 3), np.dtype[str]]) -> tuple[int ,int]:
        best_score: int = -sys.maxsize -1
        best_action: tuple[int, int] = (-1, -1)

        for action in self.get_possible_actions():
                board[action] = self.maximiser
                score: int = self.minimax(board, 0, -sys.maxsize -1, sys.maxsize, False)
                board[action] = ""
                if score > best_score:
                    best_score = score                        
                    best_action = action

        return best_action


    def minimax(self, board: np.array, depth: int, alpha: int, beta: int, maximising: bool) -> int:
        result: str = GameRules.check_terminal(board)
        if result != "":
            if result == self.maximiser:
                return 100 - depth
            elif result == self.minimiser:
                return depth - 100
            return 0


        if maximising:
            best_score: int = -sys.maxsize -1
            for column in range(3):
                for row in range(3):
                    if board[column][row] == "":
                        board[column][row] = self.maximiser
                        score = self.minimax(board, depth +1, alpha, beta, False)
                        board[column][row] = ""
                        best_score = max(score, best_score)
                        alpha = max(best_score, alpha)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score: int = sys.maxsize
            for column in range(3):
                for row in range(3):
                    if board[column][row] == "":
                        board[column][row] = self.minimiser
                        score = self.minimax(board, depth +1, alpha, beta, True)
                        board[column][row] = ""
                        best_score = min(score, best_score)
                        beta = min(best_score, beta)
                        if beta <= alpha:
                            break
            return best_score


