# Dựng giao diện Mộc Thư với Flatsome Classic

**Trạng thái: bản hướng dẫn thiết kế, chưa chạy trên Flatsome thực tế. Không có theme thương mại trong gói.**

## Xác định đúng sản phẩm trước khi cài

Nguồn chính thức ngày 04/11/2026: https://flatsome.com/classic-vs-site-builder và https://flatsome.com/docs . Classic dòng 3 dùng UX Builder và shortcode riêng; Site Builder dòng 4 dùng WordPress blocks. Các bước dưới dành cho **Classic**. Nếu bộ cài là Site Builder/Block Theme, dừng phần hướng dẫn Classic, lập hướng dẫn theo phiên bản đó; không đổi tên thư mục hoặc cố nạp UX shortcode.

Trong Appearance → Themes → Theme Details, ghi tên và Version. Kiểm tra `style.css` của bộ cài cha để xác định tên thư mục/Template chính xác trước khi tạo child theme. Không suy luận phiên bản đang cài từ số phiên bản mới nhất trên website.

## Cài theme cha, child theme và giấy phép

1. Sao lưu site Local. Lấy bộ cài từ tài khoản mua hợp lệ hoặc người có quyền cung cấp theo giấy phép. Không lấy ZIP từ nguồn nulled.
2. Appearance → Themes → Add New → Upload Theme: chọn ZIP theme cài được, không phải ZIP lớn chứa tài liệu và nhiều gói. Install, kiểm tra theme details.
3. Đăng ký qua mục Flatsome Registration/License mà bộ cài thực tế cung cấp, bằng tài khoản/giấy phép hợp lệ. Hướng dẫn Classic: https://docs.uxthemes.com/article/407-theme-license-registration ; quản lý tại https://account.uxthemes.com/ . Không chia sẻ purchase code/token trong ảnh bảo vệ. Nếu đăng ký lỗi, kiểm tra kết nối và điều kiện giấy phép, liên hệ nhà cung cấp; không sửa cơ chế kích hoạt.
4. Nếu gói hợp lệ có child theme mẫu đúng phiên bản, cài ZIP child sau theme cha, rồi kích hoạt child. Theme cha vẫn phải giữ trong máy. Nếu chưa có mẫu, chỉ tạo child sau khi kiểm tra cách theme cha nạp CSS; tránh nạp CSS hai lần. Bộ bàn giao hiện không có child ZIP vì chưa đáp ứng điều kiện này.
5. Toàn bộ CSS/PHP hiển thị tùy chỉnh sau này đặt trong child theme. Không sửa theme cha/WooCommerce. Hiện các thông số thiết kế dưới có thể đặt trong quản trị và UX Builder, chưa cần PHP.

Không nhập demo cửa hàng lớn vì dễ mang theo hình, đánh giá, sản phẩm và plugin ngoài phạm vi. Dựng từ trang trống để tự giải thích được từng phần.

## Hệ thiết kế

| Thành phần | Giá trị đề xuất |
|---|---|
| Nền chính | Kem `#FAF6EE` |
| Nền thẻ/ô nhập | `#FFFFFF` |
| Chữ | Nâu đậm `#2D241E` |
| Nút chính | Nâu `#6B4226`, chữ trắng |
| Chữ phụ | `#675B50` |
| Viền | `#D8CABB` (không dùng làm màu chữ) |
| Font | Arial hoặc system sans-serif có tiếng Việt; 1 họ font |
| Cỡ chữ thân bài | 16–18px, line-height khoảng 1.6 |
| Bề rộng nội dung | Tối đa khoảng 1200px, lề mobile 16–20px |
| Khoảng cách section | Desktop 56–64px, mobile 32–40px |
| Nút/điểm chạm | Tối thiểu 44×44px, focus rõ |

Trong Theme Options/Customizer của bản Classic, đặt màu chính, màu chữ, typography và container. Nếu chỉ có danh sách Google Fonts, chọn font web-safe khi có, hoặc kiểm tra phương án tự host font được phép dùng; không thêm hai họ font chỉ để trang trí. Không chèn animation, gradient, bộ đếm “đã bán” giả hay slider tự chạy. Logo dùng chữ Mộc Thư; nếu header chỉ nhận ảnh, dùng logo PNG tự tạo trong `assets/logo-moc-thu.png`, khai báo alt “Mộc Thư — trang chủ”.

## Header, menu, footer

Header Builder của Classic: logo trái, tìm kiếm sản phẩm ở giữa, tài khoản và giỏ hàng bên phải. Menu desktop có Cửa hàng, 5 thể loại, Góc đọc, Giới thiệu. Mobile: logo, nút menu, giỏ hàng; tìm kiếm trên hàng riêng, tài khoản trong menu. Kiểm tra nút icon có nhãn đọc được và đóng menu bằng bàn phím.

