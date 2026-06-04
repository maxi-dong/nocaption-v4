from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_icon(name: str, c1: tuple[int, int, int], c2: tuple[int, int, int], label: str):
    size = 1024
    img = Image.new("RGBA", (size, size), c1 + (255,))
    draw = ImageDraw.Draw(img)

    # Vertical gradient background
    for y in range(size):
        t = y / (size - 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Rounded card
    pad = 110
    draw.rounded_rectangle(
        [(pad, pad), (size - pad, size - pad)],
        radius=180,
        fill=(255, 255, 255, 60),
        outline=(255, 255, 255, 255),
        width=14,
    )

    # Core mark
    cx, cy = size // 2, size // 2
    draw.ellipse([(cx - 210, cy - 210), (cx + 210, cy + 210)], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=8)
    draw.ellipse([(cx - 170, cy - 170), (cx + 170, cy + 170)], fill=(20, 30, 45, 255))

    # Label text
    big = load_font(190)
    small = load_font(74)
    text_main = label
    text_sub = "NOCAPTION"

    box_main = draw.textbbox((0, 0), text_main, font=big)
    w_main = box_main[2] - box_main[0]
    h_main = box_main[3] - box_main[1]
    draw.text((cx - w_main // 2, cy - h_main // 2 - 40), text_main, fill=(245, 252, 255, 255), font=big)

    box_sub = draw.textbbox((0, 0), text_sub, font=small)
    w_sub = box_sub[2] - box_sub[0]
    draw.text((cx - w_sub // 2, cy + 170), text_sub, fill=(240, 246, 252, 255), font=small)

    img.save(OUT / f"{name}.png", format="PNG")


def main():
    make_icon("nocaption_v1_1024", (23, 83, 192), (96, 165, 250), "V1")
    make_icon("nocaption_v2_1024", (22, 101, 52), (34, 197, 94), "V2")


if __name__ == "__main__":
    main()
