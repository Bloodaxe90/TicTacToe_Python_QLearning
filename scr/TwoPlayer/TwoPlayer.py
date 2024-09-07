from PySide6.QtWidgets import QPushButton

from scr.Main.TicTacToe import TicTacToe


class TwoPlayer(TicTacToe):
    def __init__(self, game_controller) -> None:
        super().__init__(game_controller)
        self.current_player: str = self.P1

    def play(self, b: QPushButton) -> None:
        b.setText(self.current_player)
        self.update_board_as_actual_board()
        if not self.check_game_over():
            self.change_current_player()

    def change_current_player(self) -> None:
        if self.current_player == self.P1:
            self.current_player = self.P2
        else:
            self.current_player = self.P1


