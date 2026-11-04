"""Build DuwcsAnhLib package with authentic publication data, realistic covers,
official hotline 0933 543 987, and professional policies without AI placeholder text.
"""
import csv, json, re, html, hashlib, zipfile, shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("D:/VSCode/HKDN/BookVerse")
SRC_DIR = ROOT / "moc-thu"
OUT_DIR = ROOT / "duwcsanhlib"

# 1. Create directory structure
for sub in ["assets/covers", "content", "data", "docs"]:
    (OUT_DIR / sub).mkdir(parents=True, exist_ok=True)

# 2. Load books and update brand references
raw_books = json.loads((SRC_DIR / "data/books.json").read_text(encoding="utf-8"))
books = []
for b in raw_books:
    item = dict(b)
    num = item['sku'].split('-')[-1]
    item['dal_sku'] = f"DAL-{num}"
    item['sku'] = f"DAL-{num}"
    item['description'] = item['description'].replace("Mộc Thư", "DuwcsAnhLib")
    books.append(item)

(OUT_DIR / "data/books.json").write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")

# 3. Build CSVs with authentic publication details
def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

products = []
sources = []
for b in books:
    size = b['size'].replace(',', '.').replace('x', ' × ')
    attrs = [
        ('Tác giả', b['author']),
        ('Nhà xuất bản', b['publisher']),
        ('Năm xuất bản của lần in', b['year']),
        ('Số trang', b['pages']),
        ('Ngôn ngữ', b['language']),
        ('Kích thước sách', size),
        ('ISBN', b['isbn']),
        ('Lần in', b['edition'])
    ]
    p = {
        'Type': 'simple',
        'SKU': b['sku'],
        'Name': b['title'],
        'Published': 1,
        'Is featured?': b['featured'],
        'Visibility in catalog': 'visible',
        'Short description': b['short'],
        'Description': '<p>' + html.escape(b['description']) + '</p><p><strong>Thông tin ấn bản:</strong> Tác phẩm do ' + html.escape(b['publisher']) + ' ấn hành, bản in chất lượng cao, định dạng bìa mềm quy chuẩn. Sách được phân phối chính hãng bởi DuwcsAnhLib, cam kết 100% sách thật, hỗ trợ đổi trả trong 7 ngày nếu có lỗi kỹ thuật từ nhà in.</p>',
        'Tax status': 'none',
        'In stock?': 1,
        'Stock': b['stock'],
        'Low stock amount': 2,
        'Backorders allowed?': 0,
        'Sold individually?': 0,
        'Allow customer reviews?': 0,
        'Regular price': b['reference_price'],
        'Sale price': b['demo_price'],
        'Categories': b['category'],
        'Images': ''
    }
    for n, (key, val) in enumerate(attrs, 1):
        p.update({
            f'Attribute {n} name': key,
            f'Attribute {n} value(s)': val,
            f'Attribute {n} visible': 1,
            f'Attribute {n} global': 0
        })
    products.append(p)
    sources.append({
        'SKU': b['sku'],
        'Tên sách': b['title'],
        'Danh mục DuwcsAnhLib': b['category'],
        'Tác giả': b['author'],
        'NXB': b['publisher'],
        'Số trang': b['pages'],
        'Năm lần in': b['year'],
        'Lần in': b['edition'],
        'ISBN nguồn': b['isbn'],
        'Kích thước': b['size'],
        'URL nguồn': b['url'],
        'Ngày tra cứu': b['accessed'],
        'Giá bìa niêm yết (VND)': b['reference_price'],
        'Giá bán ưu đãi (VND)': b['demo_price'],
        'Tồn kho': b['stock'],
        'Ngôn ngữ đối chiếu': 'Tiếng Việt',
        'Ảnh bìa': f"assets/covers/{b['sku']}.png",
        'Ghi chú': 'Thông tin ấn bản chính thức đối chiếu NXB Trẻ.'
    })

write_csv(OUT_DIR / "data/san-pham-duwcsanhlib.csv", products)
write_csv(OUT_DIR / "data/nguon-sach.csv", sources)

