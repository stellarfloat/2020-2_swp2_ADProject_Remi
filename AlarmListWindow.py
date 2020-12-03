import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

from AlarmAddWindow import AlarmAddWindow

UI = uic.loadUiType("./ui/AlarmListWindow.ui")[0]


class AlarmListWindow(QDialog, UI):
    def __init__(self, parent=None):
        super(AlarmListWindow, self).__init__(parent)

        self.parent = parent

        self.ScheduleManager = self.parent.ScheduleManager

        self.setupUi(self)

        self.AlarmListTable.setRowCount(len(self.ScheduleManager.schedules))
        self.AlarmListTable.setHorizontalHeaderLabels(['알람 이름', '알람 시각', '반복일'])

        self.removeButton.clicked.connect(self.remove_button_handler)
        self.modifyButton.clicked.connect(self.modify_button_handler)
        self.closeButton.clicked.connect(self.close_button_handler)

        self.get_contents()

    def get_contents(self):
        idx = 0

        self.AlarmListTable.clearContents()

        self.AlarmListTable.setColumnCount(3)
        self.AlarmListTable.setRowCount(len(self.ScheduleManager.schedules))

        for i in self.ScheduleManager.schedules:
            p = QTableWidgetItem(i.name)
            q = QTableWidgetItem(" ".join(i.get_time()))
            r = QTableWidgetItem(str(i.repeat))

            self.AlarmListTable.setItem(idx, 0, p)
            self.AlarmListTable.setItem(idx, 1, q)
            self.AlarmListTable.setItem(idx, 2, r)

            idx += 1

        self.AlarmListTable.resizeRowsToContents()
        self.AlarmListTable.resizeColumnsToContents()

    def get_clicked_schedule(self):
        ranges = self.AlarmListTable.selectedRanges()

        i = ranges[0].bottomRow()

        p = self.AlarmListTable.item(i, 0)
        q = self.AlarmListTable.item(i, 1)
        r = self.AlarmListTable.item(i, 2)

        p = p.text()
        q = q.text()
        r = r.text()

        print(p, q, r, int(r))

        return self.ScheduleManager.find_schedule(p, q, int(r))

    def remove_button_handler(self):

        schedule = self.get_clicked_schedule()

        if schedule is not None:
            self.ScheduleManager.remove_schedule(schedule)
            self.get_contents()

    def modify_button_handler(self):
        schedule = self.get_clicked_schedule()

        if schedule is not None:
            modify_window = AlarmAddWindow(parent=self, p_schedule=schedule)
            modify_window.open()

    def close_button_handler(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = AlarmListWindow()

    myWindow.show()

    app.exec_()
