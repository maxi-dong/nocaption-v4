from pathlib import Path
from PIL import Image

base = Path('/Users/sany/Documents/gmvcodex/nocaption_app/assets/icons/nocaption_v1_1024.png')
out = Path('/Users/sany/Documents/gmvcodex/nocaption_app/assets/icons/nocaption_v1_pil.iconset')
out.mkdir(parents=True, exist_ok=True)
img = Image.open(base).convert('RGBA')

sizes = [
    ('icon_16x16.png', 16),
    ('icon_16x16@2x.png', 32),
    ('icon_32x32.png', 32),
    ('icon_32x32@2x.png', 64),
    ('icon_128x128.png', 128),
    ('icon_128x128@2x.png', 256),
    ('icon_256x256.png', 256),
    ('icon_256x256@2x.png', 512),
    ('icon_512x512.png', 512),
    ('icon_512x512@2x.png', 1024),
]
for name, px in sizes:
    resized = img.resize((px, px), Image.Resampling.LANCZOS)
    resized.save(out / name, format='PNG')
print('done')
