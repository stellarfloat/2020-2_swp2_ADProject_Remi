import sys

from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import *
from PyQt5 import uic

UI = uic.loadUiType("./ui/AlarmAddWindow.ui")[0]


class AlarmAddWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.AlarmTime.setTime(QTime.currentTime())
        self.AlarmDate.setDate(QDate.currentDate())

        self.addButton.clicked.connect(self.addBtnClicked)

    def addBtnClicked(self):
        print(self.AlarmTime.time().toString())
        print(self.AlarmDate.date().toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = AlarmAddWindow()

    myWindow.show()

    app.exec_()
