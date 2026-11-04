"""Process brand assets for DuwcsAnhLib
Generates:
- Site Icon Suite: site-icon-512.png, apple-touch-icon.png, favicon-32x32.png, favicon-16x16.png, favicon.ico
- Brand Logo Suite: logo-phoenix-master.png, logo-header.png, logo-header-symbol.png, logo-duwcsanhlib.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import deque

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / 'duwcsanhlib' / 'assets'
RAW_DIR = ASSETS_DIR / 'raw'

def font(name, size):
    fonts_dir = Path("C:/Windows/Fonts")
    p = fonts_dir / name
    if p.exists():
        return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def process_site_icons():
    raw_path = RAW_DIR / 'site_icon_squircle_raw.jpg'
    if not raw_path.exists():
        raise FileNotFoundError(f"Missing {raw_path}")

    im = Image.open(raw_path).convert('RGBA')
    arr = np.array(im)
    h, w, _ = arr.shape

    # Flood fill exterior white background from corners
    visited = np.zeros((h, w), dtype=bool)
    q = deque([(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)])
    for y, x in q:
        visited[y, x] = True

    while q:
        cy, cx = q.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                r, g, b, _ = arr[ny, nx]
                if r > 230 and g > 230 and b > 230:
                    visited[ny, nx] = True
                    q.append((ny, nx))

    # Mask exterior to transparent
    arr[visited, 3] = 0

    # Smooth the boundary transition without scipy
    # Pad visited by 1 pixel in each direction
    padded_v = np.pad(visited, 1, mode='edge')
    adjacent_visited = (
        padded_v[:-2, 1:-1] | padded_v[2:, 1:-1] |
        padded_v[1:-1, :-2] | padded_v[1:-1, 2:]
    )
    border_mask = adjacent_visited & (~visited)
    for y, x in np.argwhere(border_mask):
        r, g, b, _ = arr[y, x]
        brightness = (int(r) + int(g) + int(b)) / 3.0
        if brightness > 220:
            arr[y, x, 3] = int(255 * max(0.0, (255 - brightness) / 35.0))

    # Crop square around squircle center (cx=508, cy=514, size=720)
    cx, cy = 508, 514
    half_s = 360
    cropped = Image.fromarray(arr).crop((cx - half_s, cy - half_s, cx + half_s, cy + half_s))

    # 1. site-icon-512.png
    icon_512 = cropped.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512.save(ASSETS_DIR / 'site-icon-512.png', optimize=True)

    # 2. apple-touch-icon.png (180x180)
    icon_180 = cropped.resize((180, 180), Image.Resampling.LANCZOS)
    icon_180.save(ASSETS_DIR / 'apple-touch-icon.png', optimize=True)

    # 3. favicon-32x32.png
    icon_32 = cropped.resize((32, 32), Image.Resampling.LANCZOS)
    icon_32.save(ASSETS_DIR / 'favicon-32x32.png', optimize=True)

    # 4. favicon-16x16.png
    icon_16 = cropped.resize((16, 16), Image.Resampling.LANCZOS)
    icon_16.save(ASSETS_DIR / 'favicon-16x16.png', optimize=True)

    # 5. favicon.ico
    icon_48 = cropped.resize((48, 48), Image.Resampling.LANCZOS)
    icon_512.save(ASSETS_DIR / 'favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("[OK] Processed Site Icon Suite (512, 180, 32, 16, ico)")

def process_phoenix_logo():
    raw_path = RAW_DIR / 'logo_phoenix_raw.jpg'
    if not raw_path.exists():
        raise FileNotFoundError(f"Missing {raw_path}")

    im = Image.open(raw_path).convert('RGB')
    arr = np.array(im).astype(np.float32)

    # Alpha matting unblending from white
    c_norm = arr / 255.0
    min_c = np.min(c_norm, axis=-1)
    alpha = 1.0 - min_c
    # Clip slight jpeg noise near white
    alpha = np.clip((alpha - 0.035) / (1.0 - 0.035), 0.0, 1.0)

    # Reconstruct foreground
    f_norm = np.zeros_like(c_norm)
    mask = alpha > 0.001
    for i in range(3):
        f_norm[..., i] = np.where(mask, np.clip(1.0 - (1.0 - c_norm[..., i]) / np.maximum(alpha, 1e-5), 0.0, 1.0), 1.0)

    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[..., :3] = (f_norm * 255.0).astype(np.uint8)
    rgba[..., 3] = (alpha * 255.0).astype(np.uint8)

    symbol_im = Image.fromarray(rgba, 'RGBA')
    bbox = symbol_im.getbbox()
    symbol_cropped = symbol_im.crop(bbox) # approx 667x696

    # 1. Master Logo (800x800 square canvas with padding)
    master = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
    # Resize symbol to fit ~740x740
    sym_w, sym_h = symbol_cropped.size
    ratio = min(740 / sym_w, 740 / sym_h)
    new_w = int(sym_w * ratio)
    new_h = int(sym_h * ratio)
    res_sym = symbol_cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    master.paste(res_sym, ((800 - new_w) // 2, (800 - new_h) // 2), res_sym)
    master.save(ASSETS_DIR / 'logo-phoenix-master.png', optimize=True)

    # 2. Header symbol (140x140)
    sym_140 = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ratio_140 = min(130 / sym_w, 130 / sym_h)
    w_140, h_140 = int(sym_w * ratio_140), int(sym_h * ratio_140)
    res_140 = symbol_cropped.resize((w_140, h_140), Image.Resampling.LANCZOS)
    sym_140.paste(res_140, ((140 - w_140) // 2, (140 - h_140) // 2), res_140)
    sym_140.save(ASSETS_DIR / 'logo-header-symbol.png', optimize=True)

    # 3. Horizontal Brand Header Lockup (560x140)
    header_img = Image.new('RGBA', (560, 140), (0, 0, 0, 0))
    # Place symbol on left: height 126px
    h_sym = 126
    w_sym = int(sym_w * (h_sym / sym_h))
    res_header_sym = symbol_cropped.resize((w_sym, h_sym), Image.Resampling.LANCZOS)
    header_img.paste(res_header_sym, (10, (140 - h_sym) // 2), res_header_sym)

    # Text drawing
    d = ImageDraw.Draw(header_img)
    text_x = 10 + w_sym + 18

    # Line 1: DuwcsAnh (Red #C92127) + Lib (Amber #D97706)
    f_title = font('georgiab.ttf', 54)
    d.text((text_x, 14), 'DuwcsAnh', font=f_title, fill='#C92127')
    # calculate width of 'DuwcsAnh'
    w_duwcs = int(d.textlength('DuwcsAnh', font=f_title))
    d.text((text_x + w_duwcs + 2, 14), 'Lib', font=f_title, fill='#D97706')

    # Line 2: Separator bar
    f_sub = font('arialbd.ttf', 13)
    bar_y = 80
    d.line([(text_x, bar_y), (text_x + 360, bar_y)], fill='#E2E8F0', width=1)
    d.line([(text_x, bar_y), (text_x + 80, bar_y)], fill='#D97706', width=2)

    # Line 3: Subtitle
    d.text((text_x, 90), 'HIỆU SÁCH & THƯ VIỆN TRI THỨC', font=f_sub, fill='#334155')

    header_img.save(ASSETS_DIR / 'logo-header.png', optimize=True)

    # Also update logo-duwcsanhlib.png (used by WordPress / Flatsome as the primary logo)
    header_img.save(ASSETS_DIR / 'logo-duwcsanhlib.png', optimize=True)
    print("[OK] Processed Phoenix Logo Suite (master, header, symbol, logo-duwcsanhlib)")

if __name__ == '__main__':
    process_site_icons()
    process_phoenix_logo()
    print("ALL BRAND ASSETS PROCESSED SUCCESSFULLY!")
