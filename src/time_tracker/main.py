"""
Main entry point for the Time Tracker application.
"""
# First, load the bootstrap to ensure all dependencies are properly available
try:
    from time_tracker.bootstrap.loader import initialize
    initialize()
except ImportError:
    print("Warning: Bootstrap loader not available")

# Now import the actual application
from time_tracker.app import TimeTrackerApp

def main():
    app = TimeTrackerApp()
    app.run()

if __name__ == "__main__":
    main()