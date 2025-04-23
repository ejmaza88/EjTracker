from PIL import Image, ImageDraw
import os

# Create the icons directory if it doesn't exist
os.makedirs("resources/icons/menubar", exist_ok=True)

# Function to create an icon
def create_icon(filename, draw_function, background=(0, 0, 0, 0)):
    # Create a transparent image (22x22 is good for menubar)
    img = Image.new('RGBA', (22, 22), background)
    draw = ImageDraw.Draw(img)
    
    # Call the drawing function
    draw_function(draw)
    
    # Save the image
    img.save(f"resources/icons/menubar/{filename}.png")
    print(f"Created {filename}.png")

# Create play icon
def draw_play(draw):
    # Draw a play triangle
    draw.polygon([(7, 5), (7, 17), (17, 11)], fill=(50, 50, 50, 255))

# Create stop icon
def draw_stop(draw):
    # Draw a stop square
    draw.rectangle([(7, 7), (15, 15)], fill=(50, 50, 50, 255))

# Create the icons
create_icon("play", draw_play)
create_icon("stop", draw_stop)
