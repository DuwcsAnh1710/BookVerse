# Nhập sản phẩm và ảnh

## File và ý nghĩa

`data/san-pham.csv`: dữ liệu UTF-8 có BOM, dấu phân cách phẩy, chuỗi chứa dấu phẩy được bao bằng dấu nháy kép. Không đổi dấu phân cách thành chấm phẩy khi lưu bằng Excel. Giá là số nguyên VND không có ký hiệu tiền hoặc dấu phân nhóm. SKU `MT-001`…`MT-025` là khóa ổn định của bài, không phải ISBN.

`data/nguon-sach.csv`: bảng nội bộ với URL nguồn, ngày tra cứu, ấn bản, ISBN nguồn, giá tham khảo, giá demo, ghi chú quyền ảnh. **Không upload bảng nguồn hoặc thư mục research lên web.** Không nhầm barcode 893… với ISBN. Chỉ điền ISBN nếu nguồn có; bảng thuộc tính của CSV nêu đúng năm của lần in được nguồn ghi, không phải năm xuất bản đầu tiên trên thế giới.

Ngôn ngữ Tiếng Việt được xác định từ giới thiệu/trang đọc thử tiếng Việt và thông tin dịch giả của ấn bản; đây là cách đối chiếu, không phải trường ngôn ngữ do NXB luôn công bố. Không dùng ấn bản tiếng Anh. Các thông tin cân nặng chưa cần cho phí cố định nên không nhập; kích thước sách chỉ là thuộc tính hiển thị, không giả làm kích thước gói giao hàng.

## Nhập lần đầu

1. Sao lưu Local. Vào Products → All Products → Import, chọn `san-pham.csv`. Không mở rồi lưu lại bằng ứng dụng làm mất UTF-8.
2. Lần đầu không chọn Update existing products nếu chưa có SKU này. Dấu phân cách comma. Ở mapping kiểm tra: Type→Type; SKU→SKU; Name→Name; Published→Published; Is featured?→Featured; Visibility in catalog→Catalog visibility; Short description/Description đúng trường; Regular price→Regular price; Stock→Stock quantity; In stock?→Stock status; Categories→Categories; Images→Images.
3. Attribute N name/value(s)/visible/global lần lượt ánh xạ tên/giá trị/hiển thị/toàn cục. `global=0` dùng thuộc tính riêng sản phẩm, đủ cho chi tiết sách; lọc theo thể loại dùng Categories, không cần tạo hàng loạt taxonomy tác giả.
4. CSV cố ý để Images trống nhằm không tạo hotlink hoặc URL localhost giả. Nhập, xem báo cáo. Mong đợi 25 sản phẩm, 5 danh mục. Mở ít nhất 3 sách kiểm tra dấu tiếng Việt, giá, tồn và thuộc tính, rồi kiểm tra đủ 25.
5. Nếu dữ liệu lỗi, giữ log, xác định cột; khôi phục bản sao khi cần. Không nhấn import nhiều lần để “thử may”.

## Ảnh local không phụ thuộc hotlink

Media → Add New: upload 25 file `MT-xxx.png` trong `assets/covers`. Sau đó Products → Edit từng sách theo SKU → Product image → chọn đúng PNG → alt “Bìa minh họa: [tên sách]” → Update. Với 25 cuốn, cách gán thủ công này dễ kiểm tra và không cần plugin. Không upload SVG nếu WordPress không hỗ trợ.

Nếu muốn nhập ảnh tự động sau này: upload ảnh trước, xuất CSV từ WooCommerce để lấy URL thật của thư viện site đó, giữ SKU và cột Images khi cập nhật. Không gõ đường dẫn ổ D: vào Images; máy chủ không hiểu đó là URL ảnh.

Thay bìa thật: xin/kiểm tra quyền sử dụng, xác định đúng ấn bản bằng ISBN/năm/lần in, lưu nguồn và điều kiện cấp phép, tải ảnh được phép về Media. Đặt alt phù hợp và thay ảnh cho sản phẩm. Đổi ảnh không làm thay SKU. Gói hiện không cấp quyền dùng ảnh bìa chính thức của NXB.

## Nhập cập nhật không tạo trùng

WooCommerce đối chiếu SKU/ID. Giữ SKU, chọn Update existing products, kiểm tra mapping và kết quả cập nhật. Khi chỉ đổi giá, tạo CSV chỉ gồm SKU và Regular price; **không nhập lại cột Stock của bộ demo sau khi đã đặt đơn**, vì sẽ ghi đè tồn hiện tại. Không đưa cột Images trống vào bản cập nhật ảnh đã gán nếu không muốn mất ảnh. Khi đổi ấn bản thực sự, cân nhắc SKU mới để không sửa lịch sử định danh sản phẩm cũ.

Nguồn schema và importer tích hợp: https://woocommerce.com/document/product-csv-importer-exporter/ (04/11/2026). File đã được kiểm tra cấu trúc bằng Python; chưa thay thế việc chạy import trên phiên bản WooCommerce thực tế.
