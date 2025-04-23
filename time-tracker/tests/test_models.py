import unittest
from time_tracker.models.time_entry import TimeEntry

class TestTimeEntry(unittest.TestCase):

    def setUp(self):
        self.entry = TimeEntry(start_time="2023-01-01 09:00:00", end_time="2023-01-01 10:00:00")

    def test_duration(self):
        self.assertEqual(self.entry.duration(), 3600)  # Duration in seconds

    def test_start_time(self):
        self.assertEqual(self.entry.start_time, "2023-01-01 09:00:00")

    def test_end_time(self):
        self.assertEqual(self.entry.end_time, "2023-01-01 10:00:00")

    def test_invalid_time_entry(self):
        with self.assertRaises(ValueError):
            TimeEntry(start_time="2023-01-01 10:00:00", end_time="2023-01-01 09:00:00")

if __name__ == '__main__':
    unittest.main()