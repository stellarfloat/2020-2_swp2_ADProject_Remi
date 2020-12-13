import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

from AlarmAddWindow import AlarmAddWindow
from Schedule import Schedule, ScheduleGenerator, get_time

UI = uic.loadUiType("./ui/AlarmWidget.ui")[0]


class AlarmWidget(QWidget, UI):
    def __init__(self, schedule: Schedule, parent=None):
        super(AlarmWidget, self).__init__(parent)

        self.parent = parent

        self.setupUi(self)

        self.schedule = schedule

        self.AlarmName.setText(self.schedule.name)
        self.AlarmTime.setText(" ".join(self.schedule.get_time()))
        self.AlarmDescription.setText(self.schedule.description)
        self.AlarmRepeat.setText("반복: " + (str(self.schedule.repeat) + "일마다" if self.schedule.repeat > 0 else "없음"))

        self.alarm_button_styler()

        self.enableAlarm.clicked.connect(self.alarm_button_handler)
        self.removeAlarm.clicked.connect(self.remove_button_handler)
        self.editAlarm.clicked.connect(self.edit_button_handler)

    def alarm_button_styler(self):
        if self.schedule.is_enabled:
            self.enableAlarm.setStyleSheet("background-color: green;")
            self.enableAlarm.setText("활성화")
        else:
            self.enableAlarm.setStyleSheet("background-color: red;")
            self.enableAlarm.setText("비활성화")

    def alarm_button_handler(self):
        self.schedule.is_enabled = not self.schedule.is_enabled

        print(self.schedule.is_enabled)

        self.alarm_button_styler()

    def remove_button_handler(self):
        if self.schedule is not None and self.parent.ScheduleManager is not None:
            self.parent.ScheduleManager.remove_schedule(self.schedule)
            self.parent.get_contents()

    def edit_button_handler(self):
        if self.schedule is not None:
            modify_window = AlarmAddWindow(parent=self, p_schedule=self.schedule)
            modify_window.open()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sg = ScheduleGenerator()

    sg.set_name("테스트 일정").time = get_time("10:00:00", "2020-12-25", "-1400")
    sg.set_description("테스트 일정의 테스트 설명").set_repeat(7)

    myWindow = AlarmWidget(sg.generate())

    myWindow.show()

    app.exec_()
