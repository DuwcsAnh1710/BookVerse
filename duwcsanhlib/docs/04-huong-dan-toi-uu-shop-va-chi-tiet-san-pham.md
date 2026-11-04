# Hướng Dẫn Tối Ưu Trang Cửa Hàng (Shop) & Trang Chi Tiết Sách (Single Product) Với Flatsome

Tài liệu này hướng dẫn chi tiết cách thiết lập giao diện **Cửa hàng (Shop Catalog)** và **Trang chi tiết sản phẩm (Single Product Page)** trên website WordPress sử dụng theme **Flatsome** cho dự án **DuwcsAnhLib**.

---

## 1. Mục Tiêu Tối Ưu UX/CRO
1. **Trang Cửa hàng (Shop Catalog / Archive)**:
   - Hiển thị danh mục trực quan, ảnh bìa tỉ lệ chuẩn sách 2:3 với chiều cao đồng đều (*Equal Heights*).
   - Bộ lọc thông minh theo Thể loại, Mức giá và Tác giả tiêu biểu.
   - Hiệu ứng rê chuột (*Hover Style*) hiển thị nút **Xem nhanh (Quick View)** và nút **Yêu thích (Wishlist)**.
   - Huy hiệu giảm giá `% Giảm` màu đỏ thương hiệu `#C92127` nổi bật ở góc trên bên trái.

2. **Trang Chi Tiết Sản Phẩm (Single Product Page)**:
   - Bố cục 2 cột tiêu chuẩn: Cột trái ảnh bìa sắc nét kèm Lightbox phóng to; cột phải là Typography sách tao nhã, giá ưu đãi kèm giá niêm yết gạch ngang.
   - Nút hành động kép (*Dual CTA*): **"Thêm vào giỏ hàng"** (không reload trang) và **"Mua ngay"** (chuyển thẳng đến trang thanh toán).
   - Khối trích dẫn đắt giá từ tác phẩm (*Book Quote Box*) viền đỏ mận `#C92127`.
   - Bảng thông số thuộc tính sách chuẩn xuất bản (Tác giả, NXB Trẻ, Năm XB, Số trang, Khổ sách, ISBN, Bìa mềm tay gập, Trọng lượng).
   - Hệ thống 4 Tab chuyên sâu:
     - **Tab 1: Giới thiệu tác phẩm & Giá trị đọc**
     - **Tab 2: Thông số kỹ thuật & Bản quyền NXB Trẻ**
     - **Tab 3: Quy cách đóng gói 3 lớp chống cấn móp**
     - **Tab 4: Đánh giá & Nhận xét từ độc giả (Social Proof)**
   - Khối **Sách cùng thể loại / Gợi ý thêm** (*Related Products*) kích thích gia tăng giá trị đơn hàng.

---

## 2. Cấu Hình Trang Cửa Hàng (Shop Page) Trong Flatsome

Truy cập **WordPress Admin** → **Appearance (Giao diện)** → **Customize (Tùy biến)** → **WooCommerce (Shop)**:

### A. Bố Cục Danh Mục (Category Page)
1. **Layout**: Chọn `Left Sidebar` (thanh lọc nằm bên trái, danh sách sách nằm bên phải).
2. **Shop Header**: Chọn `Simple` hoặc `Transparent` với tiêu đề trang trang nhã.
3. **Products per row (Desktop)**: Đặt `4` cột (hoặc `3` cột nếu muốn bìa sách hiển thị to hơn).
4. **Products per row (Mobile)**: Đặt `2` cột.

### B. Hiển Thị Thẻ Sách (Product Box)
1. **Product Box Style**: Chọn `Shade` hoặc `Normal` có viền nhẹ.
2. **Image Hover**: Chọn `Zoom` hoặc `Fade in back image`.
3. **Image Size**: Chọn `Equal Image Heights` (tỉ lệ 2:3) để bìa sách 25 ấn bản luôn thẳng hàng tăm tắp, không bị lệch hàng.
4. **Add to Cart Button**: Chọn `Show on hover` hoặc `Always show (Button inside/under)`.
5. **Quick View**: Bật `Enable Quick View` → Hiển thị nút kính lúp xem nhanh không cần rời trang.
6. **Sale Badge**: Chọn kiểu tròn hoặc nhãn chữ nhật bo góc, màu nền `#C92127`.

---

## 3. Cấu Hình Trang Chi Tiết Sản Phẩm (Single Product Page)

Truy cập **Customize** → **WooCommerce** → **Product Page**:

