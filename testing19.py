from PIL import Image, ImageDraw

# Constants
DPI = 300
LETTER_WIDTH_IN = 8.5
LETTER_HEIGHT_IN = 11

# Convert to pixels
letter_width_px = int(LETTER_WIDTH_IN * DPI)
letter_height_px = int(LETTER_HEIGHT_IN * DPI)

# Create a white background image
img = Image.new("RGB", (letter_width_px, letter_height_px), "white")
draw = ImageDraw.Draw(img)

# Calculate center points
half_width = letter_width_px // 2
half_height = letter_height_px // 2

# Draw vertical center line
draw.line((half_width, 0, half_width, letter_height_px), fill="black", width=2)

# Draw horizontal center line
draw.line((0, half_height, letter_width_px, half_height), fill="black", width=2)

# Save the image
img.save("letter_divided_into_4_sections.png", dpi=(DPI, DPI))
