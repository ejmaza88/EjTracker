# Time Tracker

A simple macOS menu bar application for tracking your work time.

## Features

- Track your work time with a simple click on the menu bar icon
- View time spent on tasks
- Add notes about what you worked on
- Save time entries to CSV for later analysis

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install the package in development mode:
   ```
   pip install -e .
   ```

## Usage

Run the application with:
```
time_tracker
```

- Click the stopwatch icon in the menu bar to start tracking
- Click again to stop tracking and enter details about your work
- Time entries are saved to `~/.time_tracker/time_entries.csv`