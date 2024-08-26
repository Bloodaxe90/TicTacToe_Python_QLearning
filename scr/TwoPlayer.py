from PySide6.QtWidgets import QPushButton

class TwoPlayer:
    def __init__(self, game_controller, player1: str, player2: str) -> None:
        self.game_controller = game_controller
        self.player1: str = player1
        self.player2: str = player2
        self.current_player: str = self.player1

    def play(self, b: QPushButton) -> None:
        b.setText(self.current_player)
        if not self.game_controller.check_game_over():
            self.change_current_player()


    def change_current_player(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def reset(self) -> None:
        self.current_player = self.player1

