# Công cụ dựng gói — không cài lên WordPress

Người nhập gói đã có CSV/PNG/XML sẵn, không cần chạy Python.

- `build.py`: đọc `../data/books.json`, tạo CSV sản phẩm/nguồn, 25 bìa PNG, logo/banner, WXR 8 mục nháp và bảng đối chiếu. Cần Python 3, Pillow và font Arial có trên Windows. Từ thư mục gói chạy `python -X utf8 tools/build.py`. Lệnh ghi lại các file sinh ra; sao lưu nếu đã sửa tay. Không truy cập mạng.
- `validate.py`: chạy `python -X utf8 tools/validate.py`, kiểm tra nội dung gói và ghi báo cáo. Không truy cập WordPress, không thay thế kiểm thử import/checkout.

Các công cụ thu thập research ở workspace chỉ phục vụ xây dựng ban đầu và không nằm trong ZIP bàn giao. Dữ liệu đầu vào đã được cố định ở `books.json`; không cần tải lại trang NXB để sử dụng gói. Không cài các file Python như plugin/theme. WXR được sinh bằng XML escaping; nội dung HTML không có script, form, iframe hoặc hook PHP. Không có mật khẩu/token/API secret trong công cụ.
