import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

UI = uic.loadUiType("./ui/AlarmListWindow.ui")[0]


class AlarmListWindow(QDialog, UI):
    def __init__(self, parent=None):
        super(AlarmListWindow, self).__init__(parent)

        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = AlarmListWindow()

    myWindow.show()

    app.exec_()