# 4. Generate Graphic Book Covers (Realistic Book Jackets)
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

THEMES = {
    'DAL-001': {'bg': '#2C3E50', 'bg2': '#1A252F', 'gold': '#F1C40F', 'accent': '#E74C3C'},
    'DAL-002': {'bg': '#1B4F72', 'bg2': '#0B2545', 'gold': '#5DADE2', 'accent': '#F39C12'},
    'DAL-003': {'bg': '#4A235A', 'bg2': '#2E1139', 'gold': '#D7BDE2', 'accent': '#E59866'},
    'DAL-004': {'bg': '#145A32', 'bg2': '#0B331C', 'gold': '#F4D03F', 'accent': '#58D68D'},
    'DAL-005': {'bg': '#6E2C00', 'bg2': '#3E1900', 'gold': '#EDBB99', 'accent': '#E67E22'},
    'DAL-006': {'bg': '#1C2833', 'bg2': '#0E141B', 'gold': '#F39C12', 'accent': '#2ECC71'},
    'DAL-007': {'bg': '#1B2631', 'bg2': '#17202A', 'gold': '#E74C3C', 'accent': '#BB8FCE'},
    'DAL-008': {'bg': '#512E5F', 'bg2': '#2C1736', 'gold': '#F5B041', 'accent': '#AF7AC5'},
    'DAL-009': {'bg': '#283747', 'bg2': '#1B242F', 'gold': '#48C9B0', 'accent': '#F39C12'},
    'DAL-010': {'bg': '#0E6251', 'bg2': '#07332A', 'gold': '#F9E79F', 'accent': '#48C9B0'},
    'DAL-011': {'bg': '#154360', 'bg2': '#0B2535', 'gold': '#52BE80', 'accent': '#F4D03F'},
    'DAL-012': {'bg': '#5B2C6F', 'bg2': '#331940', 'gold': '#F8C471', 'accent': '#85C1E9'},
    'DAL-013': {'bg': '#641E16', 'bg2': '#3D120D', 'gold': '#FAD7A0', 'accent': '#F1948A'},
    'DAL-014': {'bg': '#186A3B', 'bg2': '#0D3820', 'gold': '#F9E79F', 'accent': '#7DCEA0'},
    'DAL-015': {'bg': '#17202A', 'bg2': '#0B1015', 'gold': '#E67E22', 'accent': '#3498DB'},
    'DAL-016': {'bg': '#1F618D', 'bg2': '#11354D', 'gold': '#FADBD8', 'accent': '#A9DFBF'},
    'DAL-017': {'bg': '#2E4053', 'bg2': '#1A242F', 'gold': '#F39C12', 'accent': '#E74C3C'},
    'DAL-018': {'bg': '#34495E', 'bg2': '#1D2A37', 'gold': '#A3E4D7', 'accent': '#FAD7A0'},
    'DAL-019': {'bg': '#4A235A', 'bg2': '#271131', 'gold': '#F8C471', 'accent': '#D2B4DE'},
    'DAL-020': {'bg': '#196F3D', 'bg2': '#0C381F', 'gold': '#F7DC6F', 'accent': '#82E0AA'},
    'DAL-021': {'bg': '#78281F', 'bg2': '#421611', 'gold': '#F9E79F', 'accent': '#E74C3C'},
    'DAL-022': {'bg': '#1B4F72', 'bg2': '#0E2E44', 'gold': '#FAD7A0', 'accent': '#5499C7'},
    'DAL-023': {'bg': '#B03A2E', 'bg2': '#692019', 'gold': '#F9E79F', 'accent': '#FADBD8'},
    'DAL-024': {'bg': '#117864', 'bg2': '#094539', 'gold': '#F8C471', 'accent': '#73C6B6'},
    'DAL-025': {'bg': '#2874A6', 'bg2': '#16405B', 'gold': '#F9E79F', 'accent': '#85C1E9'}
}

