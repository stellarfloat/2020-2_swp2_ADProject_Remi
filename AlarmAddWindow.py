import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

UI = uic.loadUiType("./ui/AlarmAddWindow.ui")[0]


class AlarmAddWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = AlarmAddWindow()

    myWindow.show()

    app.exec_()
