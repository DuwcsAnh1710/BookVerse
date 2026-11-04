# Báo cáo kiểm tra thực tế — 04/11/2026

## Đã chạy và có bằng chứng

| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Mở/kiểm tra ZIP BookVerse | CRC không phát hiện file hỏng; 10.429 entry, phần lớn node_modules | SHA-256 và ghi nhận trong `06-bookverse-tham-khao.md` |
| Tra cứu sách online | Đọc trực tiếp trang NXB Trẻ, chọn 25 bản có tác giả/trang/khổ/ISBN/lần in/năm/giá | `data/nguon-sach.csv`, `data/doi-chieu-an-ban.md`; HTML lưu riêng ở workspace research, không phân phối toàn trang |
| Sinh CSV | 25 SKU riêng, 5 thể loại × 5 sách; UTF-8 BOM, đúng số cột | `data/san-pham.csv`; đọc lại bằng csv.DictReader |
| Định danh ấn bản | 25 ISBN checksum hợp lệ; tên/tác giả/năm/trang lấy cùng URL | Bảng nguồn; checksum chỉ bắt lỗi số, không tự chứng minh nguồn đúng |
| Nội dung WordPress | XML parse được; 5 trang và 3 bài viết nháp | `content/noi-dung.xml` |
| Ảnh | 25 PNG 600×900 đọc được; đã xem bảng tổng hợp 25 bìa và banner, không thấy chữ chồng/cắt | `assets/covers/`, `assets/banner-moc-thu.png` |
| Kiểm tra tự động | 196 kiểm tra tĩnh đạt, 0 lỗi | `docs/kiem-tra-tu-dong.json`, chạy `python -X utf8 tools/validate.py` |
| Tương phản màu thiết kế | Chữ/nền 14,09:1; chữ phụ/nền 6,11:1; trắng/nút nâu 8,63:1 | Công thức luminance trong validator; chưa tính mọi trạng thái theme |
| Tổng tiền mẫu | 2×99.000+25.000=223.000; 3×27.000+25.000=106.000 | Phép tính tham chiếu, chưa chạy checkout |

Khi truy cập bằng web tool, một số nguồn Việt Nam bị timeout hoặc tìm kiếm trả kết quả không phù hợp. Truy cập HTTPS trực tiếp có quyền ngoài sandbox đã đọc được NXB Trẻ. Vì vậy đây không phải trường hợp mất toàn bộ internet; dữ liệu NXB đã được đọc online, còn WordPress chưa được cài để kiểm thử.

## Mới kiểm tra cấu trúc/mã

Đã đối chiếu schema CSV với tài liệu WooCommerce chính thức. WXR dùng namespace WordPress export 1.2 và HTML cơ bản, không chứa shortcode UX tự đặt. Nội dung hiển thị dùng escape khi sinh XML/HTML. Mã Python chỉ dựng file offline; không có endpoint, tài khoản tự viết, nonce handler hoặc mã PHP phải cấp quyền trên website.

Đọc một số model/route/config của BookVerse để xác định phạm vi và điểm chưa triển khai; không phải audit bảo mật toàn dự án và không tuyên bố backend cũ chạy đúng.

## Chưa kiểm thử

- Cài/kích hoạt WordPress/WooCommerce và import sản phẩm/WXR thực tế.
- Giao diện desktop/mobile trên website chạy thật; header, footer, UX Builder, child theme.
- Bộ lọc giá/thể loại và tính tương thích widget/block với phiên bản cụ thể.
- Giỏ hàng, checkout COD/BACS, vận chuyển, tài khoản, đơn và biến động tồn kho.
- Phân quyền đơn giữa hai tài khoản, email thử, khôi phục Local.

Lý do: không có bộ cài Flatsome hợp lệ; chưa tìm thấy Local/PHP sẵn trên máy làm việc; Docker CLI có nhưng engine không chạy. Không cài theme khác thay hướng chính thức. **Không có child theme ZIP hoặc plugin ZIP trong lần bàn giao này**: parent chưa xác định thực tế và nghiệp vụ bổ sung chưa cần thiết.

## Quyết định dữ liệu

Giá demo bằng khoảng 90% giá tham khảo, làm tròn xuống nghìn đồng, chỉ để có dải giá thử lọc; không coi đây là giảm giá đang diễn ra và không dùng Sale price. Tồn 10–15 cuốn là giả lập. Không nhập đánh giá. Không nhập nguồn nội bộ vào mô tả khách. Kích thước dùng dấu chấm thập phân trong thuộc tính CSV để tránh dấu phẩy bị tách thành nhiều giá trị; bảng nguồn giữ định dạng gốc.

Ngôn ngữ Tiếng Việt là kết luận đối chiếu từ nội dung giới thiệu của bản Việt và thông tin tác giả/dịch giả, không phải trường ngôn ngữ riêng luôn xuất hiện trên trang NXB. Không chọn bản The Girl Of Yesterday vì phần giới thiệu của ấn bản đó bằng tiếng Anh. Năm 2025/2026 là năm lần in trên nguồn, không khẳng định năm tác phẩm ra đời lần đầu.

## Việc còn lại để đạt toàn bộ đề bài

1. Cài Local/WordPress/WooCommerce trên máy người học; nhập dữ liệu và nội dung, gán ảnh.
2. Có bộ cài/giấy phép Flatsome hợp lệ, xác định Classic hay Site Builder và phiên bản.
3. Tạo/kiểm tra child theme tương ứng nếu cần tùy chỉnh mã; dựng giao diện chính thức.
4. Hoàn tất lựa chọn công cụ lọc miễn phí tương thích và chạy toàn bộ checklist 25 ca.

Gói độc lập đã bàn giao để bắt đầu thực hành; website Flatsome hoàn chỉnh chưa thể được coi là đã nghiệm thu.
