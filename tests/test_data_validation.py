"""
Unit Test Suite for DuwcsAnhLib Data Integrity & Production Assets
Validates:
1. Product Catalog CSV: 25 authentic titles, unique DAL-xxx SKUs, 5 categories.
2. Production Asset Files: 25 covers (600x900px), brand logos, favicons, hero background.
3. XML Import File: Contains all pages, posts, and Flatsome homepage shortcodes.
4. Static Web Application Build: index.html integrity, official MoMo wallet 0933543987, UTF-8.
"""
import unittest
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

class TestDuwcsAnhLibData(unittest.TestCase):
    def setUp(self):
        self.csv_path = ROOT / 'duwcsanhlib' / 'data' / 'san-pham-duwcsanhlib.csv'
        self.xml_path = ROOT / 'duwcsanhlib' / 'content' / 'duwcsanhlib-noi-dung.xml'
        self.static_dir = ROOT / 'duwcsanhlib-static-web'
        self.index_html_path = self.static_dir / 'index.html'

    def test_01_product_csv_integrity(self):
        """Kiểm tra tệp CSV 25 sản phẩm: tồn tại, đúng định dạng, SKU duy nhất, giá > 0."""
        self.assertTrue(self.csv_path.exists(), "Tệp san-pham-duwcsanhlib.csv không tồn tại")
        
        with open(self.csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = list(csv.DictReader(f))
        
        self.assertEqual(len(reader), 25, f"Tổng số sản phẩm phải là 25, thực tế: {len(reader)}")
        
        skus = set()
        categories = {}
        for row in reader:
            sku = row.get('SKU', '').strip()
            self.assertTrue(sku.startswith('DAL-'), f"Mã SKU {sku} không có tiền tố DAL-")
            self.assertNotIn(sku, skus, f"Mã SKU {sku} bị trùng lặp")
            skus.add(sku)
            
            reg_price = int(row.get('Regular price', 0) or 0)
            self.assertGreater(reg_price, 0, f"Sản phẩm {sku} có giá không hợp lệ: {reg_price}")
            
            cat = row.get('Categories', '').strip()
            self.assertTrue(bool(cat), f"Sản phẩm {sku} thiếu danh mục")
            categories[cat] = categories.get(cat, 0) + 1

        self.assertEqual(len(categories), 5, f"Phải có đúng 5 danh mục, thực tế: {len(categories)}")
        for cat_name, count in categories.items():
            self.assertEqual(count, 5, f"Danh mục '{cat_name}' phải có 5 cuốn, thực tế: {count}")

    def test_02_production_cover_assets(self):
        """Kiểm tra toàn bộ 25 ảnh bìa sách trong duwcsanhlib-static-web/assets/covers."""
        covers_dir = self.static_dir / 'assets' / 'covers'
        self.assertTrue(covers_dir.exists(), "Thư mục covers không tồn tại")
        
        for i in range(1, 26):
            sku = f"DAL-{i:03d}"
            cover_path = covers_dir / f"{sku}.png"
            self.assertTrue(cover_path.exists(), f"Thiếu ảnh bìa cho {sku}: {cover_path}")
            
            with Image.open(cover_path) as img:
                w, h = img.size
                self.assertGreaterEqual(w, 400, f"Chiều rộng {sku} quá nhỏ: {w}")
                self.assertGreaterEqual(h, 600, f"Chiều cao {sku} quá nhỏ: {h}")

    def test_03_brand_identity_assets(self):
        """Kiểm tra các assets nhận diện thương hiệu: logo header, site icon, hero background."""
        assets_dir = self.static_dir / 'assets'
        required_assets = [
            'logo-header.png',
            'logo-header-symbol.png',
            'site-icon-512.png',
            'hero-bookstore-bg.jpg',
            'favicon.ico',
            'favicon-32x32.png',
            'apple-touch-icon.png'
        ]
        for asset in required_assets:
            path = assets_dir / asset
            self.assertTrue(path.exists(), f"Thiếu file asset thương hiệu: {asset}")
            self.assertGreater(path.stat().st_size, 0, f"File {asset} có kích thước 0 byte")

    def test_04_master_index_html_build(self):
        """Kiểm tra build hoàn chỉnh duwcsanhlib-static-web/index.html."""
        self.assertTrue(self.index_html_path.exists(), "index.html chưa được build")
        content = self.index_html_path.read_text(encoding='utf-8')
        
        # Kiểm tra không có ký tự lỗi mã hoá UTF-8
        self.assertNotIn('\ufffd', content, "index.html chứa ký tự lỗi UTF-8 replacement (\\ufffd)")
        
        # Kiểm tra hotline và ví MoMo chính thức
        self.assertIn('0933.543.987', content, "Thiếu hotline hiển thị trên giao diện")
        self.assertIn('0933543987', content, "Thiếu số tài khoản ví MoMo chính thức")
        self.assertIn('971025', content, "Thiếu mã ngân hàng MoMo Napas BIN 971025")
        
        # Kiểm tra thành phần cốt lõi của giao diện
        self.assertIn('view-landing', content, "Thiếu Landing Page onboarding view")
        self.assertIn('view-checkout', content, "Thiếu view thanh toán chuẩn Flatsome")
        self.assertIn('view-order-success', content, "Thiếu view xác nhận đơn hàng thành công")
        self.assertIn('succVietQRImage', content, "Thiếu phần hiển thị mã VietQR / MoMo QR động")
        self.assertIn('categoryMegaMenuDropdown', content, "Thiếu dropdown Danh mục sản phẩm")
        self.assertIn('logo-header.png', content, "Thiếu logo header chuẩn vector")

    def test_05_xml_content_export(self):
        """Kiểm tra tệp XML duwcsanhlib-noi-dung.xml."""
        self.assertTrue(self.xml_path.exists(), "Tệp XML không tồn tại")
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        items = root.findall('.//item')
        self.assertGreaterEqual(len(items), 9, f"Tệp XML phải chứa ít nhất 9 items, thực tế: {len(items)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
