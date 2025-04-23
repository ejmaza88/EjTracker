class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return f"TimeEntry(start_time={self.start_time}, end_time={self.end_time}, duration={self.duration})"