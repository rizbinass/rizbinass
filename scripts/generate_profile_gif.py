from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "rizbinass-mario.gif"

W, H = 320, 160
SCALE = 3
FRAMES = 132
GROUND_Y = 132
ENEMY_X = 265


TECHS = [
    ("React", "#61dafb"),
    ("TypeScript", "#3178c6"),
    ("JavaScript", "#f7df1e"),
    ("Tailwind", "#38bdf8"),
    ("Figma", "#a259ff"),
    ("Framer", "#0055ff"),
]


def font(size, bold=False):
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT_TINY = font(5, True)
FONT_SMALL = font(7, True)
FONT_MED = font(10, True)
FONT_BIG = font(17, True)


def rect(d, xy, fill, outline="#111111", width=1):
    d.rectangle(xy, fill=fill, outline=outline, width=width)


def text_shadow(d, xy, text, fnt, fill="#fff5d6", shadow="#111111"):
    x, y = xy
    d.text((x + 2, y + 2), text, font=fnt, fill=shadow)
    d.text((x, y), text, font=fnt, fill=fill)


def centered_shadow(d, box, text, fnt, fill="#fff5d6", shadow="#111111"):
    left, top, right, bottom = box
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = left + (right - left - tw) // 2
    y = top + (bottom - top - th) // 2 - 2
    text_shadow(d, (x, y), text, fnt, fill, shadow)


def draw_cloud(d, x, y, scale=1):
    fill = "#f8ffff"
    edge = "#111111"
    blue = "#22d3ee"
    parts = [
        (x, y + 8, x + 17 * scale, y + 18 * scale),
        (x + 8 * scale, y + 3 * scale, x + 24 * scale, y + 18 * scale),
        (x + 21 * scale, y + 6 * scale, x + 38 * scale, y + 18 * scale),
        (x + 35 * scale, y + 10 * scale, x + 52 * scale, y + 18 * scale),
    ]
    for p in parts:
        d.ellipse(p, fill=fill, outline=edge, width=1)
    d.rectangle((x + 6 * scale, y + 12 * scale, x + 46 * scale, y + 20 * scale), fill=fill)
    d.line((x + 9 * scale, y + 18 * scale, x + 43 * scale, y + 18 * scale), fill=blue, width=1)


