import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

UI = uic.loadUiType("./ui/MainWindow.ui")[0]


class MainWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = MainWindow()

    myWindow.show()

    app.exec_()
