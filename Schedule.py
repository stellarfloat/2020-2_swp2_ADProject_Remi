import time
from datetime import datetime


class Schedule:
    name: str
    time: datetime
    tune: str
    description: str
    repeat: int
    is_enabled: bool

    def __init__(self, name: str, ptime: datetime, description: str, tune: str, repeat: int):
        """
        Schedule.__init__
        :param name: Schedule Name: str
        :param ptime: Schedule Time: time.struct_time
        :param description: Schedule Description: String(allow null)
        :param tune: Schedule Alarm Tune: String(allow null)
        :param repeat: Schedule Repeat: int (0: no repeat, n: repeat with n days)
        """
        self.name = name
        self.description = description
        self.tune = tune
        self.time = ptime
        self.repeat = repeat
        self.is_enabled = True

    def get_timestamp(self):
        """
        Get timestamp (UTC) from Schedule
        :return: Timestamp
        """
        return int(self.time.timestamp())

    def get_time(self):
        """
        Get time string [Y-M-D, H:M:S, +-HHMM] from Schedule
        :return:
        """
        return self.time.strftime("%Y-%m-%d %H:%M:%S %z").split()

    def set_time(self, ptime: str, date: str, timezone: str = time.strftime("%z")):
        """
        Set Schedule time (with Timezone)
        :param ptime: "H:M:S"
        :param date: "Y-M-D"
        :param timezone: "+-HHMM"
        :return:
        """
        self.time = get_time(ptime, date, timezone)

    def __repr__(self):
        return f"Schedule({self.name}, {self.description}, {self.get_timestamp()}, " \
               f"{self.tune}, {self.repeat} day repeat)"


class ScheduleGenerator:
    def __init__(self):
        self.name = None
        self.description = None
        self.tune = None
        self.time = None
        self.repeat = 0

    def set_name(self, name: str):
        """
        Set Schedule name
        :param name: String
        :return:
        """
        if isinstance(name, str):
            self.name = name
            return self
        else:
            raise ValueError("name argument is must be String")

    def set_description(self, description: str):
        """
        Set Schedule description
        :param description: String
        :return:
        """

        if isinstance(description, str):
            self.description = description
            return self
        else:
            raise ValueError("description argument is must be String or None")

    def set_tune(self, tune: str):
        """
        Set Schedule alarm tune
        :param tune:
        :return:
        """
        if isinstance(tune, str):
            self.tune = tune
            return self
        else:
            raise ValueError("tune argument is must be String")

    def set_time(self, ptime: str, date: str, timezone: str = time.strftime("%z")):
        """
        Set Schedule time (with Timezone)
        :param ptime: "H:M:S"
        :param date: "Y-M-D"
        :param timezone: "+-HHMM"
        :return:
        """
        self.time = get_time(ptime, date, timezone)

        return self

    def set_repeat(self, repeat: int):
        """
        Set Schedule Repeat
        :param repeat: int
        :return:
        """
        self.repeat = repeat

        return self

    def generate(self):
        """
        Generate Schedule object
        :return: Schedule with configurable fields
        """
        return Schedule(self.name, self.time, self.description, self.tune, self.repeat)


def get_time(ptime: str, date: str, timezone: str = time.strftime("%z")):
    """
    Set Schedule time (with Timezone)
    :param ptime: "H:M:S"
    :param date: "Y-M-D"
    :param timezone: "+-HHMM"
    :return:
    """
    return datetime.strptime((date + " " + ptime + " " + timezone).rstrip(), "%Y-%m-%d %H:%M:%S %z")


if __name__ == '__main__':
    sg = ScheduleGenerator()

    sg.set_name("testSchedule")
    sg.set_description("test schedule description")
    sg.set_time("10:00:00", "2020-12-25", "-1400")
    sg.set_repeat(7)

    schedule = sg.generate()

    print(schedule, schedule.get_timestamp())

    print(schedule.time)

    # Schedule(
    #   testSchedule,
    #   test schedule description,
    #   1608858000,
    #   None,
    #   7 day repeat
    # )
    # 1608858000
    # 2020-12-25 10:00:00-14:00
