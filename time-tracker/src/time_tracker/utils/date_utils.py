from datetime import datetime, timedelta

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_duration(start: datetime, end: datetime) -> timedelta:
    return end - start

def parse_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")