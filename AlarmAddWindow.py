import os
import re
import sys

from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import *

from Schedule import ScheduleGenerator

UI = uic.loadUiType("./ui/AlarmAddWindow.ui")[0]

TZRegExp = re.compile(r"^((?:\+|\-)\d{2}\d{2})$")


class AlarmAddWindow(QDialog, UI):
    def __init__(self, parent=None, schedule=None):
        """
        AlarmAddWindow Class
        :param schedule: if open this window as Schedule edit mode, you can pass Schedule object to this parameters
        """
        super(AlarmAddWindow, self).__init__(parent)

        self.setupUi(self)

        self.parent = parent

        self.AlarmTime.setTime(QTime.currentTime())
        self.AlarmDate.setDate(QDate.currentDate())

        self.addButton.clicked.connect(self.add_btn_clicked)
        self.cancelButton.clicked.connect(self.cancel_btn_clicked)
        self.AlarmTune.clicked.connect(self.tune_btn_clicked)
        self.tune = ""

        if schedule is not None:
            self.name = schedule.name

            self.AlarmName.setText(self.name)

        if schedule is not None:
            self.time_str, self.date_str, self.timezone = schedule.get_time()

            self.AlarmTime.setTime(QTime.fromString(self.time_str, "HH:mm:ss"))
            self.AlarmDate.setDate(QDate.fromString(self.date_str, "Y-M-d"))
            self.AlarmTimezone.setText(self.timezone)

        if schedule is not None:
            self.tune_url = schedule.tune

            if self.tune_url:
                self.AlarmTuneInfo.setText(os.path.split(self.tune_url)[1])

        if schedule is not None:
            self.description = schedule.description

            self.AlarmDescription.setPlainText(self.description)

    def cancel_btn_clicked(self):
        self.close()

    def add_btn_clicked(self):
        try:
            time = self.AlarmTime.time()
            date = self.AlarmDate.date()

            self.time_str = time.toString("HH:mm:ss")
            self.date_str = date.toString("Y-M-d")

            self.description = self.AlarmDescription.toPlainText()

            self.name = self.AlarmName.text()

            self.timezone = self.AlarmTimezone.text()

            print(self.name, self.time_str, self.date_str, self.tune, self.timezone, self.description)

            timezone_result = TZRegExp.search(self.AlarmTimezone.text())

            if not timezone_result:
                if self.parent is not None:
                    self.parent.statusbar.showMessage(f"{self.timezone} 은 맞지 않는 시간대 문자열 입니다. (+-HHMM)")
                return
            else:
                print(timezone_result.group(1))
        except Exception as E:
            print(E)

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

    myWindow = AlarmAddWindow(schedule=schedule)

    myWindow.show()

    app.exec_()
