import os
import re
import sys

from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import *

from Schedule import ScheduleGenerator, Schedule

UI = uic.loadUiType("./ui/AlarmAddWindow.ui")[0]

TZRegExp = re.compile(r"^((?:\+|-)\d{2}\d{2})$")


class AlarmAddWindow(QDialog, UI):
    schedule: Schedule

    def __init__(self, parent=None, p_schedule=None):
        """
        AlarmAddWindow Class
        :param p_schedule: if open this window as Schedule edit mode, you can pass Schedule object to this parameters
        """
        super(AlarmAddWindow, self).__init__(parent)

        self.setupUi(self)

        self.parent = parent
        self.schedule = p_schedule

        self.AlarmTime.setTime(QTime.currentTime())
        self.AlarmDate.setDate(QDate.currentDate())

        self.addButton.clicked.connect(self.add_btn_clicked)
        self.cancelButton.clicked.connect(self.cancel_btn_clicked)
        self.AlarmTune.clicked.connect(self.tune_btn_clicked)

        self.name = ""
        self.description = ""
        self.tune = ""
        self.repeat = 0

        if p_schedule is not None:
            self.addButton.setText("수정")

            self.name = p_schedule.name

            self.AlarmName.setText(self.name)

            self.date_str, self.time_str, self.timezone = p_schedule.get_time()

            self.AlarmTime.setTime(QTime.fromString(self.time_str, "HH:mm:ss"))
            self.AlarmDate.setDate(QDate.fromString(self.date_str, "Y-M-d"))
            self.AlarmTimezone.setText(self.timezone)

            self.tune = p_schedule.tune

            if self.tune:
                self.AlarmTuneInfo.setText(os.path.split(self.tune)[1])

            self.description = p_schedule.description
            self.AlarmDescription.setPlainText(self.description)

            self.repeat = p_schedule.repeat
            self.AlarmRepeat.setValue(self.repeat)

    def cancel_btn_clicked(self):
        self.close()

    def add_btn_clicked(self):
        try:
            time = self.AlarmTime.time()
            date = self.AlarmDate.date()

            self.time_str = time.toString("HH:mm:ss")
            self.date_str = date.toString("yyyy-M-dd")

            self.description = str(self.AlarmDescription.toPlainText())

            self.name = self.AlarmName.text()

            self.timezone = self.AlarmTimezone.text()

            self.repeat = self.AlarmRepeat.value()

            if self.name == "":
                self.parent.statusbar.showMessage("일정 이름을 입력해주세요.")
                return

            timezone_result = TZRegExp.search(self.AlarmTimezone.text())

            if not timezone_result:
                self.parent.statusbar.showMessage(f"{self.timezone} 은 정확하지 않은 시간대입니다. (+-HHMM)")

            if self.schedule:
                self.schedule.name = self.name
                self.schedule.set_time(self.time_str, self.date_str, self.timezone)
                self.schedule.description = self.description
                self.schedule.tune = self.tune
                self.schedule.repeat = self.repeat
            else:
                print(self.description)

                sg_ = ScheduleGenerator()

                sg_.set_name(self.name)
                sg_.set_time(self.time_str, self.date_str, self.timezone)
                sg_.set_description(self.description)
                sg_.set_tune(self.tune)
                sg_.set_repeat(self.repeat)

                sch = sg_.generate()
                self.parent.ScheduleManager.add_schedule(sch)

            if type(self.parent).__name__ == "MainWindow":
                self.parent.ScheduleManager.save()
                self.parent.ScheduleManager.schedule_mapper()

                self.parent.get_contents()

            self.close()
        except Exception as E:
            print(E)

        self.close()

    def tune_btn_clicked(self):
        tune_file = QFileDialog.getOpenFileName(parent=self, caption="알람음 열기", filter="*.wav *.mp3")

        if tune_file[1] is not None:
            self.tune = tune_file[0]

            print(os.path.split(self.tune))

            self.AlarmTuneInfo.setText(os.path.split(self.tune)[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sg = ScheduleGenerator()

    sg.set_name("testSchedule")
    sg.set_description("test schedule description")
    sg.set_time("10:00:00", "2020-12-25")  # "-0800")

    schedule = sg.generate()

    myWindow = AlarmAddWindow(p_schedule=schedule)

    myWindow.show()

    app.exec_()
