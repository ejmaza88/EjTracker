
import os
import sys
import datetime

def log_exception(exc_type, exc_value, exc_traceback):
    error_log_path = os.path.expanduser('~/time_tracker_error.log')
    with open(error_log_path, 'a') as f:
        f.write('\n\n' + '-' * 60 + '\n')
        f.write(f"Exception logged at: {datetime.datetime.now()}\n")
        
        # Log system information
        f.write(f"System: {sys.platform}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Executable: {sys.executable}\n")
        f.write(f"Sys.path: {sys.path}\n\n")
        
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

sys.excepthook = log_exception

if __name__ == '__main__':
    try:
        # Set Python path to include the application directories
        bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, bundle_dir)
        
        from time_tracker.main import main
        main()
    except Exception as e:
        log_exception(type(e), e, e.__traceback__)
        # Show an error dialog
        import traceback
        error_message = f"Application Error: {str(e)}\n\nSee ~/time_tracker_error.log for more details"
        
        try:
            # Try to show a PyQt dialog
            from PyQt6.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Time Tracker Error", error_message)
        except:
            # Fall back to a basic dialog
            import subprocess
            subprocess.call(['osascript', '-e', f'display dialog "{error_message}" buttons {{"OK"}} default button "OK" with title "Time Tracker Error" with icon stop'])
