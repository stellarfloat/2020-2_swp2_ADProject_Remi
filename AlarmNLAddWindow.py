import os
import re
import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import *

from ko_NL_time_parser.ko_NL_time_parser import parse_time
from Schedule import Schedule, ScheduleGenerator

UI = uic.loadUiType("./ui/AlarmNLAddWindow.ui")[0]

TZRegExp = re.compile(r"^((?:\+|-)\d{2}\d{2})$")


class AlarmNLAddWindow(QDialog, UI):
    schedule: Schedule

    def __init__(self, parent=None, p_schedule=None):
        """
        AlarmAddWindow Class
        :param p_schedule: if open this window as Schedule edit mode, you can pass Schedule object to this parameters
        """
        super(AlarmNLAddWindow, self).__init__(parent)

        self.setupUi(self)

        self.parent = parent
        self.schedule = p_schedule

        self.AlarmDateTime.setDateTime(QDateTime.currentDateTime())

        self.addButton.clicked.connect(self.add_btn_clicked)
        self.cancelButton.clicked.connect(self.cancel_btn_clicked)
        self.ButtonNLparse.clicked.connect(self.parse_btn_clicked)
        self.datetimeTextRaw.returnPressed.connect(self.parse_btn_clicked)
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

            self.AlarmDateTime.setDateTime(QDateTime.fromString(f'{self.date_str} {self.time_str}', 'yyyy-MM-dd hh:mm:ss'))

            self.tune = p_schedule.tune

            if self.tune:
                self.AlarmTuneInfo.setText(os.path.split(self.tune)[1])

            self.description = p_schedule.description
            self.AlarmDescription.setPlainText(self.description)

            self.repeat = p_schedule.repeat
            self.AlarmRepeat.setValue(self.repeat)

    def cancel_btn_clicked(self):
        self.close()

    def parse_btn_clicked(self):
        text = self.datetimeTextRaw.text()
        try:
            parsed_time, translated, optimized = parse_time(text, time_base = datetime.now())
        except Exception as E:
            self.displayParseLog.setText(E)
        else:
            self.displayParseLog.setText(f'**Result |** `(In)`_{[t.name for t in translated]}_ **->** `(Out)`_{[t.name for t in optimized]}_')
            if len(optimized) > 0:
                time_str = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                self.AlarmDateTime.setDateTime(QDateTime.fromString(time_str, 'yyyy-MM-dd hh:mm:ss'))
        

    def add_btn_clicked(self):
        try:
            time = self.AlarmDateTime.time()
            date = self.AlarmDateTime.date()

            self.time_str = time.toString("HH:mm:ss")
            self.date_str = date.toString("yyyy-M-dd")

            self.description = str(self.AlarmDescription.toPlainText())

            self.name = self.AlarmName.text()

            self.timezone = '+0900' #self.AlarmTimezone.text()

            self.repeat = self.AlarmRepeat.value()

            if self.name == "":
                self.parent.statusbar.showMessage("일정 이름을 입력해주세요.")
                return

            # timezone_result = TZRegExp.search(self.AlarmTimezone.text())

            # if not timezone_result:
            #     self.parent.statusbar.showMessage(f"{self.timezone} 은 정확하지 않은 시간대입니다. (+-HHMM)")

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

    myWindow = AlarmNLAddWindow(p_schedule=schedule)

    myWindow.show()

    app.exec_()
