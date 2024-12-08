from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a transparent background
size = (200, 200)
image = Image.new('RGBA', size, (255, 255, 255, 0))

# Create a drawing context
draw = ImageDraw.Draw(image)

# Draw a banana shape
# Curved yellow banana
draw.ellipse([50, 50, 150, 150], fill=(255, 215, 0, 255))  # Golden yellow
draw.arc([50, 50, 150, 150], 0, 180, fill=(210, 180, 50, 255), width=10)

# Add a brown stem
draw.line([100, 30, 100, 50], fill=(139, 69, 19, 255), width=5)

# Save the image
output_dir = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(output_dir, exist_ok=True)
image.save(os.path.join(output_dir, 'banana_icon.png'))

print("Banana icon created successfully!")
