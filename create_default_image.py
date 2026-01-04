#!/usr/bin/env python
"""Create a default profile image"""
import os
from PIL import Image, ImageDraw, ImageFont

# Create media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media')
os.makedirs(media_dir, exist_ok=True)

# Create a simple default profile image
img = Image.new('RGB', (200, 200), color=(100, 149, 237))  # Cornflower blue
draw = ImageDraw.Draw(img)

# Draw a simple user icon (circle)
draw.ellipse([50, 40, 150, 140], fill=(255, 255, 255))  # Head
draw.ellipse([60, 140, 140, 200], fill=(255, 255, 255))  # Body

# Save the image
img.save(os.path.join(media_dir, 'default.jpg'), 'JPEG')
print('✅ Created default.jpg profile image')
