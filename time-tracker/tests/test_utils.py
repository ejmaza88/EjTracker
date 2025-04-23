import unittest
from src.time_tracker.utils.date_utils import format_duration, calculate_duration

class TestDateUtils(unittest.TestCase):

    def test_format_duration(self):
        self.assertEqual(format_duration(3600), "1 hour")
        self.assertEqual(format_duration(7200), "2 hours")
        self.assertEqual(format_duration(3661), "1 hour, 1 minute")
        self.assertEqual(format_duration(61), "1 minute")
        self.assertEqual(format_duration(0), "0 seconds")

    def test_calculate_duration(self):
        start_time = "2023-10-01 10:00:00"
        end_time = "2023-10-01 12:30:00"
        self.assertEqual(calculate_duration(start_time, end_time), 9000)  # 2 hours 30 minutes in seconds

        start_time = "2023-10-01 14:00:00"
        end_time = "2023-10-01 14:15:00"
        self.assertEqual(calculate_duration(start_time, end_time), 900)  # 15 minutes in seconds

if __name__ == '__main__':
    unittest.main()