from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Slot

from scr.GameController import GameController


class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("/Users/eric/PycharmProjects/TicTacToe/UI/TicTacToe.ui")
        if not ui_file.open(QFile.ReadOnly):
            print(f"Failed to open file: {ui_file.errorString()}")
            return

        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.controller = GameController(self.ui)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.controller.key_pressed(event)


def main():
    app = QApplication([])
    window = Application()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
