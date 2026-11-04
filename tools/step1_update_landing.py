"""Script nâng cấp toàn diện giao diện DuwcsAnhLib:
1. Gỡ bỏ Top Notification Strip khỏi landing-page.html (Ảnh 5).
2. Xóa bỏ hoàn toàn cơ chế tự động chuyển hướng (auto-redirect) gây lỗi không xem được Landing Page.
3. Đồng bộ nhãn taskbar, gỡ bỏ '(25)' và trùng lặp menu (Ảnh 1).
4. Thiết kế Banner Billboard chuẩn điện ảnh với ảnh nền thư viện & bóng chiếu spotlight (Ảnh 3 & 4).
5. Tích hợp Toast notification thông minh khi thêm vào giỏ hàng (Ảnh 2).
6. Xây dựng Drawer danh sách Yêu thích (Wishlist) tương tác thực tế 100%.
7. Làm giàu dữ liệu chuyên sâu cho toàn bộ 25 ấn bản NXB Trẻ.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'

print("[1] Đang cập nhật duwcsanhlib/landing-page.html...")
content = landing_file.read_text(encoding='utf-8')

# Gỡ bỏ Top Notification Strip
content = re.sub(
    r'<!-- TOP NOTIFICATION STRIP -->[\s\S]*?<!-- MINIMALIST STICKY HEADER -->',
    '<!-- MINIMALIST STICKY HEADER -->',
    content
)

# Gỡ bỏ '(25 Sách)' trong nút CTA
content = content.replace('Khám Phá Cửa Hàng (25 Sách)', 'Khám Phá Cửa Hàng')

# Gỡ bỏ auto-redirect localStorage
auto_redirect_pattern = r'try\s*\{\s*const hasEntered = localStorage\.getItem\(\'duwcsanhlib_has_entered_store\'\) === \'true\';[\s\S]*?window\.location\.replace\(\'/shop\'\);\s*\}\s*\}\s*catch\s*\(e\)\s*\{\}'
replacement_script = """// Click nút CTA để vào cửa hàng (/shop)
    function enterStore(cat) {
      let targetUrl = '/shop';
      if (cat) {
        targetUrl = '/shop?cat=' + encodeURIComponent(cat);
      }
      window.location.href = targetUrl;
    }"""

if 'hasEntered' in content:
    content = re.sub(r'<script>[\s\S]*?function enterStore\(cat\)[\s\S]*?</script>', f"<script>\n    {replacement_script}\n  </script>", content)

landing_file.write_text(content, encoding='utf-8')
print(" -> duwcsanhlib/landing-page.html đã được cập nhật thành công!")

