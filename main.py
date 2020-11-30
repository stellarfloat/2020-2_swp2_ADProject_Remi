import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import time

UI = uic.loadUiType("./ui/MainWindow.ui")[0]


class MainWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Timer = QtCore.QTimer(self)
        self.Timer.setInterval(1000) # every 1 seconds

        self.Timer.timeout.connect(self.timer_handler)

    def timer_handler(self):
        current_time = time.localtime()

        self.CurrentTime.setText(time.strftime("%p %I:%M:%S"))

        print(int(time.mktime(current_time)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = MainWindow()

    myWindow.show()
    myWindow.Timer.start()

    app.exec_()
