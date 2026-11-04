# BookVerse: phần tham khảo và phần xây dựng mới

Đã kiểm tra `BookVerse_Version_1-main.zip` tại thư mục đầu vào, không chạy mã của dự án cũ. SHA-256: `49cab7513fc718f53931289ce24d385b7a3f7dacd800276ae86f275a41ed055b`.

ZIP có 10.429 entry (gồm thư mục), trong đó 10.274 entry nằm trong `node_modules`. Kiểm tra CRC bằng Python `zipfile.testzip()` không phát hiện entry hỏng. Không giải nén/chạy toàn bộ thư viện kèm theo.

## Bằng chứng đọc mã

- `backend/package.json`: Express, Mongoose, JWT, bcrypt; scripts khai báo Jest. Không tìm thấy file test/spec của dự án ngoài node_modules trong danh sách ZIP. Khai báo công cụ test không chứng minh có test đạt.
- `backend/models/Product.js`, `Order.js`: dữ liệu sản phẩm và đơn theo MongoDB/Mongoose; đơn có liên kết seller và nhiều trạng thái riêng. Không chuyển schema này sang WordPress.
- `backend/server.js`: khởi động Express, kết nối DB, mount các API. Mặc định cổng 5000 nếu không có PORT.
- `frontend/assets/js/config.js`: URL API local cổng 5000, cùng URL staging/production ghi trong mã. Chưa xác minh các endpoint từ xa đang hoạt động; không tái sử dụng tên miền đó cho Mộc Thư.
- `backend/routes/auth.js`: route quên mật khẩu có dòng chưa triển khai gửi email OTP, trả thông báo “would be sent”. Vì vậy README nói khôi phục bằng OTP không đủ chứng minh gửi thư thật đã hoạt động.
- `backend/routes/orders.js`: có tạo đơn, giảm stock và truy vấn theo customer; mới đọc mã, chưa chứng minh tính đúng khi chạy đồng thời hoặc bảo mật toàn bộ luồng.

README có tuyên bố Lighthouse 90+, thanh toán tích hợp và nhiều tính năng hoàn tất. Chưa có kết quả đo/chạy để xác nhận. README nhắc LICENSE nhưng không tìm thấy file LICENSE cấp dự án trong ZIP (ngoài thư viện); không dựa vào dòng MIT trong package.json để đóng gói lại toàn bộ tài nguyên.

## Phạm vi sử dụng

| Phần | Xử lý ở Mộc Thư |
|---|---|
| Ý tưởng danh mục sách, xem chi tiết, giỏ và đơn | Tham khảo luồng chức năng phổ biến; triển khai bằng WooCommerce |
| Node.js, Express, MongoDB, JWT | Không chuyển sang, không cài để vận hành website mới |
| UI PHP/CSS/JS, logo, ảnh cũ | Không sao chép vào theme Mộc Thư |
| Người bán, hoa hồng, ví, dashboard marketplace | Loại khỏi phạm vi bài cá nhân |
| Thành viên/địa chỉ/email trong README cũ | Không dùng làm danh tính hoặc liên hệ của người làm bài |
| Dữ liệu sách | Tra cứu mới từ nguồn NXB, không tin dữ liệu seed cũ |
| Nội dung/ảnh Mộc Thư | Viết mới; placeholder chữ tự tạo |
| Chính sách, hướng dẫn, checklist | Soạn mới theo cấu hình local và nghiệp vụ WooCommerce |

Cách trình bày trung thực: “Em dùng BookVerse làm tài liệu tham khảo về phạm vi chức năng. Em không tham gia dự án nhóm đó. Bài Mộc Thư sử dụng WordPress/WooCommerce, có dữ liệu và nội dung chuẩn bị riêng; chức năng chuẩn thuộc nền tảng, phần em cấu hình và kiểm thử được ghi trong biên bản.” Chỉ đổi câu cuối thành “đã kiểm thử” cho các ca có bằng chứng.
