from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("ARBF")
        self.setGeometry(300, 250, 350, 200)

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Тут должно будет что-то написано")
        self.main_text.move(70, 100)
        self.main_text.adjustSize()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(120, 150)
        self.btn.setText("Нажми на меня!")
        self.btn.adjustSize()
        self.btn.clicked.connect(self.add_label)
    def add_label(self):
        print("Здарова!")

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()
