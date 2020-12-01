import pickle
import time

from Schedule import Schedule, ScheduleGenerator


class ScheduleManager:
    def __init__(self):
        self.scheduleFile = "schedule.remi"
        self.schedules = []  # [Schedules]
        self.mapped_schedules = {}  # { Timestamp: [ Schedules ] }

        try:
            with open(self.scheduleFile, "rb") as F:
                self.schedules = pickle.load(F)

                for i in self.schedules:
                    if i.get_timestamp() < time.mktime(time.localtime()):
                        self.schedules.remove(i)
                    else:
                        if i.get_timestamp() in self.mapped_schedules:
                            self.mapped_schedules[i.get_timestamp()].append(i)
                        else:
                            self.mapped_schedules[i.get_timestamp()] = [i]

                F.close()
        except FileNotFoundError as E:
            with open(self.scheduleFile, "wb") as F:
                pickle.dump(self.schedules, F)

                F.close()

    def add_schedule(self, p_schedule):
        """
        Add schedule.
        :param p_schedule: Schedule object
        :return:
        """

        if isinstance(p_schedule, Schedule):
            self.schedules.append(p_schedule)

            if p_schedule.get_timestamp() in self.mapped_schedules:
                self.mapped_schedules[p_schedule.get_timestamp()].append(p_schedule)
            else:
                self.mapped_schedules[p_schedule.get_timestamp()] = [p_schedule]
        else:
            raise ValueError("schedule argument only a Schedule object")

    def remove_schedule(self, p_schedule):
        """
        Remove schedule. if return true: schedule remove success
        :param p_schedule: Schedule object
        :return:
        """

        if isinstance(p_schedule, Schedule):
            try:
                self.schedules.remove(p_schedule)

                if len(self.mapped_schedules[p_schedule.get_timestamp()]) == 1:
                    del self.mapped_schedules[p_schedule.get_timestamp()]
                else:
                    self.mapped_schedules[p_schedule.get_timestamp()].remove(p_schedule)
                return True
            except ValueError:
                return False
        else:
            raise ValueError("schedule argument only a Schedule object")

    def get_schedules(self, timestamp):
        """
        Get schedules from timestmap
        :param timestamp: Timestamp (integer)
        :return:
        """
        if isinstance(timestamp, int):
            return self.mapped_schedules[timestamp]
        else:
            raise ValueError("timestamp argument only a integer (Timestamp)")

    def save(self):
        try:
            with open(self.scheduleFile, "wb") as F:
                pickle.dump(self.schedules, F)

                F.close()
        except Exception as E:
            print(E)

    def __repr__(self):
        print(self.schedules)


if __name__ == '__main__':
    manager = ScheduleManager()

    sg = ScheduleGenerator()

    sg.set_name("testSchedule")
    sg.set_description("test schedule description")
    sg.set_time("10:00:00", "2020-12-25")

    schedule = sg.generate()

    manager.add_schedule(schedule)

    print(manager.get_schedules(schedule.get_timestamp()))

    manager.remove_schedule(schedule)