covers_dir = OUT_DIR / 'assets/covers'
W, H = 600, 900
for b in books:
    sku = b['sku']
    theme = THEMES.get(sku, {'bg': '#1C2833', 'bg2': '#0E141B', 'gold': '#F39C12', 'accent': '#2ECC71'})
    im = Image.new('RGB', (W, H), theme['bg'])
    d = ImageDraw.Draw(im)
    
    # Smooth vertical gradient
    for y in range(H):
        r1, g1, b1 = tuple(int(theme['bg'][i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(theme['bg2'][i:i+2], 16) for i in (1, 3, 5))
        ratio = y / H
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        blue = int(b1 * (1 - ratio) + b2 * ratio)
        d.line([(0, y), (W, y)], fill=(r, g, blue))
        
    # Double Golden Border
    frame = theme['gold']
    d.rectangle([25, 25, W - 25, H - 25], outline=frame, width=3)
    d.rectangle([35, 35, W - 35, H - 35], outline=frame, width=1)
    for cx, cy in [(35, 35), (W - 35, 35), (35, H - 35), (W - 35, H - 35)]:
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=frame)
        
    # Author
    author_str = b['author'].upper()
    f_auth = font('georgiab.ttf', 20)
    w_auth = d.textlength(author_str, font=f_auth)
    d.text(((W - w_auth) / 2, 70), author_str, font=f_auth, fill=theme['gold'])
    d.line([(W/2 - 50, 105), (W/2 + 50, 105)], fill=theme['gold'], width=2)
    d.ellipse([(W/2 - 4, 103), (W/2 + 4, 107)], fill=theme['gold'])
    
    # Title
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
        d.text(((W - line_w) / 2 + 2, start_y + i * 48 + 2), line, font=f_title, fill='#0B1015')
        d.text(((W - line_w) / 2, start_y + i * 48), line, font=f_title, fill='#FFFFFF')
        
    # Category
    cat_str = f"— {b['category'].upper()} —"
    f_cat = font('georgia.ttf', 16)
    w_cat = d.textlength(cat_str, font=f_cat)
    d.text(((W - w_cat) / 2, start_y + len(title_lines) * 48 + 25), cat_str, font=f_cat, fill=theme['accent'])
    
    # Medallion
    mid_y = 560
    d.ellipse([(W/2 - 80, mid_y - 80), (W/2 + 80, mid_y + 80)], outline=theme['gold'], width=2)
    d.ellipse([(W/2 - 70, mid_y - 70), (W/2 + 70, mid_y + 70)], outline=theme['accent'], width=1)
    d.polygon([(W/2, mid_y - 50), (W/2 + 50, mid_y), (W/2, mid_y + 50), (W/2 - 50, mid_y)], outline=theme['gold'], width=2)
    d.ellipse([(W/2 - 15, mid_y - 15), (W/2 + 15, mid_y + 15)], fill=theme['gold'])
    
    # Publisher
    pub_str = "NHÀ XUẤT BẢN TRẺ"
    f_pub = font('georgiab.ttf', 18)
    w_pub = d.textlength(pub_str, font=f_pub)
    d.line([(W/2 - 100, 770), (W/2 + 100, 770)], fill=theme['gold'], width=1)
    d.text(((W - w_pub) / 2, 790), pub_str, font=f_pub, fill='#FFFFFF')
    
    sub_str = f"Ấn bản {b['year']}  •  Khổ {b['size']}"
    f_sub = font('georgia.ttf', 13)
    w_sub = d.textlength(sub_str, font=f_sub)
    d.text(((W - w_sub) / 2, 822), sub_str, font=f_sub, fill='#BDC3C7')
    
    # Spine Shadow
    spine = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_spine = ImageDraw.Draw(spine)
    for x in range(35):
        alpha = int(120 * (1 - x / 35))
        d_spine.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
    for x in range(35, 45):
        alpha = int(40 * (1 - abs(x - 40) / 5))
        d_spine.line([(x, 0), (x, H)], fill=(255, 255, 255, alpha))
    im = Image.alpha_composite(im.convert('RGBA'), spine).convert('RGB')
    im.save(covers_dir / f"{sku}.png", quality=95, optimize=True)

# Generate Logo
logo = Image.new('RGBA', (760, 180), (0, 0, 0, 0))
d = ImageDraw.Draw(logo)
d.text((15, 10), 'DuwcsAnhLib', font=font('georgiab.ttf', 92), fill='#C92127')
d.text((20, 125), 'HIỆU SÁCH & THƯ VIỆN TRI THỨC', font=font('arialbd.ttf', 20), fill='#1C2833')
logo.save(OUT_DIR / 'assets/logo-duwcsanhlib.png')

# Generate Banner
banner = Image.new('RGB', (1200, 700), '#F0F2F5')
d = ImageDraw.Draw(banner)
for i, b in enumerate(books[::5][:3]):
    c = Image.open(covers_dir / (b['sku'] + '.png')).resize((230, 345))
    banner.paste(c, (160 + i * 310, 160 + (i % 2) * 40))

d.rectangle((100, 50, 1100, 120), fill='#C92127')
d.text((140, 68), 'DUWCSANHLIB — ĐẠI TIỆC TRI THỨC NXB TRẺ', font=font('arialbd.ttf', 30), fill='#FFFFFF')
d.text((160, 600), 'Ưu đãi lên đến 30% — Hotline: 0933.543.987', font=font('arialbd.ttf', 26), fill='#1C2833')
banner.save(OUT_DIR / 'assets/banner-duwcsanhlib.png', optimize=True)

# 5. Transform Content Markdown files (Hotline 0933 543 987, zero AI cliches)
content_map = {
    'gioi-thieu.md': """# Về DuwcsAnhLib

DuwcsAnhLib là hệ thống nhà sách trực tuyến chuyên cung cấp các ấn phẩm sách tinh tuyển, chất lượng cao dành cho độc giả yêu văn hóa đọc trên toàn quốc. Chúng tôi tin rằng mỗi cuốn sách là một nguồn cảm hứng bất tận, mở rộng tư duy và bồi đắp tri thức cho mỗi cá nhân.

Tại DuwcsAnhLib, độc giả có thể dễ dàng tìm kiếm những ấn bản chất lượng thuộc 5 thể loại cốt lõi: Văn học & Tản văn, Kinh tế & Khởi nghiệp, Tâm lý & Đời sống, Kỹ năng phát triển bản thân và Sách Thiếu nhi. Mọi ấn bản đều được nhập trực tiếp và phân phối chính thức từ các nhà xuất bản uy tín hàng đầu như Nhà xuất bản Trẻ.

Với phương châm phục vụ tận tâm, DuwcsAnhLib cam kết 100% sách thật, quy cách đóng gói chống sốc kỹ lưỡng và dịch vụ giao hàng nhanh chóng tận tay độc giả.
""",
    'lien-he.md': """# Liên hệ DuwcsAnhLib

DuwcsAnhLib luôn sẵn sàng hỗ trợ độc giả trong việc tra cứu thông tin sách, đặt hàng và chăm sóc hậu mãi.

- **Thương hiệu:** DuwcsAnhLib — Hiệu Sách & Thư Viện Tri Thức
- **Hotline hỗ trợ:** 0933 543 987 (Hỗ trợ từ 08:00 – 21:00 hàng ngày)
- **Email:** lienhe@duwcsanhlib.vn
- **Địa chỉ:** Hệ thống phân phối trực tuyến DuwcsAnhLib
- **Thời gian làm việc:** Thứ 2 đến Chủ nhật (08:00 – 21:00)
""",
    'giao-hang.md': """# Chính sách Giao hàng — DuwcsAnhLib

DuwcsAnhLib liên kết cùng các đơn vị vận chuyển hàng đầu (VNPost, ViettelPost, GHTK) để giao sách nhanh chóng đến tận tay bạn:

- **Phạm vi giao hàng:** Toàn quốc đến tất cả 63 tỉnh thành.
- **Thời gian giao dự kiến:** 1 – 2 ngày làm việc đối với khu vực nội thành, 2 – 4 ngày đối với khu vực liên tỉnh.
- **Ưu đãi cước phí:** **MIỄN PHÍ VẬN CHUYỂN TOÀN QUỐC** cho tất cả các đơn hàng từ 250.000 đ. Đơn hàng dưới 250.000 đ áp dụng phí vận chuyển tiêu chuẩn 25.000 đ.
- **Quy cách đóng gói:** 100% sách được bao bọc bằng màng xốp khí chống va đập và đóng hộp carton cứng cáp để giữ nguyên góc cạnh sách.
- **Hotline điều phối giao hàng:** 0933 543 987
""",
    'doi-tra.md': """# Chính sách Đổi trả & Hoàn tiền — DuwcsAnhLib

Nhằm đảm bảo quyền lợi cao nhất của khách hàng, DuwcsAnhLib áp dụng chính sách đổi trả minh bạch và nhanh chóng:

- **Thời hạn tiếp nhận:** Trong vòng 7 ngày kể từ thời điểm nhận sách thành công.
- **Điều kiện áp dụng:** Sách bị lỗi in ấn (trang trắng, ngược trang, mờ chữ), rách bìa hoặc cấn móp trong quá trình vận chuyển.
- **Hình thức xử lý:** Đổi mới 100% cuốn sách cùng tựa hoàn toàn miễn phí (DuwcsAnhLib chịu toàn bộ phí vận chuyển đổi chiều).
- **Quy trình đơn giản:** Quý khách chỉ cần liên hệ hotline **0933 543 987** hoặc gửi hình ảnh qua Zalo/Email để được xử lý ngay trong 24h.
""",
    'bao-mat.md': """# Chính sách Bảo mật Thông tin — DuwcsAnhLib

DuwcsAnhLib cam kết bảo vệ tuyệt đối thông tin cá nhân của khách hàng theo quy chuẩn pháp luật:

- **Thông tin thu thập:** Họ tên, số điện thoại, địa chỉ nhận hàng và email để phục vụ việc giao nhận và thông báo trạng thái đơn hàng.
- **Mục đích sử dụng:** Xử lý đơn hàng, thông tin hành trình bưu phẩm và chăm sóc khách hàng sau bán.
- **Cam kết an toàn:** Không chia sẻ, buôn bán hoặc tiết lộ thông tin người dùng cho bất kỳ bên thứ ba nào ngoài đối tác vận chuyển giao hàng.
""",
    'blog-01.md': """# Khởi đầu ngày mới cùng thói quen đọc 15 phút

Dành 15 phút mỗi buổi sáng cho một vài trang sách có thể tạo nên sự chuyển biến bất ngờ cho tư duy và tâm trạng của bạn trong cả ngày dài.

Tại DuwcsAnhLib, chúng tôi khuyến khích độc giả bắt đầu từ những cuốn tản văn nhẹ nhàng hoặc những đầu sách kỹ năng ngắn gọn. Không cần đặt áp lực phải hoàn thành cả cuốn sách trong một ngày, điều quý giá nhất là sự đều đặn và khoảng không gian tĩnh tại bạn dành riêng cho tâm trí.
""",
    'blog-02.md': """# 5 tựa sách kinh điển nên có trên giá sách của bạn

Dù xu hướng đọc có thay đổi theo thời gian, những giá trị nguyên bản trong các tác phẩm văn học kinh điển vẫn luôn giữ nguyên sức hút.

Bài viết này gợi ý 5 ấn bản nổi bật đang có mặt tại thư viện DuwcsAnhLib, từ những tác phẩm phản ánh chiều sâu văn hóa đến những câu chuyện truyền cảm hứng vượt thời gian. Hãy cùng khám phá và tìm cho mình một cuốn sách phù hợp nhất cho dịp cuối tuần này.
""",
    'blog-03.md': """# Nghệ thuật chọn sách cho trẻ em theo từng độ tuổi

Đọc sách cùng con không chỉ giúp bồi đắp vốn từ và trí tưởng tượng mà còn là cầu nối gắn kết tình cảm gia đình.

Bộ sưu tập Sách Thiếu nhi tại DuwcsAnhLib được tuyển chọn với nội dung nhân văn, hình minh họa tươi sáng và ngôn ngữ dễ hiểu. Hãy tham khảo những kinh nghiệm chọn sách theo giai đoạn phát triển để giúp trẻ xây dựng tình yêu đọc sách tự nhiên nhất.
"""
}

for name, text in content_map.items():
    (OUT_DIR / "content" / name).write_text(text, encoding="utf-8")

# 6. Build WXR XML for DuwcsAnhLib
def markdown_content(text):
    blocks = text.strip().split('\n\n')
    title = blocks.pop(0).removeprefix('# ')
    def inline(t): return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(t))
    out = []
    for text_block in blocks:
        if text_block.startswith('## '):
            out.append('<h2>' + inline(text_block[3:]) + '</h2>')
        elif text_block.startswith('- '):
            out.append('<ul>' + ''.join('<li>' + inline(x[2:]) + '</li>' for x in text_block.splitlines()) + '</ul>')
        else:
            out.append('<p>' + inline(text_block.replace('\n', ' ')) + '</p>')
    return title, '\n'.join(out)

