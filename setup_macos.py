"""
This script is used to build a standalone macOS application using py2app.
Run 'python setup_macos.py py2app' to build the application.
"""
from setuptools import setup
import sys
import os

# Use our special launcher script as the main entry point
APP = ['src/app_launcher.py']
DATA_FILES = [
    ('resources/icons/menubar', ['resources/icons/menubar/play.png', 'resources/icons/menubar/stop.png']),
    ('resources/icons', ['resources/icons/app_icon.icns']),
]

# Try to find the styles file
try:
    if os.path.exists('resources/styles/default.qss'):
        DATA_FILES.append(('resources/styles', ['resources/styles/default.qss']))
    elif os.path.exists('time-tracker/resources/styles/default.qss'):
        DATA_FILES.append(('resources/styles', ['time-tracker/resources/styles/default.qss']))
except Exception as e:
    print(f"Warning: Could not add styles file: {e}")

# We're not importing jaraco modules here to avoid issues with py2app
# They'll be handled by our custom launcher

OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,  # Make it a background app (appears in menu bar only)
        'CFBundleName': 'Time Tracker',
        'CFBundleDisplayName': 'Time Tracker',
        'CFBundleIdentifier': 'com.ejtracker.timetracker',
        'CFBundleVersion': '1.0.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'ejtk',
        'CFBundleIconFile': 'app_icon.icns',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
    },
    'packages': [
        'rumps', 
        'PyQt6', 
        'time_tracker',
        'time_tracker.bootstrap',
    ],
    'iconfile': 'resources/icons/app_icon.icns',
    'includes': [
        'PyQt6.QtCore', 
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    'frameworks': [],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'pandas', 'wx'],
    # For macOS Sonoma with Python 3.12
    'site_packages': True,
    'qt_plugins': ['platforms', 'styles', 'imageformats'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='Time Tracker',
)