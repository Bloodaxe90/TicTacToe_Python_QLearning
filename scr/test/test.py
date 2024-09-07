from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Slot


class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("/Resources/UI/TicTacToe.ui")
        if not ui_file.open(QFile.ReadOnly):
            print(f"Failed to open file: {ui_file.errorString()}")
            return

        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.b2 = self.ui.findChild(QPushButton, 'b2')
        print(type(self.b2))
        if self.b2:
            self.b2.pressed.connect(self.button_pressed)
        else:
            print("Button b2 not found")


    @Slot()
    def button_pressed(self) -> None:
        print(self.sender().objectName())

if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    window.show()
    app.exec()