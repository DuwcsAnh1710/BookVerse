# Kịch bản bảo vệ 8–10 phút

## Trước buổi trình bày

Khởi động Local và site, mở trang chủ cùng WP Admin. Chuẩn bị bản sao lưu, hai tài khoản Customer, một trình duyệt ẩn danh, checklist đã điền. Chỉ dùng dữ liệu giả lập. Nếu chưa có Flatsome, phải báo trước rằng bài chưa hoàn tất giao diện theo yêu cầu, không dùng tài liệu thiết kế để thay bằng chứng chạy theme.

## Trình bày

1. **Một phút:** giới thiệu Mộc Thư, người đọc mục tiêu, thông điệp, phạm vi cửa hàng đơn. Giải thích ngân sách local và điều kiện giấy phép Flatsome.
2. **Một phút:** mở báo cáo BookVerse, chỉ ra backend cũ khác WordPress và phần không kế thừa. Nêu ví dụ route OTP còn thiếu gửi email để giải thích vì sao không tin toàn bộ README.
3. **Hai phút:** mở Shop, tìm sách, lọc giá/thể loại, xem chi tiết. Mở bảng nguồn bên ngoài WordPress, đối chiếu một ISBN và năm/lần in. Giải thích giá/tồn demo và bìa minh họa.
4. **Hai phút:** tài khoản A thêm 2 MT-001, kiểm tra tổng 223.000đ với dữ liệu ban đầu, đặt COD. Mở đơn trong admin và lịch sử khách, kiểm tra tồn.
5. **Một phút:** mở đơn BACS đã tạo thử; giải thích On hold chờ xác nhận thủ công. Không thao tác chuyển tiền. Mở bằng B đường dẫn đơn A để chứng minh phân quyền sau khi đã kiểm thử.
6. **Một phút:** sửa một đoạn giới thiệu bằng UX Builder nếu dùng đúng Classic; sửa một giá/tồn trong Products. Giải thích hai nơi này có mục đích khác nhau.
7. **Một phút:** trình bày màn hình mobile, các ca kiểm thử đạt/chưa đạt, giới hạn local, chưa vận hành kinh doanh và hướng phát triển vừa sức.

## Câu hỏi thường gặp

**Tại sao không viết lại backend?** WooCommerce có nghiệp vụ chuẩn, giúp bài cá nhân tập trung cấu hình, dữ liệu và kiểm thử; tránh viết lại đăng nhập/đơn hàng và tăng rủi ro.

**Em tự làm phần nào?** Nêu đúng phần đã tự thực hành: lựa chọn phạm vi, nhập/đối chiếu sách, cấu hình giao dịch, dựng bố cục, biên tập nội dung và kiểm thử. Bộ tài liệu có hỗ trợ AI; không nhận là tác giả của WordPress, WooCommerce, Flatsome hay dự án nhóm cũ.

**WordPress, WooCommerce, Flatsome khác nhau ra sao?** WordPress quản lý nội dung/tài khoản và nền tảng; WooCommerce bổ sung sản phẩm, giỏ, checkout, đơn; Flatsome quyết định nhiều phần trình bày và công cụ dựng giao diện. Child theme giữ tùy chỉnh hiển thị khi cập nhật parent.

**COD có nghĩa đã trả tiền chưa?** Chưa. Processing là trạng thái xử lý; cần xác nhận thu tiền trong nghiệp vụ thực tế. Bài học chỉ giả lập.

**Số trang/năm lấy từ đâu?** Trang ấn bản NXB Trẻ, có URL và ngày tra cứu; kiểm tra cùng ISBN/lần in. Không trộn ấn bản vì trùng tên.

**Tại sao không dùng ảnh bìa thật?** Chưa xác định quyền phân phối; dùng placeholder tự tạo và hướng dẫn thay ảnh khi có quyền.

**Đưa lên internet có dùng ngay không?** Chưa. Cần hosting/tên miền hoặc phương án triển khai phù hợp, giấy phép, chính sách thực, bảo mật, sao lưu và kiểm thử đầy đủ. Bộ này phục vụ local, không tích hợp thanh toán thật.