ns = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}
for name, url in ns.items():
    ET.register_namespace(name, url)

def sub(node, name, text):
    if ':' in name:
        prefix, local = name.split(':')
        name = '{' + ns[prefix] + '}' + local
    e = ET.SubElement(node, name)
    e.text = str(text)
    return e

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
sub(channel, 'title', 'DuwcsAnhLib — Hiệu Sách Trực Tuyến')
sub(channel, 'link', 'http://duwcsanhlib.vn')
sub(channel, 'description', 'Dữ liệu các trang chính sách và bài viết DuwcsAnhLib')
sub(channel, 'language', 'vi')
sub(channel, 'wp:wxr_version', '1.2')
sub(channel, 'wp:base_site_url', 'http://duwcsanhlib.vn')
sub(channel, 'wp:base_blog_url', 'http://duwcsanhlib.vn')

author = sub(channel, 'wp:author', '')
sub(author, 'wp:author_id', '1')
sub(author, 'wp:author_login', 'duwcsanhlib')
sub(author, 'wp:author_email', 'hotro@duwcsanhlib.vn')
sub(author, 'wp:author_display_name', 'Ban Biên Tập DuwcsAnhLib')

files = ['gioi-thieu', 'lien-he', 'giao-hang', 'doi-tra', 'bao-mat', 'blog-01', 'blog-02', 'blog-03']
for i, slug in enumerate(files, 1):
    raw_md = (OUT_DIR / "content" / f"{slug}.md").read_text(encoding="utf-8")
    title, body = markdown_content(raw_md)
    item = ET.SubElement(channel, 'item')
    sub(item, 'title', title)
    sub(item, 'link', f'http://duwcsanhlib.vn/{slug}/')
    sub(item, 'dc:creator', 'duwcsanhlib')
    sub(item, 'content:encoded', body)
    sub(item, 'excerpt:encoded', '')
    sub(item, 'wp:post_id', 2000 + i)
    sub(item, 'wp:post_date', '2026-11-04 10:00:00')
    sub(item, 'wp:post_date_gmt', '2026-11-04 03:00:00')
    sub(item, 'wp:comment_status', 'closed')
    sub(item, 'wp:ping_status', 'closed')
    sub(item, 'wp:post_name', slug)
    sub(item, 'wp:status', 'publish')
    sub(item, 'wp:post_parent', 0)
    sub(item, 'wp:menu_order', 0)
    sub(item, 'wp:post_type', 'post' if slug.startswith('blog') else 'page')
    sub(item, 'wp:post_password', '')
    sub(item, 'wp:is_sticky', 0)

ET.indent(rss)
ET.ElementTree(rss).write(OUT_DIR / 'content/duwcsanhlib-noi-dung.xml', encoding='utf-8', xml_declaration=True)

# 7. Create ZIP archive
zip_path = ROOT / "DuwcsAnhLib-ban-giao.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in OUT_DIR.rglob('*'):
        if f.is_file():
            arcname = f.relative_to(ROOT)
            z.write(f, arcname)

print("Generated DuwcsAnhLib package with authentic covers and data successfully:")
print(" - Output directory:", OUT_DIR)
print(" - Zip archive:", zip_path, f"({zip_path.stat().st_size / 1024:.1f} KB)")
