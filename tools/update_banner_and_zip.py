import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("D:/VSCode/HKDN/BookVerse")
COVERS = ROOT / "duwcsanhlib/assets/covers"
BANNER_PATH = ROOT / "duwcsanhlib/assets/banner-duwcsanhlib.png"
ZIP_PATH = ROOT / "DuwcsAnhLib-ban-giao.zip"

fontdir = Path('C:/Windows/Fonts')
def font(name, size):
    return ImageFont.truetype(str(fontdir / name), size)

# Create Banner with real covers
banner = Image.new('RGB', (1200, 700), '#F8F9FA')
d = ImageDraw.Draw(banner)

# Paste 4 real covers
sample_skus = ['DAL-001', 'DAL-004', 'DAL-006', 'DAL-020']
for i, sku in enumerate(sample_skus):
    cover_file = COVERS / f"{sku}.png"
    if cover_file.exists():
        c = Image.open(cover_file).resize((210, 315))
        # Add soft shadow behind cover
        shadow = Image.new('RGBA', (210, 315), (0, 0, 0, 70))
        banner.paste(shadow, (125 + i * 250, 195))
        banner.paste(c, (120 + i * 250, 190))

# Header band
d.rectangle([(0, 0), (1200, 120)], fill='#C92127')
d.text((80, 25), 'DUWCSANHLIB — THƯ VIỆN & HIỆU SÁCH TRI THỨC', font=font('georgiab.ttf', 32), fill='#FFFFFF')
d.text((80, 75), 'Tuyển tập 25 ấn bản chính thức Nhà xuất bản Trẻ • Hotline: 0933.543.987', font=font('arial.ttf', 18), fill='#FADBD8')

# Footer band
d.rectangle([(0, 580), (1200, 700)], fill='#1C1C1E')
d.text((80, 605), '100% Sách Thật • Đổi Trả Trong 7 Ngày • Miễn Phí Vận Chuyển Đơn Từ 250.000 đ', font=font('arialbd.ttf', 20), fill='#FFFFFF')
d.text((80, 645), 'Hotline hỗ trợ & Đặt sách: 0933 543 987  |  Website: duwcsanhlib.vn', font=font('arial.ttf', 16), fill='#BDC3C7')

banner.save(BANNER_PATH, optimize=True)
print("Updated banner-duwcsanhlib.png with real covers")

# Update ZIP package
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in (ROOT / 'duwcsanhlib').rglob('*'):
        if f.is_file():
            arcname = f.relative_to(ROOT)
            z.write(f, arcname)

print(f"Updated {ZIP_PATH.name} ({ZIP_PATH.stat().st_size / 1024:.1f} KB)")

