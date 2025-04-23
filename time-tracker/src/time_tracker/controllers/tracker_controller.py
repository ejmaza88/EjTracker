class TrackerController:
    def __init__(self):
        self.time_entries = []

    def start_entry(self, description):
        entry = {
            'description': description,
            'start_time': self._get_current_time(),
            'end_time': None,
            'duration': None
        }
        self.time_entries.append(entry)

    def stop_entry(self):
        if self.time_entries and self.time_entries[-1]['end_time'] is None:
            self.time_entries[-1]['end_time'] = self._get_current_time()
            self.time_entries[-1]['duration'] = self._calculate_duration(self.time_entries[-1]['start_time'], self.time_entries[-1]['end_time'])

    def save_entries(self, file_path):
        with open(file_path, 'w') as file:
            for entry in self.time_entries:
                file.write(f"{entry['description']}, {entry['start_time']}, {entry['end_time']}, {entry['duration']}\n")

    def _get_current_time(self):
        from datetime import datetime
        return datetime.now()

    def _calculate_duration(self, start_time, end_time):
        from datetime import datetime
        start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        return (end - start).total_seconds()