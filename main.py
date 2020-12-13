import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import time

from AlarmAddWindow import AlarmAddWindow
from AlarmNLAddWindow import AlarmNLAddWindow
from AlarmWindow import AlarmWindow
from ScheduleManager import ScheduleManager
from AlarmWidget import AlarmWidget

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
        self.AddNLAlarm.triggered.connect(self.alarmNL_add_handler)

        self.AddAlarmButton.clicked.connect(self.alarm_add_handler)

        self.get_contents()
        self.get_time_contents()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ScheduleManager.save()

    def get_contents(self):
        for i in range(self.AlarmList.count()):
            try:
                self.AlarmList.itemAt(i).widget().deleteLater()
            except Exception as E:
                pass

        for i in self.ScheduleManager.schedules:
            widget = AlarmWidget(i, self)

            self.AlarmList.addWidget(widget)

    def get_time_contents(self, current_time=time.localtime()):
        self.CurrentTime.setText(time.strftime("%p %I:%M:%S", current_time))
        self.CurrentDate.setText(time.strftime("%Y-%m-%d", current_time))

    def timer_handler(self):
        current_time = time.localtime()

        self.get_time_contents(current_time)

        schedules = self.ScheduleManager.get_schedules(int(time.mktime(current_time)))

        if len(schedules) > 0:
            for i in schedules:
                if i.is_enabled:
                    alarm_window = AlarmWindow(i, self)

                    alarm_window.show()

    def alarm_add_handler(self):
        try:
            add_window = AlarmAddWindow(self)
            add_window.show()

            self.statusbar.showMessage("알림 추가 창을 열었습니다.")
        except Exception as E:
            print(E)

    def alarmNL_add_handler(self):
        try:
            addNL_window = AlarmNLAddWindow(self)
            addNL_window.show()

            self.statusbar.showMessage("알림 추가(NLP) 창을 열었습니다.")
        except Exception as E:
            print(E)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = MainWindow()

    myWindow.show()
    myWindow.Timer.start()

    app.exec_()
