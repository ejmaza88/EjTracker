import rumps
import sys
import os
from PyQt6.QtWidgets import QApplication
from datetime import datetime
from time_tracker.utils.time_manager import TimeManager
from time_tracker.gui.main_window import TimeTrackerWindow

class TimeTrackerApp(rumps.App):
    def __init__(self):
        # Get the path to the icons
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_dir = os.path.join(base_dir, "resources", "icons", "menubar")
        self.play_icon = os.path.join(icon_dir, "play.png")
        self.stop_icon = os.path.join(icon_dir, "stop.png")
        
        # Initialize with the play icon
        super().__init__(
            name="Time Tracker",
            icon=self.play_icon,
            menu=[],
            quit_button=None  # Disable default quit button so we can add our own
        )
        
        # Store action name to avoid duplicates
        self.tracking_action_name = "Start Tracking"
        
        # Add the tracking menu item with a proper callback
        tracking_item = rumps.MenuItem(self.tracking_action_name, callback=self.toggle_tracking)
        self.menu.add(tracking_item)
        
        # Add quit button with proper label
        quit_item = rumps.MenuItem("Quit", callback=self.quit_app)
        self.menu.add(quit_item)
        
        self.time_manager = TimeManager()
        self.update_menu()
    
    def update_menu(self):
        """Update both the icon and menu text based on tracking state"""
        is_tracking = self.time_manager.is_tracking()
        
        # Update icon - use stop icon when tracking, play icon when not
        self.icon = self.stop_icon if is_tracking else self.play_icon
        
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
        
        # Update menu text and icon
        self.update_menu()
    
    def quit_app(self, _):
        """Custom quit handler to ensure tracking is stopped before quitting"""
        # If tracking is active, stop it before quitting
        if self.time_manager.is_tracking():
            start_time, end_time = self.time_manager.stop_tracking()
            # Optionally show the tracker window when quitting while tracking
            self.show_tracker_window(start_time, end_time)
        
        # Quit the application
        rumps.quit_application()
    
    def show_tracker_window(self, start_time, end_time):
        """Show the tracker window with PyQt"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        window = TimeTrackerWindow(start_time, end_time)
        window.show()
        app.exec()