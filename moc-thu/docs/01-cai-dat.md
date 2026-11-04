# Cài trên Windows với Local

## 1. Cài môi trường — thao tác trên máy

Tải trình cài Windows tại https://localwp.com/ . Hướng dẫn hãng: https://localwp.com/help-docs/getting-started/installing-local/ (tra cứu 04/11/2026). Chạy trình cài; nếu Windows hỏi quyền, kiểm tra đúng ứng dụng Local trước khi chấp nhận. Mở Local, chọn tạo site mới, đặt tên **Moc Thu**, dùng cấu hình Preferred. Nếu máy có xung đột cổng, đóng máy chủ web khác hoặc đọc hướng dẫn sửa lỗi của Local; không sửa ngẫu nhiên cấu hình hệ thống.

Đặt tên người quản trị riêng và mật khẩu mạnh do bạn tự chọn. Không dùng mật khẩu trong tài liệu mẫu. Email quản trị dùng địa chỉ bạn kiểm soát nếu cần nhận thư; không đưa mật khẩu vào báo cáo. Nhấn Add Site, chờ khởi tạo, Start Site. Nút WP Admin đưa vào quản trị; Open Site mở trang khách. Địa chỉ thường có dạng `moc-thu.local`, nhưng dùng đúng URL Local hiển thị. Đường quản trị là URL đó cộng `/wp-admin/`.

Trong Local, chọn Trust nếu muốn tin cậy chứng chỉ HTTPS local theo hướng dẫn ứng dụng. Site local chỉ chạy khi máy và dịch vụ đang bật; không phải website công khai, không có tên miền internet được đăng ký.

## 2. Cấu hình WordPress — thao tác quản trị

Settings → General: tên Mộc Thư, tagline “Một cuốn sách, một khoảng bình yên.”, ngôn ngữ Tiếng Việt, múi giờ Ho Chi Minh hoặc UTC+7. Settings → Permalinks: Post name, lưu. Settings → Reading: bật ngăn công cụ tìm kiếm lập chỉ mục cho bài demo; đây không phải cơ chế bảo vệ truy cập nếu sau này công khai.

Plugins → Add New: tìm WooCommerce của Automattic, Install, Activate. Bỏ qua dịch vụ trả phí, quảng cáo, thanh toán online, plugin tiếp thị tùy chọn. Không cần Jetpack, multi-vendor hay ví điện tử cho phạm vi này. Ghi lại phiên bản WordPress, WooCommerce, PHP đang cài.

Giữ theme mặc định do WordPress tạo trong giai đoạn chuẩn bị quản trị; đó **không phải giao diện Mộc Thư chính thức**. Chưa nghiệm thu frontend hoặc chọn theme miễn phí thay Flatsome khi chưa thống nhất với người làm bài.

## 3. Nội dung và các trang hệ thống

WooCommerce thường tạo Shop, Cart, Checkout, My Account. Kiểm tra WooCommerce → Settings → Advanced để gán đúng các trang. Không tạo hai trang thanh toán. Nếu thiếu trang, dùng công cụ tạo trang mặc định trong WooCommerce → Status → Tools sau khi sao lưu; tên công cụ có thể khác theo phiên bản.

Trang nội dung: Tools → Import → WordPress → Install Now (WordPress Importer), Run Importer, chọn `content/noi-dung.xml`. Gán tác giả cho tài khoản của bạn. Không chọn tải attachment vì file không chứa ảnh từ xa. Các trang/bài được nhập ở trạng thái nháp: mở xem rồi Publish. Các nội dung này là WordPress HTML cơ bản, **không phải file UX Builder**.

Trang chủ: tạo mới “Trang chủ”; Settings → Reading → static homepage chọn trang này sau khi dựng. Trang “Góc đọc” trống dùng làm Posts page nếu muốn trang lưu trữ blog. Tạo menu bằng các trang/danh mục thật để WordPress quản lý URL; tránh gõ link chứa tên miền local vào nội dung.

## 4. Sao lưu và khôi phục

Trước khi nhập dữ liệu hoặc thay theme: dừng chỉnh sửa, dùng Export của Local để xuất site, lưu ngoài thư mục web. Bản sao chứa cơ sở dữ liệu và tài khoản, không đưa công khai. Có thể nhập bản export vào Local để khôi phục; kiểm tra đăng nhập, đường dẫn và ảnh sau khi khôi phục. Không gộp bản export có theme thương mại vào bộ phát hành công khai.

Khi bảo vệ: mở Local → Start Site → Open Site, chuẩn bị sẵn WP Admin, dùng tài khoản khách riêng. Không cần internet để trình bày sau khi đã tải đầy đủ tài nguyên local. Email thử xem bằng Mailpit/MailHog trong Local tùy phiên bản, không khẳng định thư đã được gửi ra internet.
