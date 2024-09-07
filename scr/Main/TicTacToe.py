import random

import numpy as np

from scr.Main.GameRules import GameRules


class TicTacToe:

    def __init__(self, game_controller, player1: str= "X", player2: str= "O"):
        self.GAME_CONTROLLER = game_controller
        self.ACTIONS: list[tuple[int, int]] = [(col, row) for col in range(3) for row in range(3)]
        self.board = np.empty((3, 3), dtype=str)

        self.P1: str = player1
        self.P2: str = player2

    def make_move(self, player: int, action: tuple[int, int]) -> None:
        self.board[action] = player

    def check_game_over(self) -> bool:
        result: str = GameRules.check_terminal(self.board)
        if result != "":
            self.GAME_CONTROLLER.game_over(result, self.P1, self.P2)
            return True
        return False

    def update_board_as_actual_board(self) -> None:
        self.board = self.GAME_CONTROLLER.get_string_actual_board()

    def get_possible_actions(self, board: np.array = None) -> list[tuple[int, int]]:
        if board is None:
            board = self.board
        return [action for action in self.ACTIONS if board[action] == ""]

    def get_random_action(self, board: np.array = None) -> tuple[int, int]:
        return random.choice(self.get_possible_actions(board))