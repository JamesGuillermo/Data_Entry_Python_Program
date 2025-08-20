from PIL import Image, ImageDraw

# Constants
DPI = 300
LETTER_WIDTH_IN = 8.5
LETTER_HEIGHT_IN = 11

POSTCARD_WIDTH_IN = 3.9
POSTCARD_HEIGHT_IN = 5.8

# Convert to pixels
letter_width_px = int(LETTER_WIDTH_IN * DPI)
letter_height_px = int(LETTER_HEIGHT_IN * DPI)

postcard_width_px = int(POSTCARD_WIDTH_IN * DPI)
postcard_height_px = int(POSTCARD_HEIGHT_IN * DPI)

# Create a white background image
img = Image.new("RGB", (letter_width_px, letter_height_px), "white")
draw = ImageDraw.Draw(img)

# Draw gridlines
# Vertical line to split the page across the width
draw.line((postcard_width_px, 0, postcard_width_px, letter_height_px), fill="black", width=2)

# Horizontal line to show height of postcard
draw.line((0, postcard_height_px, letter_width_px, postcard_height_px), fill="black", width=2)

# Save the image
img.save("letter_with_postcard_grid_2up.png", dpi=(DPI, DPI))
