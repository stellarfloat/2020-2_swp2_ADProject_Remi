import sys
import time
from datetime import datetime

from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import *
from PyQt5 import uic
from dateutil.relativedelta import relativedelta

from Schedule import Schedule, ScheduleGenerator

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
            _sg = ScheduleGenerator()

            _sg.set_name(self.schedule.name)
            _sg.set_tune(self.schedule.tune if self.schedule.tune else "")
            _sg.set_description(self.schedule.description)
            _sg.set_repeat(self.schedule.repeat)

            repeat_time = datetime.strptime(" ".join(self.schedule.get_time()), "%Y-%m-%d %H:%M:%S %z")

            repeat_time + relativedelta(days=self.schedule.repeat)

            repeat_time = time.strftime("%Y-%m-%d %H:%M:%S %z", repeat_time.timetuple()).split()

            _sg.set_time(repeat_time[1], repeat_time[0], repeat_time[2])

            if self.parent is not None:
                self.parent.ScheduleManager.add_schedule(_sg.generate())
            else:
                print(_sg.generate())

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sg = ScheduleGenerator()

    sg.set_name("테스트 일정").time = time.localtime()
    sg.set_description("테스트 일정의 테스트 설명").set_repeat(7)

    myWindow = AlarmWindow(sg.generate(), None)

    myWindow.show()

    app.exec_()
