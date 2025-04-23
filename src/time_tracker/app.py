import rumps
import sys
from PyQt6.QtWidgets import QApplication
from datetime import datetime
from time_tracker.utils.time_manager import TimeManager
from time_tracker.gui.main_window import TimeTrackerWindow

class TimeTrackerApp(rumps.App):
    def __init__(self):
        # Initialize with an empty menu first
        super().__init__(
            "⏱️",         # App name/icon
            menu=[],      # Start with empty menu
            quit_button=None  # Disable default quit button so we can add our own
        )
        
        # Store action name to avoid duplicates
        self.tracking_action_name = "Start Tracking"
        
        # Add the tracking menu item with a proper callback
        tracking_item = rumps.MenuItem(self.tracking_action_name, callback=self.toggle_tracking)
        self.menu.add(tracking_item)
        
        # Add quit button with proper label
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))
        
        self.time_manager = TimeManager()
        self.update_menu()
    
    def update_menu(self):
        """Update both the icon and menu text based on tracking state"""
        is_tracking = self.time_manager.is_tracking()
        
        # Update icon
        self.title = "⏱️ 🔴" if is_tracking else "⏱️"
        
        # Update menu text - correct approach to modify rumps menu items
        new_action_name = "Stop Tracking" if is_tracking else "Start Tracking"
        
        # Only update if the name changed to avoid duplication
        if new_action_name != self.tracking_action_name:
            # Delete the old menu item and create a new one with different key
            del self.menu[self.tracking_action_name]
            
            # Add new menu item with updated title at the beginning
            new_item = rumps.MenuItem(new_action_name, callback=self.toggle_tracking)
            
            # Insert at the beginning (before the Quit item)
            self.menu.insert_before("Quit", new_item)
            
            # Update stored action name
            self.tracking_action_name = new_action_name
    
    def toggle_tracking(self, _):
        """Toggle time tracking on/off"""
        if self.time_manager.is_tracking():
            # Stop tracking and show window
            start_time, end_time = self.time_manager.stop_tracking()
            self.show_tracker_window(start_time, end_time)
        else:
            # Start tracking
            self.time_manager.start_tracking()
            # Flash the menu bar icon briefly for feedback
            self.title = "⏱️ ▶️"
            rumps.Timer(lambda _: self.update_menu(), 1).start()
        
        # Update menu text and icon
        self.update_menu()
    
    def show_tracker_window(self, start_time, end_time):
        """Show the tracker window with PyQt"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        window = TimeTrackerWindow(start_time, end_time)
        window.show()
        app.exec()