from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "rizbinass-mario.gif"

W, H = 320, 160
SCALE = 3
FRAMES = 96
GROUND_Y = 132


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
FONT_BIG = font(22, True)


def rect(d, xy, fill, outline="#111111", width=1):
    d.rectangle(xy, fill=fill, outline=outline, width=width)


def text_shadow(d, xy, text, fnt, fill="#fff5d6", shadow="#111111"):
    x, y = xy
    d.text((x + 2, y + 2), text, font=fnt, fill=shadow)
    d.text((x, y), text, font=fnt, fill=fill)


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
    text_shadow(d, (111, 30), "RIZBINASS", FONT_BIG)


def draw_player(d, x, y, step):
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
    d.rounded_rectangle((cx - 43, cy - 16, cx + 43, cy + 16), radius=3, fill="#fff7dd", outline="#111111", width=1)
    ix = cx - 19
    if name == "React":
        for r in (0, 60, -60):
            d.ellipse((ix - 14, cy - 6, ix + 14, cy + 6), outline=color, width=2)
        d.ellipse((ix - 3, cy - 3, ix + 3, cy + 3), fill=color)
    elif name == "TypeScript":
        rect(d, (ix - 12, cy - 12, ix + 12, cy + 12), color)
        d.text((ix - 7, cy - 7), "TS", font=FONT_MED, fill="#ffffff")
    elif name == "JavaScript":
        rect(d, (ix - 12, cy - 12, ix + 12, cy + 12), color)
        d.text((ix - 7, cy - 7), "JS", font=FONT_MED, fill="#111111")
    elif name == "Tailwind":
        d.arc((ix - 14, cy - 8, ix + 2, cy + 8), 190, 350, fill=color, width=3)
        d.arc((ix - 1, cy - 8, ix + 15, cy + 8), 190, 350, fill="#0ea5e9", width=3)
    elif name == "Figma":
        colors = ["#f24e1e", "#ff7262", "#a259ff", "#1abcfe", "#0acf83"]
        pts = [(ix - 5, cy - 9), (ix + 3, cy - 9), (ix - 5, cy), (ix + 3, cy), (ix - 5, cy + 9)]
        for (px, py), c in zip(pts, colors):
            d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=c, outline="#111111")
    else:
        d.polygon([(ix - 11, cy - 12), (ix + 10, cy - 12), (ix - 1, cy), (ix + 10, cy), (ix - 11, cy + 12)], fill=color, outline="#111111")
    d.text((cx - 2, cy - 4), name, font=FONT_SMALL, fill="#111111")


def player_position(i):
    if i < 24:
        return 93 + i * 1.6, GROUND_Y - 28
    if i < 42:
        t = (i - 24) / 18
        x = 131 + t * 18
        y = GROUND_Y - 28 - sin(t * pi) * 38
        return x, y
    return 149 + (i - 42) * 0.22, GROUND_Y - 28


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
    if i >= 38:
        tech = TECHS[((i - 38) // 9) % len(TECHS)]
        bob = int(sin(i / 3) * 2)
        draw_logo(d, tech[0], tech[1], 152, 63 + bob)

    draw_ground(d)
    draw_enemy(d, 252, 112)
    px, py = player_position(i)
    draw_player(d, int(px), int(py), i // 6)

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
