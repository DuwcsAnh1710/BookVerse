# DuwcsAnhLib — Production Tools & Build Pipeline

Thư mục này chứa các công cụ tự động hoá, bộ biên dịch giao diện và quy trình triển khai cho hệ thống **DuwcsAnhLib (BookVerse)**.

---

## 🛠️ Danh Sách Công Cụ

### 1. Trình Biên Dịch & Triển Khai Web (Core Build & Deploy)
- **`build_master_unified_web.py`**:
  Biên dịch gói ứng dụng web hợp nhất (`duwcsanhlib-static-web/index.html`, `landing.html`, `store.html`, `index.php`). Tích hợp giao diện onboarding phiên đầu, catalog 25 sách NXB Trẻ, điều hướng thanh taskbar màu hổ phách, Mega Menu danh mục và luồng thanh toán Flatsome.
- **`deploy_unified_master.py`**:
  Tự động kết nối FTP Pure-FTPd đến hosting InfinityFree (`duwcsanhlib.wuaze.com`) và triển khai toàn bộ gói tĩnh (`index.html`, `index.php`, `.htaccess`, `assets/`).

### 2. Thành Phần Giao Diện Thanh Toán (Checkout Components)
- **`checkout_template.py`**:
  Template HTML 2 cột lấy cảm hứng từ WooCommerce & theme Flatsome: Thông tin nhận hàng (Họ tên, SĐT, Địa chỉ, Ghi chú), Tuỳ chọn thanh toán (Ví MoMo QR Napas BIN `971025` và COD), Tóm tắt giỏ hàng Sticky, Mã giảm giá voucher (`DUWCSANH10`, `FREESHIP`), và Hoá đơn xác nhận đơn hàng thành công.
- **`checkout_js.py`**:
  Module JavaScript điều khiển toàn bộ luồng thanh toán: kiểm tra form validation, tạo mã QR MoMo động theo thời gian thực (VietQR API), sao chép nhanh số tài khoản `0933543987` và lời nhắn chuyển tiền 1-click, cùng chức năng in hoá đơn (`window.print()`).

### 3. Quy Trình Dữ Liệu & Ảnh Bìa (Assets & Data Pipelines)
- **`download_real_covers.py`**: Tải ảnh bìa chính thức từ NXB Trẻ với User-Agent chuẩn.
- **`find_all_nxbtre_images.py`**: Quét và thu thập link ảnh gốc từ kho lưu trữ NXB Trẻ.
- **`fetch_fahasa.py`**: Bổ sung tư liệu sách và đối soát thông tin từ Fahasa.
- **`generate_real_covers.py`**: Trình tạo ảnh bìa chất lượng cao chuẩn tỷ lệ 600x900px.
- **`process_brand_assets.py`**: Tạo các biến thể logo vector, site-icon 512 squircle, apple-touch-icon, và favicons đa kích thước.
- **`book_images_found.json`**: Tệp JSON lưu trữ ánh xạ ảnh bìa đã được xác thực cho 25 ấn bản.
- **`add_homepage_to_xml.py`**: Bổ sung shortcode trang chủ Flatsome vào tệp WXR XML để import vào WordPress.

---

## 🚀 Hướng Dẫn Sử Dụng

### Biên dịch lại giao diện web:
```bash
python tools/build_master_unified_web.py
```

### Triển khai lên máy chủ InfinityFree:
```bash
python tools/deploy_unified_master.py
```

