import numpy as np
from PySide6.QtCore import Slot, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QPushButton, QLabel

from scr.GameRules import GameRules
from scr.Minimax import Minimax
from scr.TwoPlayer import TwoPlayer


class GameController(QObject):

    def __init__(self, view) -> None:
        super().__init__()
        self.view = view

        self.board: np.array = self.set_up_board()
        self.terminal_label = self.set_up_terminal_label()

        self.player1: str = "X"
        self.player2: str = "O"

        self.two_player = TwoPlayer(self, self.player1, self.player2)
        self.play_minimax = Minimax(self, self.player1, self.player2)

        self.stop = False

    @Slot()
    def button_clicked(self) -> None:
        if not self.stop:
            sender = self.sender()
            if isinstance(sender, QPushButton):
                if sender.text() == "":
                    #2 Player mode
                    #self.two_player.play(sender)

                    #vs AI
                    self.play_minimax.play(sender)

    def key_pressed(self, event: QKeyEvent) -> None:
        if event.key() == 32:
            self.reset()


    def place_piece(self):
        pass

    def game_over(self, result: str) -> None:
        self.stop = True
        if result == self.player1:
            self.terminal_label.setText(f"{self.player1.upper()} WINS!")
        elif result == self.player2:
            self.terminal_label.setText(f"{self.player2.upper()} WINS!")
        else:
            self.terminal_label.setText(f"DRAW")
        self.terminal_label.setVisible(True)


    def clear_board(self) -> None:
        for b in self.board.flat:
            b.setText("")

    def check_game_over(self) -> bool:
        result: str = GameRules.check_terminal(self.get_string_board())
        if result != "":
            self.game_over(result)
            return True
        return False

    def get_string_board(self) -> np.array:
        board: np.array = np.empty((3,3), dtype=str)
        for column in range(3):
            for row in range(3):
                board[column][row] = self.board[column][row].text()
        return board

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
        , dtype=QPushButton)
        self.set_up_board_connections(board)
        return board


    def set_up_board_connections(self, board: np.array) -> None:
        for button in board.flat:
            if button:
                button.clicked.connect(self.button_clicked)
            else:
                print("Not a button")


    def reset(self) -> None:
        self.two_player.reset()
        self.clear_board()

        self.terminal_label.setVisible(False)
        self.stop = False











