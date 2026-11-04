"""Generate authentic, publication-quality graphic book covers without any AI placeholder text.
Realistic book jacket design: elegant serif typography, artistic ornamentation, rich color schemes,
spine depth shading, and official publisher branding (Nhà xuất bản Trẻ).
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path("D:/VSCode/HKDN/BookVerse")
OUT_DIR = ROOT / "duwcsanhlib/assets/covers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

fontdir = Path('C:/Windows/Fonts')
def font(name, size):
    path = fontdir / name
    if not path.exists():
        path = fontdir / 'georgia.ttf'
    return ImageFont.truetype(str(path), size)

def wrapped_text(draw, text, f, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if cur and draw.textlength(test, font=f) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

# Color palettes by book theme
THEMES = {
    'DAL-001': {'bg': '#2C3E50', 'bg2': '#1A252F', 'gold': '#F1C40F', 'accent': '#E74C3C', 'motif': 'house'},
    'DAL-002': {'bg': '#1B4F72', 'bg2': '#0B2545', 'gold': '#5DADE2', 'accent': '#F39C12', 'motif': 'sea'},
    'DAL-003': {'bg': '#4A235A', 'bg2': '#2E1139', 'gold': '#D7BDE2', 'accent': '#E59866', 'motif': 'bridge'},
    'DAL-004': {'bg': '#145A32', 'bg2': '#0B331C', 'gold': '#F4D03F', 'accent': '#58D68D', 'motif': 'globe'},
    'DAL-005': {'bg': '#6E2C00', 'bg2': '#3E1900', 'gold': '#EDBB99', 'accent': '#E67E22', 'motif': 'gate'},
    'DAL-006': {'bg': '#1C2833', 'bg2': '#0E141B', 'gold': '#F39C12', 'accent': '#2ECC71', 'motif': 'trophy'},
    'DAL-007': {'bg': '#1B2631', 'bg2': '#17202A', 'gold': '#E74C3C', 'accent': '#BB8FCE', 'motif': 'scale'},
    'DAL-008': {'bg': '#512E5F', 'bg2': '#2C1736', 'gold': '#F5B041', 'accent': '#AF7AC5', 'motif': 'bell'},
    'DAL-009': {'bg': '#283747', 'bg2': '#1B242F', 'gold': '#48C9B0', 'accent': '#F39C12', 'motif': 'mask'},
    'DAL-010': {'bg': '#0E6251', 'bg2': '#07332A', 'gold': '#F9E79F', 'accent': '#48C9B0', 'motif': 'growth'},
    'DAL-011': {'bg': '#154360', 'bg2': '#0B2535', 'gold': '#52BE80', 'accent': '#F4D03F', 'motif': 'chart'},
    'DAL-012': {'bg': '#5B2C6F', 'bg2': '#331940', 'gold': '#F8C471', 'accent': '#85C1E9', 'motif': 'eye'},
    'DAL-013': {'bg': '#641E16', 'bg2': '#3D120D', 'gold': '#FAD7A0', 'accent': '#F1948A', 'motif': 'heart'},
    'DAL-014': {'bg': '#186A3B', 'bg2': '#0D3820', 'gold': '#F9E79F', 'accent': '#7DCEA0', 'motif': 'river'},
    'DAL-015': {'bg': '#17202A', 'bg2': '#0B1015', 'gold': '#E67E22', 'accent': '#3498DB', 'motif': 'gears'},
    'DAL-016': {'bg': '#1F618D', 'bg2': '#11354D', 'gold': '#FADBD8', 'accent': '#A9DFBF', 'motif': 'lotus'},
    'DAL-017': {'bg': '#2E4053', 'bg2': '#1A242F', 'gold': '#F39C12', 'accent': '#E74C3C', 'motif': 'prism'},
    'DAL-018': {'bg': '#34495E', 'bg2': '#1D2A37', 'gold': '#A3E4D7', 'accent': '#FAD7A0', 'motif': 'leaf'},
    'DAL-019': {'bg': '#4A235A', 'bg2': '#271131', 'gold': '#F8C471', 'accent': '#D2B4DE', 'motif': 'compass'},
    'DAL-020': {'bg': '#196F3D', 'bg2': '#0C381F', 'gold': '#F7DC6F', 'accent': '#82E0AA', 'motif': 'sun'},
    'DAL-021': {'bg': '#78281F', 'bg2': '#421611', 'gold': '#F9E79F', 'accent': '#E74C3C', 'motif': 'lantern'},
    'DAL-022': {'bg': '#1B4F72', 'bg2': '#0E2E44', 'gold': '#FAD7A0', 'accent': '#5499C7', 'motif': 'boat'},
    'DAL-023': {'bg': '#B03A2E', 'bg2': '#692019', 'gold': '#F9E79F', 'accent': '#FADBD8', 'motif': 'hands'},
    'DAL-024': {'bg': '#117864', 'bg2': '#094539', 'gold': '#F8C471', 'accent': '#73C6B6', 'motif': 'palette'},
    'DAL-025': {'bg': '#2874A6', 'bg2': '#16405B', 'gold': '#F9E79F', 'accent': '#85C1E9', 'motif': 'telescope'}
}

import json
books = json.loads((ROOT / "duwcsanhlib/data/books.json").read_text(encoding="utf-8"))

for b in books:
    sku = b['sku']
    theme = THEMES.get(sku, {'bg': '#1C2833', 'bg2': '#0E141B', 'gold': '#F39C12', 'accent': '#2ECC71', 'motif': 'book'})
    
    # 600 x 900 Canvas
    W, H = 600, 900
    im = Image.new('RGB', (W, H), theme['bg'])
    d = ImageDraw.Draw(im)
    
    # Vertical gradient
    for y in range(H):
        r1, g1, b1 = tuple(int(theme['bg'][i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(theme['bg2'][i:i+2], 16) for i in (1, 3, 5))
        ratio = y / H
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        blue = int(b1 * (1 - ratio) + b2 * ratio)
        d.line([(0, y), (W, y)], fill=(r, g, blue))
    
    # Double Golden Framing (Authentic Book Border)
    frame_color = theme['gold']
    d.rectangle([25, 25, W - 25, H - 25], outline=frame_color, width=3)
    d.rectangle([35, 35, W - 35, H - 35], outline=frame_color, width=1)
    
    # Corner flourishes (small squares / diamonds)
    for cx, cy in [(35, 35), (W - 35, 35), (35, H - 35), (W - 35, H - 35)]:
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=frame_color)
    
    # Top: Author Name (Centered, Tracking Serif)
    author_str = b['author'].upper()
    f_author = font('georgiab.ttf', 20)
    w_author = d.textlength(author_str, font=f_author)
    d.text(((W - w_author) / 2, 70), author_str, font=f_author, fill=theme['gold'])
    
    # Ornamental divider under author
    d.line([(W/2 - 50, 105), (W/2 + 50, 105)], fill=theme['gold'], width=2)
    d.ellipse([(W/2 - 4, 103), (W/2 + 4, 107)], fill=theme['gold'])

    # Central Box for Title
    title_str = b['title']
    f_title = font('georgiab.ttf', 38)
    title_lines = wrapped_text(d, title_str, f_title, 480)
    if len(title_lines) > 4:
        f_title = font('georgiab.ttf', 30)
        title_lines = wrapped_text(d, title_str, f_title, 480)
    elif len(title_lines) > 2:
        f_title = font('georgiab.ttf', 34)
        title_lines = wrapped_text(d, title_str, f_title, 480)
    
    total_title_h = len(title_lines) * 48
    start_y = 220 + (180 - total_title_h) / 2
    
    for i, line in enumerate(title_lines):
        line_w = d.textlength(line, font=f_title)
        # Drop shadow for luxury feel
        d.text(((W - line_w) / 2 + 2, start_y + i * 48 + 2), line, font=f_title, fill='#0B1015')
        d.text(((W - line_w) / 2, start_y + i * 48), line, font=f_title, fill='#FFFFFF')

    # Subtitle / Category
    cat_str = f"— {b['category'].upper()} —"
    f_cat = font('georgia.ttf', 16)
    w_cat = d.textlength(cat_str, font=f_cat)
    d.text(((W - w_cat) / 2, start_y + len(title_lines) * 48 + 25), cat_str, font=f_cat, fill=theme['accent'])

    # Artistic Center Medallion / Illustration geometry
    mid_y = 560
    # Outer circle
    d.ellipse([(W/2 - 80, mid_y - 80), (W/2 + 80, mid_y + 80)], outline=theme['gold'], width=2)
    d.ellipse([(W/2 - 70, mid_y - 70), (W/2 + 70, mid_y + 70)], outline=theme['accent'], width=1)
    
    # Geometric Diamond motif
    d.polygon([(W/2, mid_y - 50), (W/2 + 50, mid_y), (W/2, mid_y + 50), (W/2 - 50, mid_y)], outline=theme['gold'], width=2)
    d.ellipse([(W/2 - 15, mid_y - 15), (W/2 + 15, mid_y + 15)], fill=theme['gold'])

    # Bottom Seal & Publisher: NHÀ XUẤT BẢN TRẺ
    f_pub = font('georgiab.ttf', 18)
    pub_str = "NHÀ XUẤT BẢN TRẺ"
    w_pub = d.textlength(pub_str, font=f_pub)
    d.line([(W/2 - 100, 770), (W/2 + 100, 770)], fill=theme['gold'], width=1)
    d.text(((W - w_pub) / 2, 790), pub_str, font=f_pub, fill='#FFFFFF')
    
    f_sub = font('georgia.ttf', 13)
    sub_str = f"Ấn bản {b['year']}  •  Khổ {b['size']}"
    w_sub = d.textlength(sub_str, font=f_sub)
    d.text(((W - w_sub) / 2, 822), sub_str, font=f_sub, fill='#BDC3C7')

    # Realistic 3D Book Spine Shadow on left (50px wide)
    spine_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_spine = ImageDraw.Draw(spine_overlay)
    for x in range(35):
        alpha = int(120 * (1 - x / 35))
        d_spine.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
    # Soft right highlight
    for x in range(35, 45):
        alpha = int(40 * (1 - abs(x - 40) / 5))
        d_spine.line([(x, 0), (x, H)], fill=(255, 255, 255, alpha))
        
    im = Image.alpha_composite(im.convert('RGBA'), spine_overlay).convert('RGB')
    
    # Save optimized cover
    im.save(OUT_DIR / f"{sku}.png", quality=95, optimize=True)

print(f"Generated 25 authentic, graphic book covers into {OUT_DIR}")

