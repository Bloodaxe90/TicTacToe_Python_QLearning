
import numpy as np
from PySide6.QtCore import Slot, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QPushButton, QLabel, QRadioButton, QLineEdit

from scr.Minimax.Minimax import Minimax
from scr.QLearning.QLearning import QLearning
from scr.TwoPlayer.TwoPlayer import TwoPlayer


class GameController(QObject):

    def __init__(self, view) -> None:
        super().__init__()
        self.view = view

        self.actual_board: np.array = None
        self.terminal_label = None
        self.play_2player_radio_button = None
        self.play_minimax_radio_button = None
        self.play_q_learned_ai_radio_button = None
        self.episode_number_line_edit = None
        self.train_button = None

        self.two_player = TwoPlayer(self)
        self.play_minimax = Minimax(self)
        self.q_learning = QLearning(self)

        #Initialising the game components and connecting relevant signals and slots
        self.set_up_game()

        self.stop = False

    @Slot()
    def button_clicked(self) -> None:
        sender = self.sender()
        if not self.stop and isinstance(sender, QPushButton):
            if sender in self.actual_board and sender.text() == "":
                if self.play_2player_radio_button.isChecked():
                    # 2 Player mode
                    self.two_player.play(sender)
                elif self.play_minimax_radio_button.isChecked():
                    # Verse Minimax Ai
                    self.play_minimax.play(sender)
                elif self.play_q_learned_ai_radio_button.isChecked():
                    # Verse Q Learned AI
                    self.q_learning.play(sender)
            elif sender == self.train_button:
                if isinstance(self.episode_number_line_edit.text(), int):
                    self.q_learning.MAX_EPISODES = self.episode_number_line_edit.text()
                self.terminal_label.setText("TRAINING")
                self.terminal_label.setVisible(True)
                self.q_learning.train()
                self.terminal_label.setVisible(False)


    @Slot()
    def key_pressed(self, event: QKeyEvent) -> None:
        match event.key():
            case 32: self.reset() #(Space)
            case 83: self.q_learning.save_policies() #(S)
            case 76: self.q_learning.load_policies() #(L)
            case 84: self.q_learning.load_policies(True) #(T)
            case 82: self.q_learning.reset_q_tables() #(R)


    def game_over(self, result: str, player1: str, player2: str) -> None:
        self.stop = True
        if result == player1:
            self.terminal_label.setText(f"{player1.upper()} WINS!")
        elif result == player2:
            self.terminal_label.setText(f"{player2.upper()} WINS!")
        else:
            self.terminal_label.setText(f"DRAW")
        self.terminal_label.setVisible(True)

    def get_string_actual_board(self) -> np.array:
        return np.vectorize(lambda btn: btn.text())(self.actual_board)

    def clear_board(self) -> None:
        for b in self.actual_board.flat:
            b.setText("")


    def set_up_game(self):
        self.set_up_board()
        self.set_up_terminal_label()
        self.set_up_option_buttons()


    def set_up_board(self) -> None:
        board = np.array(
            [
                [self.view.findChild(QPushButton, f'b{i * 3 + j + 1}') for j in range(3)]
                for i in range(3)
            ]
        , dtype=QPushButton)
        self.set_up_board_connections(board)
        self.actual_board = board


    def set_up_board_connections(self, board: np.array) -> None:
        for button in board.flat:
            if button:
                button.clicked.connect(self.button_clicked)
            else:
                print("Not a button")


    def set_up_terminal_label(self) -> None:
        terminal_label = self.view.findChild(QLabel, "TerminalLabel")
        terminal_label.setVisible(False)
        terminal_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.terminal_label = terminal_label


    def set_up_option_buttons(self):
        self.train_button = self.view.findChild(QPushButton, "train")
        self.episode_number_line_edit = self.view.findChild(QLineEdit, "episodeLineEdit")
        self.play_2player_radio_button = self.view.findChild(QRadioButton, "twoPlayerRadioButton")
        self.play_minimax_radio_button = self.view.findChild(QRadioButton, "minimaxRadioButton")
        self.play_q_learned_ai_radio_button = self.view.findChild(QRadioButton, "qLearningAiRadioButton")

        self.train_button.clicked.connect(self.button_clicked)


    def reset(self) -> None:
        self.two_player = TwoPlayer(self)
        self.clear_board()

        self.terminal_label.setVisible(False)
        self.stop = False











