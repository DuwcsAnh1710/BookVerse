"""Kiểm thử tính toàn vẹn của dữ liệu DuwcsAnhLib trước khi đưa lên WordPress."""
import csv, json, re, hashlib, collections, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
data_dir = ROOT / 'data'
assets_dir = ROOT / 'assets'
content_dir = ROOT / 'content'

checks = []

def check(condition, label):
    res = 'PASS' if condition else 'FAIL'
    checks.append({'check': label, 'result': res})
    status_icon = " [OK] " if condition else " [FAIL] "
    print(f"{status_icon} {label}")
    return condition

def run_all_checks():
    print("=" * 60)
    print(" BAT DAU KIEM THU LOCAL DU LIEU DUWCSANHLIB")
    print("=" * 60)
    
    # 1. Kiểm tra CSV sản phẩm
    csv_path = data_dir / 'san-pham-duwcsanhlib.csv'
    check(csv_path.exists(), "Tệp CSV san-pham-duwcsanhlib.csv tồn tại")
    check(csv_path.read_bytes().startswith(b'\xef\xbb\xbf'), "CSV có UTF-8 BOM chuẩn cho WooCommerce")
    
    with csv_path.open(encoding='utf-8-sig', newline='') as f:
        products = list(csv.DictReader(f))
    
    check(len(products) == 25, f"Tổng số sản phẩm trong CSV là 25 (Thực tế: {len(products)})")
    
    # Kiểm tra tính duy nhất của SKU
    skus = [p['SKU'] for p in products]
    check(len(set(skus)) == 25, "Tất cả 25 mã SKU đều là duy nhất, không trùng lặp")
    check(all(s.startswith("DAL-") for s in skus), "Tất cả SKU đều mang tiền tố DAL- chuẩn DuwcsAnhLib")
    
    # 2. Kiểm tra phân bổ danh mục (5 danh mục x 5 sách)
    categories = collections.Counter(p['Categories'] for p in products)
    expected_cats = ['Văn học', 'Kỹ năng và phát triển bản thân', 'Kinh tế và kinh doanh', 'Tâm lý và đời sống', 'Thiếu nhi']
    check(all(categories[c] == 5 for c in expected_cats), "Phân bổ đồng đều: 5 danh mục, mỗi danh mục 5 cuốn")
    
    # 3. Kiểm tra thuộc tính sản phẩm và ảnh bìa
    all_covers_ok = True
    for p in products:
        sku = p['SKU']
        cover_path = assets_dir / 'covers' / f"{sku}.png"
        if not cover_path.exists():
            all_covers_ok = False
            break
        # Verify image
        try:
            with Image.open(cover_path) as im:
                if im.size != (600, 900):
                    all_covers_ok = False
                    break
        except Exception:
            all_covers_ok = False
            break
            
    check(all_covers_ok, "Tất cả 25 ảnh bìa (600x900px) hợp lệ và đọc được")
    check((assets_dir / 'logo-duwcsanhlib.png').exists(), "Logo thương hiệu logo-duwcsanhlib.png tồn tại")
    check((assets_dir / 'banner-duwcsanhlib.png').exists(), "Banner trang chủ banner-duwcsanhlib.png tồn tại")
    
    # 4. Kiểm tra WXR XML
    xml_path = content_dir / 'duwcsanhlib-noi-dung.xml'
    check(xml_path.exists(), "Tệp XML duwcsanhlib-noi-dung.xml tồn tại")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    items = root.findall('./channel/item')
    check(len(items) >= 8, f"Tệp XML chứa đầy đủ các trang và bài viết (Thực tế: {len(items)} mục)")
    check((content_dir / 'trang-chu-flatsome-shortcodes.txt').exists(), "Mã shortcode Trang chủ Flatsome tồn tại")
    check((content_dir / 'trang-chu.md').exists(), "Tài liệu cấu trúc Trang chủ trang-chu.md tồn tại")
    check((ROOT / 'docs' / '03-huong-dan-thiet-lap-landingpage-flatsome.md').exists(), "Hướng dẫn thiết lập Landing page Flatsome tồn tại")
    check((ROOT / 'docs' / '04-huong-dan-toi-uu-shop-va-chi-tiet-san-pham.md').exists(), "Hướng dẫn tối ưu Shop và Chi tiết sản phẩm tồn tại")
    
    # 5. Kiểm tra giá và tồn kho
    all_prices_valid = all(int(p['Regular price']) > 0 and int(p['Stock']) > 0 for p in products)
    check(all_prices_valid, "Giá bán và tồn kho giả lập đều > 0")
    
    print("=" * 60)
    passed_count = sum(1 for c in checks if c['result'] == 'PASS')
    total_count = len(checks)
    print(f" KET QUA: {passed_count}/{total_count} kiem tra dat (PASS)")
    print("=" * 60)
    return passed_count == total_count

if __name__ == '__main__':
    run_all_checks()
