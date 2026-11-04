# Cấu hình và vận hành WooCommerce

Tất cả phần dưới là thao tác quản trị, không cần code bổ sung. Nhãn menu có thể được dịch khác nhau theo phiên bản.

## Thiết lập cửa hàng demo

WooCommerce → Settings → General: Việt Nam, chỉ bán/giao đến Việt Nam, tiền Đồng Việt Nam (VND), 0 chữ số thập phân. Địa chỉ cửa hàng demo: “Khu thực hành Mộc Thư — địa chỉ minh họa”, thành phố Hồ Chí Minh. Không điền địa chỉ một cửa hàng thật. Bật thông báo cửa hàng: **Bài thực hành — giá và tồn kho giả lập, không giao hàng và không thu tiền thật.**

Không cấu hình thuế trong bài mô phỏng; ghi rõ quyết định này trong báo cáo, không dùng như hướng dẫn thuế khi kinh doanh. Tắt coupon nếu không trình bày khuyến mãi. Products → Inventory: bật quản lý tồn kho, không cho backorder; dùng ngưỡng sắp hết 2 và hết hàng 0. Products → Reviews: có thể tắt đánh giá vì chưa có khách hàng thật; tuyệt đối không nhập sao/nhận xét giả.

## Vận chuyển 25.000đ mỗi đơn

Settings → Shipping → Shipping zones → Add zone “Việt Nam demo”, vùng Việt Nam. Add shipping method → Flat rate. Tên hiển thị “Giao hàng tiêu chuẩn — mô phỏng”, Tax status None, Cost **25000**. Không dùng `25000 * [qty]`, không nhập phí theo shipping class. Không thêm các phương thức khác trong cùng vùng khi không dùng. Khu vực ngoài Việt Nam không có phương thức giao hàng.

Muốn sửa phí: mở lại Flat rate của vùng Việt Nam, đổi Cost và Save. Kiểm tra giỏ 1 cuốn và 3 cuốn: phí phải vẫn 25.000đ. Sách là sản phẩm vật lý, không tích Virtual. Nguồn: https://woocommerce.com/document/flat-rate-shipping/ (04/11/2026).

## COD và chuyển khoản mô phỏng

Settings → Payments (có thể nằm trong Take offline payments): chỉ bật Cash on delivery và Direct bank transfer. Không bật WooPayments, thẻ, PayPal hoặc QR thật.

COD: Title “COD — đặt đơn thử”; Description/Instructions “Đơn học tập, không giao hàng và không thu tiền. Không cung cấp thông tin cá nhân thật.” Chỉ áp dụng phương thức giao hàng demo; không cho đơn virtual. Đơn sách COD thường vào Processing. Chỉ chuyển Completed trong tình huống giả lập đã giao/thu tiền, ghi order note “Mô phỏng hoàn tất, không có giao dịch thật”.

BACS: Title “Chuyển khoản — mô phỏng, không chuyển tiền”; Description/Instructions “Chỉ thử quy trình chờ xác nhận. Không chuyển tiền. Quản trị viên xác nhận giả lập trong bài học.” Account name “MOC THU DEMO”; Bank name “NGAN HANG GIA LAP”; Account number “DEMO-KHONG-CHUYEN-TIEN”. Không cung cấp số tài khoản ngân hàng thật hoặc mã QR. Nếu phiên bản kiểm tra định dạng số, để trống dòng tài khoản và giữ hướng dẫn minh họa; không thay bằng một số có vẻ thật.

BACS là thủ công, không tự xác nhận tiền. Đơn thường On hold; trong bài thực hành thêm note “Đã xác nhận giả lập”, đổi Processing rồi Completed. Nguồn: https://woocommerce.com/document/bacs/ và https://woocommerce.com/document/cash-on-delivery/ (04/11/2026).

## Tài khoản

Settings → Accounts & Privacy: cho tạo tài khoản trong My Account và lúc checkout. Để bài kiểm thử lịch sử đơn rõ ràng, tắt guest checkout, yêu cầu đăng nhập/đăng ký trước đặt đơn. Dùng chức năng tài khoản chuẩn; không viết trang login riêng. Gán trang bảo mật được nhập ở Settings → Privacy và chính sách thanh toán trong WooCommerce khi có tùy chọn tương ứng.

Tài khoản học tập dùng email `khach-a@example.test`, `khach-b@example.test` và mật khẩu do bạn tự đặt. Có thể tạo user vai trò Customer trong Users để thử; không cấp Administrator cho khách. Dùng hai cửa sổ trình duyệt/phiên ẩn danh để tránh lẫn phiên. Xem đơn tại My Account → Orders; quản trị xem WooCommerce → Orders.

## Tồn kho và đơn hàng

Không trừ tồn thủ công sau mỗi đơn: WooCommerce quản lý việc giảm/hoàn tồn theo trạng thái và hành động. Ghi số trước/sau khi test; tránh suy luận từ nhãn trạng thái mà không đo. Với sản phẩm tồn 10, đặt 2 cuốn COD hoặc BACS rồi kiểm tra thường còn 8. Chuyển tiếp Processing/Completed không được trừ thêm lần nữa. Hủy đơn đã giảm tồn phải kiểm tra khôi phục; nếu hoàn tiền, chọn restock items khi muốn hoàn kho. BACS/COD không tự hoàn tiền ngân hàng; bài này không có tiền thật.

Sửa sách: Products → All Products → Edit; General đổi Regular price; Inventory sửa SKU/tồn kho; Product categories chọn đúng thể loại; Attributes chỉnh thông tin ấn bản đã kiểm chứng. Khi thay ấn bản, kiểm tra lại toàn bộ tác giả/NXB/năm/số trang và nguồn, không chỉ đổi ảnh bìa.

## Cửa hàng, tìm kiếm và bộ lọc

Dùng trang Shop và archive danh mục của WooCommerce. Đặt 12 sản phẩm/trang và 3–4 cột desktop, 2 cột mobile nếu vẫn đủ rộng cho tiêu đề; 1 cột ở màn hình hẹp nếu cần. Dùng tìm kiếm sản phẩm ở header; thử từ khóa có dấu và không có dấu, không hứa tìm theo tác giả nếu mặc định chưa hỗ trợ.

Với Flatsome Classic: xác định Shop Sidebar trong Widgets/Theme Options sau khi cài. Kiểm tra các widget WooCommerce có thực tế: Product Categories và Filter Products by Price. Chèn chúng vào sidebar của archive sản phẩm, không chèn tùy tiện vào trang chủ. Nếu phiên bản không có widget tương thích, kiểm tra Product Filters block trong ngữ cảnh Product Collection được WooCommerce hỗ trợ; không mặc định block này thay được sidebar Classic. Ghi phiên bản và chạy kiểm thử kết hợp danh mục/giá/sắp xếp/phân trang trước khi chốt. Không mua extension lọc khi chưa chứng minh core không đáp ứng.

Nếu thiếu công cụ lọc khả dụng ở bộ cài thực tế, đây là hạng mục **chưa đạt**, cần xử lý theo phiên bản; các liên kết danh mục đơn thuần không được báo cáo là đã hoàn tất lọc khoảng giá. Tài liệu block: https://woocommerce.com/document/woocommerce-store-editing/customizing-shop-page-catalog/filter-products/ .
