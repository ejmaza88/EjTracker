#!/usr/bin/env python3
"""
Application launcher script for Time Tracker.
This script is specifically designed to be used as the entry point for py2app builds
to ensure all dependencies are properly loaded.
"""
import os
import sys
import importlib

def preload_modules():
    """Pre-load potentially problematic modules."""
    modules_to_preload = [
        'importlib_metadata',
        'jaraco.functools',
        'jaraco.collections',
        'jaraco.context',
        'jaraco.text',
        'more_itertools',
        'zipp',
        'platformdirs',
        'packaging',
    ]
    
    for module in modules_to_preload:
        try:
            importlib.import_module(module)
            print(f"Pre-loaded {module}")
        except ImportError as e:
            print(f"Warning: Could not pre-load {module}: {e}")

def main():
    """Main entry point for the application."""
    # Set up the Python path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    
    # Pre-load problematic modules
    preload_modules()
    
    # Import and run the actual application
    try:
        from time_tracker.main import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing the main application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