### A. Bố Cục Trang Chi Tiết
1. **Product Layout**: Chọn `Right Sidebar` hoặc `No Sidebar` (khuyên dùng `No Sidebar` để trang sách thoáng đãng, tập trung vào nội dung đọc).
2. **Product Image Width**: Chọn `1/2` (50% cho ảnh bìa, 50% cho thông tin mua hàng).
3. **Image Zoom / Lightbox**: Bật `Enable Image Zoom` và `Enable Lightbox` để độc giả có thể phóng to xem chi tiết bìa trước và bìa sau.

### B. Cấu Hình Các Tab Nội Dung (Product Tabs)
1. **Tabs Style**: Chọn `Pills` hoặc `Line` (màu gạch chân đỏ `#C92127`).
2. **Tab Alignment**: Căn trái (`Left`).
3. **Thêm Custom Tab "Quy cách đóng gói"**:
   - Sử dụng plugin **Custom Product Tabs for WooCommerce** hoặc chèn shortcode Flatsome:
   ```html
   <div class="packaging-box" style="background:#FFFBEB; border:1px solid #FDE68A; padding:20px; border-radius:12px;">
     <h4 style="color:#78350F; margin-top:0;">🛡️ Quy Chuẩn Đóng Gói 3 Lớp Từ DuwcsAnhLib:</h4>
     <ul>
       <li><strong>Lớp 1:</strong> Màng co niêm phong chống ẩm và trầy xước bìa.</li>
       <li><strong>Lớp 2:</strong> Bọc xốp bóng khí (bubble wrap) 2-3 lớp bảo vệ 4 góc mép gáy.</li>
       <li><strong>Lớp 3:</strong> Hộp carton 3 lớp cứng cáp dán băng keo niêm phong thương hiệu.</li>
     </ul>
     <p style="margin-bottom:0; font-size:13px; color:#92400E;">Cam kết đổi mới miễn phí 100% trong 7 ngày nếu sách bị lỗi in ấn hoặc cấn móp trong quá trình vận chuyển.</p>
   </div>
   ```

### C. Nút Mua Hàng Nhanh (Buy Now Button)
Để thêm nút **"MUA NGAY (GIAO TẬN NƠI)"** bên cạnh nút "Thêm vào giỏ", thêm đoạn mã sau vào file `functions.php` của Flatsome Child Theme:
```php
// Thêm nút Mua Ngay chuyển thẳng đến Checkout
add_action('woocommerce_after_add_to_cart_button', 'duwcsanhlib_quick_buy_button', 20);
function duwcsanhlib_quick_buy_button() {
    global $product;
    echo '<button type="submit" name="duwcsanhlib_quick_buy" value="' . esc_attr($product->get_id()) . '" class="single_add_to_cart_button button alt quick-buy-btn" style="background-color:#1C1917; color:#FFFFFF; margin-left:10px;">⚡ MUA NGAY (COD)</button>';
}

add_filter('woocommerce_add_to_cart_redirect', 'duwcsanhlib_redirect_checkout');
function duwcsanhlib_redirect_checkout($url) {
    if (isset($_REQUEST['duwcsanhlib_quick_buy'])) {
        return wc_get_checkout_url();
    }
    return $url;
}
```

---

## 4. Tùy Biến CSS Nâng Cao Cho Nhận Diện DuwcsAnhLib

Thêm vào **Customize** → **Additional CSS**:

```css
/* Màu chủ đạo thương hiệu DuwcsAnhLib */
:root {
  --dal-red: #C92127;
  --dal-amber: #D97706;
  --dal-bg: #FAF8F5;
}

/* Tùy biến hộp trích dẫn sách */
.book-quote-box {
  background-color: #F8F9FA;
  border-left: 4px solid var(--dal-red);
  padding: 14px 18px;
  border-radius: 0 10px 10px 0;
  font-style: italic;
  font-size: 14px;
  color: #374151;
  margin: 16px 0;
}

/* Thẻ giảm giá phong cách hiện đại */
.badge-circle.sale-badge {
  background-color: var(--dal-red) !important;
  font-weight: 800;
  letter-spacing: 0.5px;
  border-radius: 6px !important;
  padding: 4px 8px !important;
}

/* Bảng thông số thuộc tính sách */
.woocommerce-product-attributes {
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
}
.woocommerce-product-attributes th {
  background-color: #F9FAFB;
  font-weight: 700;
  color: #1F2937;
  width: 35%;
}
.woocommerce-product-attributes td {
  color: #4B5563;
}
```

---
*Tài liệu thuộc bộ hồ sơ bàn giao dự án DuwcsAnhLib 2026.*

