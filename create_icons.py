#!/usr/bin/env python3
"""
Script to create macOS app icons (.icns file) from a PNG image.
This script requires the following dependencies:
- pillow (PIL)
"""
import os
import sys
import subprocess
from PIL import Image

def create_icns(png_file, output_dir):
    """Create an .icns file from a PNG image"""
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a temporary iconset directory
    iconset_dir = os.path.join(output_dir, "app.iconset")
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # Open the original image
    img = Image.open(png_file)
    
    # Define the sizes needed for macOS iconset
    icon_sizes = [
        (16, "16x16.png"),
        (32, "16x16@2x.png"),  # High DPI (Retina)
        (32, "32x32.png"),
        (64, "32x32@2x.png"),  # High DPI (Retina)
        (128, "128x128.png"),
        (256, "128x128@2x.png"),  # High DPI (Retina)
        (256, "256x256.png"),
        (512, "256x256@2x.png"),  # High DPI (Retina)
        (512, "512x512.png"),
        (1024, "512x512@2x.png"),  # High DPI (Retina)
    ]
    
    # Create each size and save to the iconset directory
    for size, filename in icon_sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_dir, f"icon_{filename}"))
    
    # Use iconutil to convert the iconset to icns
    icns_file = os.path.join(output_dir, "app_icon.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_file], check=True)
    
    # Clean up the temporary iconset directory
    subprocess.run(["rm", "-rf", iconset_dir])
    
    print(f"Icon created successfully at: {icns_file}")
    return icns_file

if __name__ == "__main__":
    # Default to using the play icon if no arguments provided
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir  # We're already in the root directory
    png_file = os.path.join(base_dir, "resources", "icons", "menubar", "play.png")
    output_dir = os.path.join(base_dir, "resources", "icons")
    
    # Use command line argument if provided
    if len(sys.argv) > 1:
        png_file = sys.argv[1]
    
    # Install required dependencies if not present
    try:
        import PIL
    except ImportError:
        print("Installing required dependency: pillow")
        subprocess.run(["pip", "install", "pillow"], check=True)
        
    create_icns(png_file, output_dir)
