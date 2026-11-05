# 📚 BookVerse — DuwcsAnhLib
### Hiệu Sách & Thư Viện Tri Thức Trực Tuyến 2026

[![Live Demo](https://img.shields.io/badge/Live_Demo-duwcsanhlib.wuaze.com-C92127?style=for-the-badge&logo=google-chrome&logoColor=white)](http://duwcsanhlib.wuaze.com)
[![Build Status](https://img.shields.io/badge/Tests-6%2F6_PASS-10B981?style=for-the-badge&logo=github-actions&logoColor=white)]()
[![Platform](https://img.shields.io/badge/Stack-HTML5_%7C_Tailwind_%7C_Python_%7C_PHP-1E293B?style=for-the-badge)]()

**DuwcsAnhLib** là hệ thống thương mại điện tử chuyên nghiệp, chuẩn mực dành cho hiệu sách trực tuyến, tuyển chọn 25 ấn bản kinh điển và đương đại từ **Nhà xuất bản Trẻ**. Dự án kết hợp ngôn ngữ thiết kế thương mại điện tử cao cấp từ theme **Flatsome (WooCommerce)** cùng nền tảng web tĩnh tối ưu tốc độ tải trang, mang lại trải nghiệm mua sắm mượt mà trên mọi thiết bị.

🌐 **Website chính thức đã triển khai trực tiếp:** [http://duwcsanhlib.wuaze.com](http://duwcsanhlib.wuaze.com)  
📞 **Hotline hỗ trợ:** `0933.543.987`  
💳 **Ví MoMo thanh toán:** `0933543987` (Napas BIN: `971025`)

---

## ✨ Tính Năng Nổi Bật

1. **Trang Giới Thiệu (Landing Page Onboarding):**
   - Tự động xuất hiện vào lần đầu tiên người dùng truy cập trang web trong phiên trình duyệt (`sessionStorage`).
   - Thiết kế độc lập toàn màn hình giới thiệu sứ mệnh *"Đọc Để Trưởng Thành & Khai Phóng Tri Thức"*, cam kết 100% sách thật NXB Trẻ.
   - Nút *"Khám Phá Cửa Hàng"* đưa độc giả thẳng vào không gian mua sắm mà không làm phiền ở các lần truy cập tiếp theo.

2. **Thanh Điều Hướng & Taskbar Nổi Bật:**
   - Hiệu ứng đổi màu vàng hổ phách (`#FDE68A` / `text-amber-300`) khi tương tác với tất cả các box trên taskbar (*Cửa Hàng, Tất Cả, Flash Sale, Sách Bán Chạy, Góc Đọc & Review, Về DuwcsAnhLib*).
   - Nút **"DANH MỤC SẢN PHẨM"** dạng Mega Menu dropdown kích hoạt nhanh 5 danh mục cốt lõi và lựa chọn xem toàn bộ sách.

3. **Danh Mục 25 Ấn Bản Tinh Hoa NXB Trẻ:**
   - 5 chủ đề cốt lõi (mỗi chủ đề 5 ấn bản): *Văn Học*, *Lịch Sử & Văn Hóa*, *Kinh Tế & Kỹ Năng*, *Tâm Lý & Phát Triển Bản Thân*, *Thiếu Nhi & Giáo Dục*.
   - Tìm kiếm thời gian thực thông minh theo tên sách, tác giả, ISBN kết hợp bộ lọc danh mục.
   - Hỗ trợ giỏ hàng (Cart) và danh sách yêu thích (Wishlist) lưu trữ tức thì.

4. **Trang Chi Tiết Sản Phẩm Độc Lập & Quick View:**
   - Xem nhanh thông số xuất bản, số trang, trọng lượng, trích dẫn truyền cảm hứng và đánh giá của độc giả.
   - Đầy đủ chính sách đổi trả 7 ngày và đóng gói chống sốc chuyên dụng.

5. **Quy Trình Thanh Toán Chuẩn Flatsome / WooCommerce:**
   - Giao diện 2 cột chuẩn UX: Cột trái nhập Thông tin giao hàng & chọn phương thức thanh toán; Cột phải ghim Sticky tóm tắt đơn hàng và mã ưu đãi (`DUWCSANH10`, `FREESHIP`).
   - Tích hợp 2 phương thức:
     - **Ví Điện Tử MoMo / MoMo QR (24/7):** Tạo mã VietQR động theo thời gian thực (chứa số tiền và mã đơn hàng `#DAL-xxx`), hỗ trợ mở app MoMo nhanh và nút sao chép 1-click số ví `0933543987`.
     - **Thanh toán khi nhận hàng (COD):** Đồng kiểm trước khi thanh toán.
   - Trang hoàn tất đơn hàng hiển thị mã QR, thông tin đối soát và nút In Hoá Đơn (`window.print()`).

6. **Tương Thích Tuyệt Đối Thiết Bị Di Động (Mobile Responsive):**
   - Đã được kiểm thử tự động trên kích thước màn hình điện thoại (iPhone 16 Pro Max 440x956px) với tỷ lệ tràn viền 0%, thanh menu thu gọn và bố cục cuộn mượt mà.

---

## 📁 Cấu Trúc Dự Án

```
BookVerse/
├── duwcsanhlib-static-web/         # Gói mã nguồn web tĩnh hoàn chỉnh sẵn sàng deploy
│   ├── assets/                     # Ảnh bìa 25 cuốn (covers/), logo vector, icon, background
│   ├── index.html                  # Ứng dụng web hợp nhất (Landing + Shop + Checkout)
│   ├── index.php                   # Entrypoint PHP hỗ trợ routing hosting
│   ├── landing.html                # Trang Landing Page độc lập
│   ├── store.html                  # Giao diện Cửa Hàng độc lập
│   └── .htaccess                   # Cấu hình rewrite rules và bảo mật Apache
├── duwcsanhlib/                    # Dữ liệu gốc và tài liệu dự án
│   ├── assets/                     # Tài nguyên thương hiệu chuẩn hóa
│   ├── content/                    # Nội dung các trang chính sách (.md) và WXR XML
│   ├── data/                       # CSV sản phẩm (san-pham-duwcsanhlib.csv) & books.json
│   └── docs/                       # Hướng dẫn thiết lập Flatsome và vận hành
├── tests/                          # Bộ kiểm thử tự động (Unit & Integration Tests)
│   ├── test_checkout_flow.py       # Kiểm thử 7/7 luồng giao diện & thanh toán trên Edge Headless
│   └── test_data_validation.py     # Kiểm thử toàn vẹn dữ liệu CSV, covers, assets, UTF-8
├── tools/                          # Bộ công cụ build, pipeline và deployment
│   ├── build_master_unified_web.py # Trình biên dịch giao diện master
│   ├── checkout_template.py        # Template HTML thanh toán Flatsome 2 cột
│   ├── checkout_js.py              # Xử lý JavaScript giỏ hàng, MoMo QR, validation
│   ├── deploy_unified_master.py    # Script tự động đẩy FTP lên InfinityFree
│   └── README.md                   # Hướng dẫn chi tiết sử dụng các tools
├── server.py                       # Máy chủ web cục bộ phát triển & chạy thử nghiệm
├── flatsome-3.18.7.zip             # Gói theme WordPress Flatsome chính thức
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 🚀 Hướng Dẫn Vận Hành

### 1. Khởi Chạy Máy Chủ Cục Bộ
Chạy ứng dụng trực tiếp trên máy tính cá nhân:
```bash
python server.py
```
Hệ thống sẽ tự động mở trình duyệt tại địa chỉ `http://localhost:8080`.

### 2. Chạy Bộ Kiểm Thử Tự Động (Automated Tests)
Kiểm tra toàn bộ tính toàn vẹn dữ liệu và luồng trải nghiệm người dùng:
```bash
# Chạy tất cả bài kiểm thử
python -m unittest discover tests

# Chạy riêng kiểm thử luồng thanh toán và giao diện (Edge Headless)
python -m unittest tests/test_checkout_flow.py

# Chạy riêng kiểm tra dữ liệu sản phẩm và ảnh bìa
python -m unittest tests/test_data_validation.py
```

### 3. Biên Dịch Lại Giao Diện
Khi có thay đổi về dữ liệu sách hoặc giao diện:
```bash
python tools/build_master_unified_web.py
```

### 4. Triển Khai Lên Máy Chủ Trực Tuyến (InfinityFree FTP)
```bash
python tools/deploy_unified_master.py
```

---

## 👨‍💻 Thông Tin Bàn Giao
- **Đơn vị chủ quản:** DuwcsAnhLib — Hiệu Sách & Thư Viện Tri Thức
- **Nhà xuất bản đối tác:** Nhà xuất bản Trẻ
- **Chủ tài khoản thụ hưởng:** Đoàn Đức Anh — Số MoMo: `0933 543 987`
- **Năm phát hành:** 2026

