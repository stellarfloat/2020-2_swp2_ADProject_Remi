import time


# Schedule (name: String, time: String(ISO-8601), description: String, tune: String)
class Schedule:
    def __init__(self, name, ptime, description, tune):
        self.name = name
        self.description = description
        self.tune = tune
        self.time = ptime

    def get_timestamp(self):
        """
        Get timestamp (UTC) from Schedule
        :return: Timestamp
        """
        return int(time.mktime(self.time))

    def __repr__(self):
        return f"Schedule({self.name}, {self.description}, {self.time}, {self.tune})"


class ScheduleGenerator:
    def __init__(self):
        self.name = None
        self.description = None
        self.tune = None
        self.time = None

    # ScheduleGenerator.setName(name: String): self
    def set_name(self, name):
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

    # ScheduleGenerator.setDescription(description: String | None): self
    def set_description(self, description: str = ""):
        """
        Set Schedule description
        :param description: String
        :return:
        """
        if isinstance(description, str) or isinstance(description, None):
            self.description = description
            return self
        else:
            raise ValueError("description argument is must be String or None")

    # ScheduleGenerator.setTune(tune: String(AbsolutePath) | None): self
    def set_tune(self, tune: str = ""):
        """
        Set Schedule alarm tune
        :param tune:
        :return:
        """
        if isinstance(tune, str):
            self.description = tune
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
        ftime = time.strptime((date + " " + ptime + " " + timezone).rstrip(), "%Y-%m-%d %H:%M:%S %z")

        self.time = ftime

        return self

    # ScheduleGenerator.generate(): Schedule
    def generate(self):
        """
        Generate Schedule object
        :return: Schedule with configurable fields
        """
        return Schedule(self.name, self.time, self.description, self.tune)


if __name__ == '__main__':
    sg = ScheduleGenerator()

    sg.set_name("testSchedule")
    sg.set_description("test schedule description")
    sg.set_time("10:00:00", "2020-12-25")  # "-0800")

    schedule = sg.generate()

    print(schedule, schedule.get_timestamp())

    # Schedule(
    #   testSchedule,
    #   test schedule description,
    #   time.struct_time,
    #   None
    # )
    # 1608858000
