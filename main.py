import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import time

from AlarmAddWindow import AlarmAddWindow
from AlarmListWindow import AlarmListWindow
from AlarmWindow import AlarmWindow
from ScheduleManager import ScheduleManager

UI = uic.loadUiType("./ui/MainWindow.ui")[0]


class MainWindow(QMainWindow, UI):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.ScheduleManager = ScheduleManager()

        self.Timer = QtCore.QTimer(self)
        self.Timer.setInterval(1000)  # every 1 seconds

        self.Timer.timeout.connect(self.timer_handler)

        self.AddAlarm.triggered.connect(self.alarm_add_handler)
        self.ListAlarm.triggered.connect(self.alarm_list_handler)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ScheduleManager.save()

    def timer_handler(self):
        current_time = time.localtime()

        self.CurrentTime.setText(time.strftime("%p %I:%M:%S"))

        schedules = self.ScheduleManager.get_schedules(int(time.mktime(current_time)))

        if len(schedules) > 0:
            for i in schedules:
                alarm_window = AlarmWindow(i, self)

                alarm_window.show()

    def alarm_add_handler(self):
        try:
            add_window = AlarmAddWindow(self)
            add_window.show()

            self.statusbar.showMessage("알림 추가 창을 열었습니다.")
        except Exception as E:
            print(E)

    def alarm_list_handler(self):
        try:
            list_window = AlarmListWindow(self)
            list_window.show()

            self.statusbar.showMessage("알림 목록 창을 열었습니다.")
        except Exception as E:
            print(E)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = MainWindow()

    myWindow.show()
    myWindow.Timer.start()

    app.exec_()
