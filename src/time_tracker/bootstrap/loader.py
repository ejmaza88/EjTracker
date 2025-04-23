"""
Bootstrap loader for handling imports before the main application starts.
This ensures dependencies are properly loaded, particularly for macOS py2app builds.
"""
import sys
import importlib

def ensure_imports():
    """
    Pre-import problematic modules to ensure they're loaded correctly
    before the application starts.
    """
    # List of modules that need to be pre-loaded
    modules = [
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
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"Successfully pre-loaded {module}")
        except ImportError as e:
            print(f"Warning: Could not pre-load {module}: {e}")

def patch_sys_path():
    """
    Add any necessary paths to sys.path to ensure all modules can be found.
    """
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add the parent directory to sys.path if it's not already there
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

def initialize():
    """
    Initialize the bootstrap process before the main application starts.
    """
    patch_sys_path()
    ensure_imports()
    
    # Return success status
    return True
