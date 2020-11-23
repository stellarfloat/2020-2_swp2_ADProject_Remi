import datetime

# Schedule (name: String, time: String(ISO-8601), description: String, tune: String)
class Schedule:
    def __init__(self, name, time, description="", tune=""):
        self.name = name
        self.description = description
        self.tune = tune
        self.time = time