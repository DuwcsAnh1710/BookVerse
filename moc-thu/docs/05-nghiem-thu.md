# Checklist nghiệm thu trên WordPress thực tế

Chưa đánh dấu đạt cho các bước chưa chạy. Điền ngày, phiên bản, kết quả và tên ảnh/log sau từng ca. Các trạng thái kỳ vọng dưới đây không phải bằng chứng đã kiểm thử.

Môi trường: Windows ___; Local ___; WordPress ___; WooCommerce ___; PHP ___; Flatsome (Classic/Site Builder) ___; phiên bản ___; child theme ___; trình duyệt ___; ngày ___ .

| ID | Thao tác | Kỳ vọng | Kết quả / bằng chứng |
|---|---|---|---|
| 01 | Cài/kích hoạt WooCommerce và theme hợp lệ | Không lỗi PHP, không thông báo thiếu parent | Chưa chạy |
| 02 | Nếu có child/plugin tự viết sau này, cài ZIP và kích hoạt | Không fatal; không sửa parent/core | Chưa áp dụng: gói chưa có child/plugin |
| 03 | Import CSV lần đầu | 25 sản phẩm, 25 SKU riêng, 5 danh mục | Chưa chạy |
| 04 | Kiểm tra đủ 25 sách | Tên/thuộc tính tiếng Việt đúng, khớp nguồn, 25 ảnh đúng SKU | Chưa chạy |
| 05 | Update một SKU bằng CSV chỉ giá | Giá đổi, tổng số sản phẩm vẫn 25, ảnh và tồn không mất | Chưa chạy |
| 06 | Tìm “Khu Tập Thể”; từ không tồn tại | Kết quả đúng; trạng thái không kết quả rõ ràng | Chưa chạy |
| 07 | Danh mục Văn học, khoảng 60–110 nghìn, sắp giá tăng | Kết quả đúng đồng thời; xóa lọc khôi phục đúng | Chưa chạy |
| 08 | Shop 12 sách/trang → trang 2/3, đổi sắp xếp | Không lặp/mất sản phẩm ngoài quy tắc; tổng 25 khi không lọc | Chưa chạy |
| 09 | Trang chi tiết và sách liên quan | Đủ ảnh, tác giả, NXB, năm, trang, kích thước; không review giả | Chưa chạy |
| 10 | Thêm 1 sách, tăng lên 2, xóa khỏi giỏ | Tổng cập nhật; giỏ trống hiển thị đúng | Chưa chạy |
| 11 | Tạo tài khoản A và B, đăng nhập/đăng xuất | Vai trò Customer, không vào quản trị đơn | Chưa chạy |
| 12 | Đặt MT-001 số lượng 2, COD bằng A | 99.000×2 + 25.000 = 223.000đ; trang cảm ơn và mã đơn | Chưa chạy |
| 13 | Xem đơn COD trong admin và tài khoản A | Cùng mã/tổng; thường Processing cho sách vật lý | Chưa chạy |
| 14 | Kiểm tra tồn MT-001 trước/sau đơn trên | Tồn ban đầu 11 → 9; Processing→Completed không giảm lần hai | Chưa chạy |
| 15 | B đặt MT-025 số lượng 3, BACS | 27.000×3 + 25.000 = 106.000đ; On hold, chỉ thông tin demo | Chưa chạy |
| 16 | Xác nhận BACS giả lập, đổi Processing rồi Completed | Đúng trạng thái; không tự thanh toán ngân hàng; không trừ tồn hai lần | Chưa chạy |
| 17 | Tạo đơn mới rồi Cancelled; thử Refund/Restock riêng | Ghi tồn trước/sau, hoàn đúng số lượng; không hứa hoàn tiền thật | Chưa chạy |
| 18 | Đặt số lượng vượt tồn, số 0/âm, sản phẩm hết | WooCommerce từ chối hợp lý, không tồn âm | Chưa chạy |
| 19 | Giỏ 1 và nhiều sách ở Việt Nam | Phí 25.000 mỗi đơn, không nhân số cuốn | Chưa chạy |
| 20 | Thử địa chỉ ngoài vùng giao hàng | Không đặt được với phương thức vận chuyển sai | Chưa chạy |
| 21 | A sao chép URL view-order, mở bằng B rồi khi logout | Không lộ chi tiết đơn A; thông báo từ chối/đăng nhập phù hợp | Chưa chạy |
| 22 | Kiểm tra menu, footer, 3 bài blog, các chính sách | Không link rỗng/404, có nhãn học tập, không thông tin nhóm cũ | Chưa chạy |
| 23 | Desktop 1440px; tablet 768px; điện thoại 375px | Không tràn ngang, tên dài không đè nút, ảnh đủ nhãn minh họa | Chưa chạy |
| 24 | Bàn phím Tab/Enter, zoom 200%, lỗi checkout | Focus rõ, nhãn form đầy đủ, thông báo lỗi hiểu được | Chưa chạy |
| 25 | Đóng/mở lại Local, khôi phục một bản export thử | Site, ảnh, tài khoản/đơn còn đúng | Chưa chạy |

Các phép tính trên dựa dữ liệu ban đầu trong gói, thuế/coupon tắt. Nếu đã sửa giá, hãy tính lại trước khi chạy; không thay kết quả kỳ vọng bằng con số đang hiển thị chỉ để cho qua.

Bằng chứng đề xuất: `01-versions.png`, `02-import-log.png`, `03-shop-mobile.png`, `04-cod-confirmation.png`, `05-bacs-admin.png`, `06-stock-before-after.png`, `07-account-isolation.png`. Che mật khẩu, token và giấy phép. Không dùng hình thiết kế hoặc CSV làm bằng chứng checkout đã hoạt động.
