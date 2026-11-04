# Hướng Dẫn Nhập Dữ Liệu DuwcsAnhLib Vào WordPress & WooCommerce

> [!IMPORTANT]
> **Quy tắc cốt lõi:** Không tải trực tiếp file zip bàn giao vào WordPress. Từng loại dữ liệu cần được nạp qua đúng chức năng quản trị tương ứng.

---

## 1. Nạp Thư Viện Ảnh Bìa (Assets)
1. Trong WordPress Admin, vào **Media (Media)** → **Thêm mới (Add New Media File)**.
2. Kéo thả toàn bộ 25 file ảnh trong thư mục `duwcsanhlib/assets/covers/` (`DAL-001.png` đến `DAL-025.png`) cùng file `logo-duwcsanhlib.png` và `banner-duwcsanhlib.png` vào thư viện.
3. Toàn bộ ảnh sẽ được lưu trữ cục bộ trong WordPress để bạn gán làm ảnh đại diện sản phẩm hoặc trang chủ.

---

## 2. Nhập 25 Sản Phẩm Sách (CSV Import)
1. Vào menu **Sản phẩm (Products)** → **Tất cả sản phẩm (All Products)**.
2. Bấm nút **Bắt đầu nhập (Start Import)** hoặc **Nhập (Import)** ở đầu trang.
3. Tại ô **Chọn tệp CSV (Choose file)**, chọn tệp:
   `duwcsanhlib/data/san-pham-duwcsanhlib.csv`
4. Để nguyên tùy chọn mặc định, bấm **Tiếp tục (Continue)**.
5. Kiểm tra bảng Ánh xạ cột (Column Mapping): Hệ thống sẽ tự động ghép các trường như `SKU`, `Name` (Tên), `Regular price` (Giá bán), `Categories` (Danh mục: Văn học, Kinh tế,...), `Description` (Mô tả), `Attributes` (Tác giả, NXB, Năm,...).
6. Bấm **Chạy trình nhập (Run the Importer)**.
7. Chờ 15–30 giây: Hệ thống sẽ báo nhập thành công 25 sản phẩm vào WooCommerce.

---

## 3. Nhập Các Trang & Bài Viết Mẫu (XML Import)
1. Vào menu **Công cụ (Tools)** → **Nhập vào (Import)**.
2. Tìm mục **WordPress** ở cuối danh sách → Nếu chưa cài thì bấm **Cài đặt ngay (Install Now)**, sau đó bấm **Chạy trình nhập (Run Importer)**.
3. Chọn tệp:
   `duwcsanhlib/content/duwcsanhlib-noi-dung.xml`
4. Bấm **Tải tệp lên và nhập (Upload file and import)**.
5. Tại màn hình gán tác giả, chọn gán các bài viết cho tài khoản Quản trị viên (Admin) hiện tại của bạn.
6. Bấm **Submit**.
7. Các trang như **Giới thiệu, Liên hệ, Chính sách giao hàng, Đổi trả, Bảo mật** cùng 3 bài viết blog sẽ xuất hiện ngay trong mục **Trang (Pages)** và **Bài viết (Posts)**.

---

## 4. Thiết lập Trang chủ & Menu
1. Vào **Cài đặt (Settings)** → **Đọc (Reading)**:
   - Mục *Bố cục trang chủ (Your homepage displays)*: Chọn **Một trang tĩnh (A static page)**.
   - *Trang chủ (Homepage)*: Chọn trang **Trang chủ** (hoặc trang Cửa hàng/Shop nếu muốn hiện ngay danh sách sách).
   - *Trang bài viết (Posts page)*: Chọn trang blog (Góc đọc).
   - Bấm **Lưu thay đổi (Save Changes)**.
2. Vào **Giao diện (Appearance)** → **Menu (Menus)**:
   - Tạo menu chính (Main Menu): Thêm các liên kết: Trang chủ, Cửa hàng (Shop), Giới thiệu, Blog, Liên hệ.
   - Gán vị trí hiển thị: **Primary Menu (Menu chính)**.

