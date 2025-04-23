#!/bin/bash
# Script to build the Time Tracker macOS application for macOS Sonoma and Python 3.12

echo "Building Time Tracker macOS application for macOS Sonoma and Python 3.12..."

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Ensure all dependencies are installed
echo "Installing dependencies..."
pip install --upgrade pip
pip install --upgrade rumps
pip install --upgrade PyQt6>=6.5.0

# Install the dependencies needed for proper packaging with pkg_resources
echo "Installing packaging dependencies..."
pip install --upgrade jaraco.text
pip install --upgrade jaraco.functools
pip install --upgrade jaraco.collections
pip install --upgrade importlib_metadata
pip install --upgrade zipp

# Install the most recent version of py2app that works with Python 3.12
echo "Installing compatible py2app version..."
pip install --upgrade py2app==0.28.8

# Clean up previous builds thoroughly
echo "Cleaning up previous builds..."
rm -rf build dist
rm -rf *.egg-info
rm -rf src/time_tracker.egg-info
rm -rf src/time_tracker/__pycache__
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Copy the style file if it exists in the alternative location
if [ -f "time-tracker/resources/styles/default.qss" ] && [ ! -f "resources/styles/default.qss" ]; then
    echo "Copying styles from time-tracker directory..."
    mkdir -p resources/styles
    cp time-tracker/resources/styles/default.qss resources/styles/
fi

# Set some environment variables for macOS Sonoma compatibility
export SYSTEM_VERSION_COMPAT=0
export MACOSX_DEPLOYMENT_TARGET=14.0

# Build the application with py2app - alias mode first for testing
echo "Building macOS application in alias mode for testing..."
python setup_macos.py py2app -A

# Test if application works in alias mode
echo "Testing application in alias mode..."
if [ -f "dist/Time Tracker.app/Contents/MacOS/Time Tracker" ]; then
    echo "Alias mode application built successfully."
    echo "Now building the final standalone application..."
    
    # Clean up the alias mode build
    rm -rf build dist
    
    # Build the standalone application
    python setup_macos.py py2app

    # Sign the application (helps with macOS permissions)
    if [ -d "dist/Time Tracker.app" ]; then
        echo "Signing the application..."
        codesign --force --deep --sign - "dist/Time Tracker.app"
        
        # Ensure the app is executable
        echo "Ensuring app is executable..."
        chmod -R +x "dist/Time Tracker.app"
        
        echo "Build complete! The application is now available in the 'dist' folder."
        echo "You can move 'Time Tracker.app' to your Applications folder."
        
        # Create a debug launcher script
        echo "Creating debug launcher..."
        cat > dist/debug_launch.sh << 'EOF'
#!/bin/bash
# Launch the Time Tracker app with debug output
echo "Launching Time Tracker with debug output..."
cd "$(dirname "$0")"
"./Time Tracker.app/Contents/MacOS/Time Tracker" 2>&1 | tee ~/time_tracker_debug.log
EOF
        chmod +x dist/debug_launch.sh
        
        echo "For debugging, run the dist/debug_launch.sh script."
    else
        echo "Error: Failed to build standalone application."
        exit 1
    fi
else
    echo "Error: Failed to build application in alias mode."
    exit 1
fi