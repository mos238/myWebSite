from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple icon
img = Image.new('RGB', (128, 128), color='#667eea')
draw = ImageDraw.Draw(img)
draw.text((40, 50), "📥", fill='white', size=80)
img.save('m3u8_icon.png')
print("Icon created")