def draw_hill(d, x, y, w, h, color):
    pts = [(x, y + h), (x + w // 2, y), (x + w, y + h)]
    d.polygon(pts, fill=color, outline="#111111")
    d.rectangle((x, y + h - 1, x + w, y + h + 3), fill=color)
    for ox in (w * 0.35, w * 0.62):
        d.rectangle((int(x + ox), y + h // 3, int(x + ox + 2), y + h // 3 + 5), fill="#111111")


def draw_bush(d, x, y, color="#9de14a"):
    for i in range(4):
        d.ellipse((x + i * 13, y + (i % 2) * 2, x + 20 + i * 13, y + 21), fill=color, outline="#111111")
    d.rectangle((x + 4, y + 14, x + 62, y + 23), fill=color)


def draw_ground(d):
    for x in range(0, W, 16):
        for y in range(GROUND_Y, H, 16):
            rect(d, (x, y, x + 15, y + 15), "#dd5217")
            d.line((x + 2, y + 4, x + 14, y + 4), fill="#ffb270")
            d.line((x + 8, y, x + 8, y + 15), fill="#111111")
            d.line((x, y + 11, x + 15, y + 11), fill="#111111")


def draw_question_block(d, x, y, bump=0):
    y -= bump
    rect(d, (x, y, x + 14, y + 14), "#f39a3d")
    d.rectangle((x + 2, y + 2, x + 12, y + 12), outline="#f7c97a")
    d.text((x + 4, y + 1), "?", font=FONT_MED, fill="#111111")
    d.point((x + 2, y + 2), fill="#111111")
    d.point((x + 12, y + 12), fill="#111111")


def draw_title(d):
    rect(d, (98, 10, 223, 71), "#dc4b13", outline="#7b250b", width=2)
    d.rectangle((101, 13, 220, 68), outline="#ffb481")
    for p in [(101, 13), (220, 13), (101, 68), (220, 68)]:
        d.ellipse((p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1), fill="#fff5d6", outline="#111111")
    d.text((111, 17), "Bekasi, IDN", font=FONT_SMALL, fill="#fff5d6")
    centered_shadow(d, (104, 31, 218, 62), "RIZBINASS", FONT_BIG)


def draw_player(d, x, y, step, hurt=False):
    if hurt:
        d.rectangle((x + 3, y + 20, x + 16, y + 26), fill="#e24a25", outline="#111111")
        d.rectangle((x + 1, y + 12, x + 12, y + 20), fill="#f4b169", outline="#111111")
        d.rectangle((x - 1, y + 10, x + 12, y + 14), fill="#d73320", outline="#111111")
        d.rectangle((x + 7, y + 14, x + 8, y + 15), fill="#111111")
        d.line((x + 15, y + 11, x + 20, y + 7), fill="#f4b169", width=2)
        d.line((x + 15, y + 24, x + 21, y + 28), fill="#4d79d8", width=2)
        return

    leg = 2 if step % 2 == 0 else -1
    d.rectangle((x + 5, y + 11, x + 12, y + 23), fill="#e24a25", outline="#111111")
    d.rectangle((x + 3, y + 4, x + 13, y + 12), fill="#f4b169", outline="#111111")
    d.rectangle((x + 1, y + 2, x + 13, y + 6), fill="#d73320", outline="#111111")
    d.rectangle((x + 6, y, x + 16, y + 3), fill="#d73320", outline="#111111")
    d.rectangle((x + 11, y + 6, x + 12, y + 7), fill="#111111")
    d.rectangle((x + 1, y + 12, x + 4, y + 16), fill="#f4b169", outline="#111111")
    d.rectangle((x + 13, y + 12, x + 16, y + 16), fill="#f4b169", outline="#111111")
    d.rectangle((x + 4, y + 23, x + 8, y + 27 + leg), fill="#4d79d8", outline="#111111")
    d.rectangle((x + 10, y + 23, x + 14, y + 27 - leg), fill="#4d79d8", outline="#111111")


def draw_enemy(d, x, y):
    d.ellipse((x, y, x + 17, y + 16), fill="#c95620", outline="#111111")
    d.rectangle((x + 2, y + 9, x + 15, y + 18), fill="#e88b44", outline="#111111")
    d.rectangle((x + 5, y + 6, x + 6, y + 8), fill="#111111")
    d.rectangle((x + 11, y + 6, x + 12, y + 8), fill="#111111")
    d.rectangle((x + 4, y + 18, x + 8, y + 20), fill="#111111")
    d.rectangle((x + 10, y + 18, x + 14, y + 20), fill="#111111")


def draw_logo(d, name, color, cx, cy):
    r = 12
    tile_fill = "#050505" if name == "React" else "#fff7dd"
    d.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), radius=2, fill=tile_fill, outline="#111111", width=1)
    ix = cx
    if name == "React":
        d.ellipse((ix - 9, cy - 4, ix + 9, cy + 4), outline=color, width=2)
        d.arc((ix - 7, cy - 10, ix + 7, cy + 10), 35, 325, fill=color, width=2)
        d.arc((ix - 7, cy - 10, ix + 7, cy + 10), 215, 145, fill=color, width=2)
        d.ellipse((ix - 2, cy - 2, ix + 2, cy + 2), fill=color)
    elif name == "TypeScript":
        rect(d, (ix - 10, cy - 10, ix + 10, cy + 10), "#3178c6")
        d.text((ix - 8, cy - 6), "TS", font=FONT_MED, fill="#ffffff")
    elif name == "JavaScript":
        rect(d, (ix - 10, cy - 10, ix + 10, cy + 10), "#f7df1e")
        d.text((ix - 8, cy - 6), "JS", font=FONT_MED, fill="#111111")
    elif name == "Tailwind":
        d.arc((ix - 10, cy - 7, ix + 2, cy + 5), 190, 350, fill="#38bdf8", width=3)
        d.arc((ix - 2, cy - 2, ix + 10, cy + 10), 190, 350, fill="#0ea5e9", width=3)
    elif name == "Figma":
        colors = ["#f24e1e", "#ff7262", "#a259ff", "#1abcfe", "#0acf83"]
        pts = [(ix - 4, cy - 7), (ix + 3, cy - 7), (ix - 4, cy), (ix + 3, cy), (ix - 4, cy + 7)]
        for (px, py), c in zip(pts, colors):
            d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=c)
    else:
        d.polygon([(ix - 8, cy - 10), (ix + 8, cy - 10), (ix, cy - 2), (ix + 8, cy - 2), (ix - 8, cy + 10)], fill="#050505")


def player_position(i):
    stand_y = GROUND_Y - 28
    if i < 28:
        return 91 + i * 1.45, stand_y, False
    if i < 43:
        t = (i - 28) / 15
        x = 132 + t * 17
        y = stand_y - sin(t * pi) * 8
        return x, y, False
    if i < 116:
        return 149 + (i - 43) * 1.38, stand_y, False
    if i < 124:
        return 246, stand_y + min(7, i - 116), True
    return 246, stand_y + 7, True


def render_frame(i):
    img = Image.new("RGB", (W, H), "#9fa8ff")
    d = ImageDraw.Draw(img)

    draw_cloud(d, 13, 9, 1)
    draw_cloud(d, 45, 84, 1)
    draw_cloud(d, 290, 3, 1)
    draw_hill(d, -16, 104, 64, 36, "#26b900")
    draw_hill(d, 198, 116, 45, 19, "#27b000")
    draw_bush(d, 132, 121)
    draw_bush(d, 290, 121)
    draw_title(d)

    draw_question_block(d, 263, 28)
    for x, y, is_q in [(244, 82, False), (259, 82, True), (274, 82, False), (289, 82, True), (304, 82, False)]:
        if is_q:
            draw_question_block(d, x, y)
        else:
            rect(d, (x, y, x + 14, y + 14), "#cd4318")
            d.line((x, y + 5, x + 14, y + 5), fill="#111111")
            d.line((x + 7, y, x + 7, y + 14), fill="#111111")

    bump = max(0, int(5 - abs(i - 40))) if 36 <= i <= 44 else 0
    draw_question_block(d, 145, 82, bump)
    if i >= 39:
        tech = TECHS[((i - 39) // 9) % len(TECHS)]
        bob = int(sin(i / 3) * 2)
        draw_logo(d, tech[0], tech[1], 152, 74 + bob)

    draw_ground(d)
    draw_enemy(d, ENEMY_X, 112)
    px, py, hurt = player_position(i)
    draw_player(d, int(px), int(py), i // 6, hurt=hurt)
    if hurt:
        d.line((263, 112, 267, 108), fill="#ffd166", width=1)
        d.line((267, 112, 263, 108), fill="#ffd166", width=1)
        d.point((266, 107), fill="#ffffff")

    if 38 <= i <= 43:
        d.text((160, 75 - bump), "+", font=FONT_SMALL, fill="#fff7dd")

    return img.resize((W * SCALE, H * SCALE), Image.Resampling.NEAREST)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [render_frame(i).convert("P", palette=Image.Palette.ADAPTIVE, colors=128) for i in range(FRAMES)]
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
