import sys

from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re, os

UI = uic.loadUiType("./ui/AlarmAddWindow.ui")[0]

TZRegExp = re.compile(r"^((?:\+|\-)\d{2}\d{2})$")


class AlarmAddWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.AlarmTime.setTime(QTime.currentTime())
        self.AlarmDate.setDate(QDate.currentDate())

        self.addButton.clicked.connect(self.add_btn_clicked)
        self.AlarmTune.clicked.connect(self.tune_btn_clicked)

        self.name = ""
        self.time_str = ""
        self.date_str = ""
        self.tune_url = ""
        self.description = ""
        self.timezone = ""

    def add_btn_clicked(self):
        time = self.AlarmTime.time()
        date = self.AlarmDate.date()

        self.time_str = time.toString("HH:mm:ss")
        self.date_str = date.toString("Y-M-d")

        self.description = self.AlarmDescription.toPlainText()

        self.name = self.AlarmName.text()

        self.timezone = self.AlarmTimezone.text()

        print(self.name, self.time_str, self.date_str, self.tune_url, self.timezone, self.description)

        timezone_result = TZRegExp.search(self.AlarmTimezone.text())

        if not timezone_result:
            self.statusBar.showMessage(f"{self.timezone} 은 맞지 않는 시간대 문자열 입니다. (+-HHMM)")
            return
        else:
            print(timezone_result.group(1))

    def tune_btn_clicked(self):
        tune_file = QFileDialog.getOpenFileName(parent=self, caption="알람음 열기", filter="*.wav *.mp3")

        if tune_file[1] is not None:
            self.tune_url = tune_file[0]

            print(os.path.split(self.tune_url))

            self.AlarmTuneInfo.setText(os.path.split(self.tune_url)[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = AlarmAddWindow()

    myWindow.show()

    app.exec_()
