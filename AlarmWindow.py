import sys
from datetime import timedelta

from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import *
from PyQt5 import uic

from Schedule import Schedule, ScheduleGenerator, get_time

UI = uic.loadUiType("./ui/AlarmWindow.ui")[0]


class AlarmWindow(QDialog, UI):
    schedule: Schedule

    def __init__(self, schedule, parent):
        super(AlarmWindow, self).__init__(parent)

        self.setupUi(self)

        self.schedule = schedule
        self.parent = parent

        self.AlarmTitle.setText(self.schedule.name)

        self.AlarmDescription.setPlainText(self.schedule.description)

        QSound.play(self.schedule.tune if self.schedule.tune else "DefaultAlarm.wav")

        self.confirmButton.clicked.connect(self.confirm_button_handler)

    def confirm_button_handler(self):
        if self.schedule.repeat > 0:
            print(self.schedule.get_time())

            self.schedule.time += timedelta(days=self.schedule.repeat)

            if type(self.parent).__name__ == "MainWindow":
                self.parent.ScheduleManager.schedule_mapper()

            print(self.schedule.get_time())

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sg = ScheduleGenerator()

    sg.set_name("테스트 일정").time = get_time("10:00:00", "2020-12-25", "-1400")
    sg.set_description("테스트 일정의 테스트 설명").set_repeat(7)

    myWindow = AlarmWindow(sg.generate(), None)

    myWindow.show()

    app.exec_()
