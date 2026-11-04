# Hướng Dẫn Thiết Lập Landing Page Trang Chủ Bằng Flatsome UX Builder

Tài liệu này hướng dẫn bạn cách đưa giao diện Landing Page 8 section chuẩn CRO vào website WordPress sử dụng theme Flatsome.

---

## Cách 1: Nạp Tự Động Qua File XML (Khuyên Dùng)

Nếu bạn nhập nội dung qua file XML:
1. Vào **Công cụ (Tools)** → **Nhập vào (Import)** → **WordPress** → **Chạy trình nhập (Run Importer)**.
2. Tải lên tệp: `duwcsanhlib/content/duwcsanhlib-noi-dung.xml`.
3. Hệ thống sẽ tự động tạo trang **Trang chủ — DuwcsAnhLib** với đầy đủ cấu trúc shortcode UX Builder.
4. Kích hoạt làm Trang chủ tĩnh:
   - Vào **Cài đặt (Settings)** → **Đọc (Reading)**.
   - Tại dòng *Bố cục trang chủ (Your homepage displays)*: Chọn **Một trang tĩnh (A static page)**.
   - Tại ô *Trang chủ (Homepage)*: Chọn trang **Trang chủ — DuwcsAnhLib**.
   - Bấm **Lưu thay đổi (Save Changes)**.

---

## Cách 2: Sao Chép Trực Tiếp Shortcode Vào UX Builder

Nếu bạn muốn tạo thủ công trên một trang trắng có sẵn:

1. Vào **Trang (Pages)** → **Thêm trang mới (Add New Page)**.
2. Đặt tiêu đề: `Trang chủ`.
3. Tại ô **Thuộc tính trang (Page Attributes)** ở cột bên phải:
   - Mục *Giao diện (Template)*: Chọn **Page - Full Width** (hoặc **Page - No Header Transparent** tùy ý thích).
4. Mở tệp `duwcsanhlib/content/trang-chu-flatsome-shortcodes.txt` bằng Notepad hoặc VS Code.
5. Sao chép (Ctrl + A, Ctrl + C) toàn bộ nội dung trong tệp.
6. Trong trình soạn thảo WordPress:
   - Chuyển sang tab **Văn bản (Text)** hoặc mở **UX Builder**.
   - Dán toàn bộ mã shortcode vào khung nội dung.
   - Bấm **Đăng (Publish)**.
7. Khi bạn bấm **UX Builder**, giao diện trực quan với 8 Section (Banner, 4 USP, 5 Danh mục, Sản phẩm chạy Slider, Lời ngỏ thương hiệu, Tác giả, Blog, Cảm nhận) sẽ hiện ra đầy đủ và có thể kéo thả chỉnh sửa tùy ý.

---

## Tùy Biến Nâng Cao Cho Theme Flatsome

### 1. Đồng bộ Font chữ & Màu sắc trong UX Customize
Vào **Giao diện (Appearance)** → **Tùy biến (Customize)**:
- **Colors (Màu sắc):**
  - Primary Color: `#C92127` (Đỏ mận thương hiệu DuwcsAnhLib).
  - Secondary Color: `#D97706` (Hổ phách / Vàng gold).
  - Base Color (Nền): `#FAF8F5` (Màu kem giấy ngà dịu mắt).
- **Typography (Phông chữ):**
  - Headings Font (Tiêu đề): Chọn **Playfair Display** hoặc **Merriweather** (Tạo nét học thuật, cổ điển thư viện).
  - Base Font (Nội dung): Chọn **Inter**, **Roboto** hoặc **Nunito Sans** (Nét chữ rõ ràng, dễ đọc trên di động).

### 2. Thiết lập Menu Điều Hướng (Primary Menu)
Vào **Giao diện (Appearance)** → **Menu (Menus)**:
Thêm các mục liên kết theo thứ tự tối ưu trải nghiệm khách hàng:
1. **Trang chủ** (Landing Page)
2. **Cửa hàng** (`/cua-hang/` — Lưới 25 đầu sách đầy đủ)
3. **Danh mục sách** (Menu thả xuống: Văn học, Kinh tế, Tâm lý, Kỹ năng, Thiếu nhi)
4. **Về DuwcsAnhLib** (`/gioi-thieu/` — Lời ngỏ và tôn chỉ sách thật)
5. **Góc Đọc & Review** (`/blog/` — Bài viết điểm sách)
6. **Liên hệ & Hỗ trợ** (`/lien-he/` — Hotline 0933 543 987)

