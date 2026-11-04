# Mộc Thư — bộ chuẩn bị triển khai WordPress/WooCommerce

Một cuốn sách, một khoảng bình yên.

Đây là bài cá nhân mô phỏng cửa hàng sách giấy, không phải cửa hàng đang kinh doanh. Giá bán và tồn kho trong dữ liệu là giả lập. Không chuyển tiền thật.

## Trạng thái bàn giao

Bộ này cung cấp dữ liệu, nội dung và quy trình cấu hình; **không phải bản sao một website WordPress đã cài xong**. Người dùng xác nhận chưa có Flatsome hợp lệ. Không đóng gói theme cha, WordPress core hoặc thư viện của BookVerse. Chưa tạo child theme vì chưa kiểm tra bộ cài/phiên bản thực tế. Không cần plugin nghiệp vụ riêng: WooCommerce đã đáp ứng sản phẩm, tài khoản, đơn hàng, COD, BACS và phí giao hàng.

## Điều kiện và thứ tự cài

1. Máy Windows có quyền cài ứng dụng, kết nối internet để tải Local, WordPress và WooCommerce. Tải Local từ https://localwp.com/ — không cần mua hosting/tên miền cho bài chạy trên máy.
2. Làm theo [hướng dẫn cài đặt](docs/01-cai-dat.md). Ghi phiên bản thực tế vào [biên bản nghiệm thu](docs/05-nghiem-thu.md).
3. Cấu hình WooCommerce bằng [hướng dẫn vận hành](docs/02-woocommerce.md).
4. Nhập `data/san-pham.csv` và ảnh theo [hướng dẫn dữ liệu](docs/03-du-lieu.md). Bảng `data/nguon-sach.csv` chỉ để kiểm chứng, **không nhập vào WordPress**.
5. Tạo trang và bài viết từ `content/`; có thể nhập `content/noi-dung.xml` bằng công cụ WordPress Importer miễn phí rồi kiểm tra lại. Không nhập lại WXR nhiều lần tùy tiện.
6. Khi có Flatsome hợp lệ, thực hiện [hướng dẫn Flatsome Classic](docs/04-flatsome.md). Giao diện hiện chưa được kiểm thử với theme thực tế.
7. Thực hiện toàn bộ [checklist nghiệm thu](docs/05-nghiem-thu.md), chụp bằng chứng và tập [kịch bản bảo vệ](docs/07-bao-ve.md).

## Cấu trúc

| Thư mục | Mục đích |
|---|---|
| `data/` | CSV sản phẩm và nguồn ấn bản; giá tham khảo tách khỏi giá demo |
| `assets/` | Bìa chữ minh họa PNG tự tạo, không phải bìa chính thức |
| `content/` | Nội dung trang, 3 blog và WXR nhập nội dung |
| `docs/` | Cài đặt, WooCommerce, Flatsome, kiểm thử, đối chiếu BookVerse |
| `tools/` | Công cụ Python xây dựng/kiểm tra dữ liệu, không cài lên WordPress |
| `tasks/` | Kế hoạch và trạng thái thực hiện |

Các đường dẫn trong bộ tài liệu tính từ thư mục `moc-thu`. Mã tiện ích được giao nguyên file trong `tools/`, không có mã chạy trên máy chủ website. Không upload cả gói bàn giao vào thư mục web công khai.

## Chi phí và Flatsome

WordPress, WooCommerce và môi trường Local cho bài thực hành không yêu cầu mua hosting. Flatsome thương mại không nằm trong ngân sách 0 đồng nếu bạn chưa có quyền sử dụng. Có thể xin bộ cài/giấy phép hợp lệ từ giảng viên theo điều kiện cấp phép; nếu không có, cần thống nhất thay theme miễn phí trước khi thay hướng giao diện. Gói này không âm thầm đổi theme.

Flatsome Classic (dòng 3, UX Builder/shortcode) khác Flatsome Site Builder (dòng 4, WordPress blocks). Không áp dụng hướng dẫn UX Builder cho sản phẩm mới chỉ vì cùng tên Flatsome. Nguồn đối chiếu ngày 04/11/2026: https://flatsome.com/classic-vs-site-builder .

## Giới hạn kiểm thử

Đã kiểm tra ZIP tham khảo và dữ liệu bằng công cụ tại máy làm việc. Máy chưa có PHP/Local được tìm thấy; Docker CLI có nhưng Docker engine không chạy. Chưa chạy WordPress, chưa nhập trên WooCommerce và chưa kiểm thử giao dịch/giao diện. Xem báo cáo kiểm tra thực tế trong `docs/08-ket-qua-kiem-tra.md`; checklist chưa chạy không được coi là đạt.
