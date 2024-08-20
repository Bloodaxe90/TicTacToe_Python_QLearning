import numpy as np
from PySide6.QtCore import Slot, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QPushButton, QLabel

from scr.GameRules import GameRules


class GameController(QObject):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.board: np.array = self.set_up_board()
        self.terminal_label = self.set_up_terminal_label()

        self.player1: str = "X"
        self.player2: str = "O"
        self.current_player: str = self.player1
        self.stop = False

    @Slot()
    def button_clicked(self) -> None:
        if not self.stop:
            sender = self.sender()
            if isinstance(sender, QPushButton):
                self.play_2_player(sender)


    def key_pressed(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.reset()


    def play_2_player(self, b: QPushButton) -> None:
        if b.text() == "":
            b.setText(self.current_player)
            result: str = self.check_terminal()
            if result is not None:
                self.game_over(result)
            else:
                self.change_current_player()



    def change_current_player(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def check_terminal(self) -> str:
        if GameRules.check_win(self.board):
            return "W"
        elif GameRules.check_draw(self.board):
            return "D"
        #Return None

    def game_over(self, result: str) -> None:
        self.stop = True
        if result == "W":
            self.terminal_label.setText(f"{self.current_player.upper()} WINS!")
        else:
            self.terminal_label.setText(f"DRAW")
        self.terminal_label.setVisible(True)


    def clear_board(self) -> None:
        for b in self.board.flat:
            b.setText("")


    def set_up_terminal_label(self) -> QLabel:
        terminal_label = self.view.findChild(QLabel, "TerminalLabel")
        terminal_label.setVisible(False)
        terminal_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        return terminal_label

    def set_up_board(self) -> np.array:
        board = np.array(
            [
                [self.view.findChild(QPushButton, f'b{i * 3 + j + 1}') for j in range(3)]
                for i in range(3)
            ]
        )
        self.set_up_board_connections(board)
        return board


    def set_up_board_connections(self, board: np.array) -> None:
        for button in board.flat:
            if button:
                button.clicked.connect(self.button_clicked)
            else:
                print("Not a button")


    def reset(self):
        self.current_player = self.player1
        self.clear_board()

        self.terminal_label.setVisible(False)
        self.stop = False