Nguồn Header Builder: https://docs.uxthemes.com/article/191-how-to-use-the-new-header-builder . Các vị trí và tên control cần đối chiếu phiên bản thực tế.

Footer: tạo UX Block “Footer Mộc Thư” nếu bản Classic hỗ trợ và gán vào khu vực footer; hoặc dùng footer widget của theme. Ba cột desktop: tên/tagline; liên kết giao hàng/đổi trả/bảo mật; liên hệ demo. Mobile xếp dọc. Dòng cuối luôn có “Website học tập — không nhận đơn hoặc thanh toán thật”. Không tạo form liên hệ không có nơi nhận; dùng thông tin mẫu được ghi rõ và trang liên hệ.

## Trang chủ — dựng thủ công bằng UX Builder

Pages → Trang chủ → Edit with UX Builder. Dùng Add Elements, chọn phần tử có thật trong phiên bản đang cài. Sau mỗi khu vực: Apply/Update, xem desktop và mobile. Sơ đồ dưới là hướng dẫn thao tác, **không phải file import**.

| Thứ tự | Cấu trúc cần dựng | Nội dung/cấu hình |
|---|---|---|
| 1 | Section → Row → 2 Column → Text, Button, Image | Trái 60%: H1 “Một cuốn sách, một khoảng bình yên.”, đoạn giới thiệu từ `content/trang-chu.md`, nút “Khám phá sách” trỏ Shop thật. Phải 40%: ảnh `banner-moc-thu.png`; mobile xếp dọc. Không đặt chữ quan trọng trong ảnh. |
| 2 | Section → Title + Products | “Sách nổi bật”, chọn 5 SKU có featured trong CSV; 4 cột desktop, 2 mobile; không slider tự chạy. Nếu phần tử không lọc featured, chọn thủ công 5 sách đó. |
| 3 | Section → Title + Products | “Mới lên kệ Mộc Thư”, chọn sắp theo ngày thêm sản phẩm. Đây là mới trên website, không khẳng định sách mới xuất bản. |
| 4 | Section → Title + Row/Text/Button | “Bạn muốn đọc điều gì hôm nay?”, 5 thẻ danh mục trỏ archive thật. Có thể dùng phần tử Product Categories nếu có. |
| 5 | Section → Row → Text | “Một góc đọc vừa đủ”, câu chuyện thương hiệu từ trang giới thiệu, liên kết “Về Mộc Thư”. Nền kem, không ảnh kho giả làm cửa hàng thật. |
| 6 | Section → Title + Blog Posts | “Góc đọc”, 3 bài nguyên bản trong gói; ngày đăng thực tế, tác giả do bạn đặt. |

H1 chỉ một lần ở trang chủ. Các tiêu đề khu vực là H2. Nếu phần tử Products thiếu control cần thiết, chọn sản phẩm bằng UI của nó, không tự đoán tham số UX shortcode. HTML nhập từ WXR là nội dung cơ bản; muốn chỉnh từng section bằng UX Builder phải dựng các phần tử như bảng trên. Không cam kết paste HTML sẽ biến thành layout kéo thả.

## Shop và chi tiết sản phẩm

Giữ template chuẩn WooCommerce/Flatsome. Shop có số kết quả, sắp xếp, phân trang, sidebar thể loại/giá theo `02-woocommerce.md`. Chi tiết: ảnh 2:3 hiển thị đủ bìa, tên, giá, tồn, số lượng, thêm giỏ; mô tả và bảng thuộc tính dưới. Related products lấy từ danh mục/tags; không tự viết thuật toán gợi ý.

Ảnh placeholder phải còn nhãn “BÌA MINH HỌA”; không crop làm mất nhãn. Thử tên sách dài để không đè giá/nút. Đừng biến mọi sản phẩm thành “sale” khi giá chỉ là demo. Chưa có review thật thì ẩn phần xếp hạng hoặc hiển thị đúng trạng thái chưa đánh giá.

## Tự chỉnh và kiểm tra

Đổi banner/chữ: mở UX Builder, chọn đúng Text/Image/Button, sửa rồi Update. Đổi giá/tồn: Products → Edit, không sửa trong banner. Đổi thứ tự thể loại: Appearance → Menus. Đổi footer: sửa UX Block được gán. Đổi màu/font: Theme Options để nhất quán toàn site.

Kiểm tra ở 375, 768, 1440px; phóng chữ 200%, Tab từ header đến footer. Không có cuộn ngang, nút bị che, ảnh vỡ, chữ trên nền thiếu tương phản. Màu đã có kiểm tra toán học trong báo cáo; giao diện thực tế vẫn cần đo lại vì theme có opacity/overlay/hover riêng.
