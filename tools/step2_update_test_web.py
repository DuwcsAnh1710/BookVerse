"""Script tái cấu trúc toàn diện test_local_web.py đáp ứng 100% 5 yêu cầu của người dùng:
1. Taskbar tinh giản, loại bỏ '(25)', bỏ mục trùng lặp, thêm link 'Trang Chủ' về landing page.
2. Dữ liệu sách phong phú (trích dẫn, điểm nổi bật, định dạng, trọng lượng, đối tượng, đánh giá).
3. Toast notification khi thêm giỏ hàng (không tự động mở drawer).
4. Banner Hero dạng Billboard chuẩn điện ảnh (MoMo / Bánh mì Hữu Liêm) với ảnh nền thư viện & đèn chiếu rọi.
5. Ngăn kéo 'Yêu thích' (Wishlist) tương tác thực tế 100%, có nút tim trên từng thẻ sách.
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
output_file = ROOT / 'test_local_web.py'

NEW_TEST_WEB_CODE = '''"""Ứng dụng Web Hiệu Sách Trực Tuyến DuwcsAnhLib
Hotline chính thức: 0933 543 987
Giao diện thương mại điện tử chuyên nghiệp, chuẩn mực 2026.
"""
import http.server
import socketserver
import json
import csv
import webbrowser
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'duwcsanhlib' / 'data'
ASSETS_DIR = ROOT / 'duwcsanhlib' / 'assets'
CONTENT_DIR = ROOT / 'duwcsanhlib' / 'content'

# Dữ liệu bổ sung làm giàu giá trị cho toàn bộ 25 ấn bản NXB Trẻ
BOOK_EXTRAS = {
    'DAL-001': {
        'subtitle': 'Tản văn & Ký ức Hà Nội',
        'quote': 'Hà Nội không chỉ là những địa danh, mà là căn nhà của ký ức, nơi từng viên ngói cũ còn vương hơi thở của nhiều thế hệ.',
        'format': 'Bìa mềm tay gập cao cấp',
        'weight': '320g',
        'highlights': ['Tản văn đậm đà phong vị phố cổ Hà Nội', 'Văn phong hóm hỉnh, sâu lắng từ Trung Sỹ', 'Tặng kèm bookmark DuwcsAnhLib độc quyền'],
        'audience': 'Độc giả yêu mến nét đẹp hoài niệm, văn hóa thủ đô và tản văn đương đại.',
        'reader_review': 'Một cuốn sách tuyệt vời để đọc trong những buổi chiều tĩnh lặng. Trung Sỹ viết rất duyên và thật.'
    },
    'DAL-002': {
        'subtitle': 'Ký sự Biển đảo & Tuổi thơ',
        'quote': 'Gió mặn của Cù Lao Ré ngấm vào da thịt, dạy cho đứa trẻ biển đảo lòng can trường trước sóng dữ.',
        'format': 'Bìa mềm tay gập',
        'weight': '240g',
        'highlights': ['Bức tranh sinh động về con người và cảnh sắc Lý Sơn', 'Tư liệu quý báu về văn hóa biển đảo quê hương', 'Thích hợp cho mọi lứa tuổi gia đình'],
        'audience': 'Bạn đọc quan tâm đến biển đảo Việt Nam, tình yêu quê hương và giáo dục lòng tự hào.',
        'reader_review': 'Vừa là ký ức êm đềm, vừa là tư liệu biển đảo sống động. Đọc rất xúc động.'
    },
    'DAL-003': {
        'subtitle': 'Ký ức Thời bao cấp & Tình người',
        'quote': 'Trong khu tập thể gió lùa ngày ấy, bữa cơm độn bo bo ấm sực tiếng cười vì người ta biết tựa vào nhau.',
        'format': 'Bìa mềm tay gập',
        'weight': '330g',
        'highlights': ['Tái hiện chân thực đời sống thợ cầu Thăng Long thập niên 80', 'Giá trị tình làng nghĩa xóm bền chặt', 'In ấn tiêu chuẩn cao NXB Trẻ'],
        'audience': 'Thế hệ từng trải qua thời bao cấp và người trẻ muốn hiểu về lịch sử đời sống cha ông.',
        'reader_review': 'Đọc từng trang mà ngỡ như sống lại những năm tháng tập thể đầy gian lao nhưng ấm áp.'
    },
    'DAL-004': {
        'subtitle': 'Tùy bút & Góc nhìn toàn cầu',
        'quote': 'Học từ thế giới để làm giàu cho mình, nhưng giữ gìn gốc rễ để không đánh mất bản sắc.',
        'format': 'Bìa mềm tay gập',
        'weight': '220g',
        'highlights': ['Chiêm nghiệm từ chuyên gia đàm phán quốc tế Phan Văn Trường', 'So sánh đối chiếu văn hóa Đông - Tây sắc sảo', 'Ngôn từ gần gũi, truyền cảm hứng mạnh mẽ'],
        'audience': 'Học sinh, sinh viên, người đi làm và những ai khao khát vươn ra biển lớn thế giới.',
        'reader_review': 'Thầy Trường viết cuốn nào cũng thấm thía, bài học giản dị mà triết lý sâu xa.'
    },
    'DAL-005': {
        'subtitle': 'Khảo cứu Văn hóa Sài Gòn xưa',
        'quote': 'Một dấu tích mất đi là một trang sử đô thị khép lại; người ghi chép hôm nay là người giữ lửa cho mai sau.',
        'format': 'Bìa mềm tay gập',
        'weight': '210g',
        'highlights': ['Di cảo khảo cứu quý giá của học giả Vương Hồng Sển', 'Tư liệu lịch sử - kiến trúc Nam Bộ xưa', 'Ấn bản sưu tầm dành cho người mê sách cổ'],
        'audience': 'Nhà nghiên cứu văn hóa, người yêu mến lịch sử Sài Gòn - Gia Định xưa.',
        'reader_review': 'Một tài liệu lịch sử vô giá được NXB Trẻ tái bản trang trọng. Rất đáng có trong tủ sách.'
    },
    'DAL-006': {
        'subtitle': 'Kỹ năng bứt phá & Chiến lược tư duy',
        'quote': 'Thiên tài dựa vào năng khiếu bẩm sinh, còn người bình thường làm chủ thế trận bằng phương pháp và tính kỷ luật sắt.',
        'format': 'Bìa mềm tay gập',
        'weight': '350g',
        'highlights': ['Bí quyết thành công thực chiến từ nhà sản xuất âm nhạc lừng danh Tsunku', 'Chiến lược tối ưu hóa thế mạnh cá nhân', 'Lộ trình rèn luyện tính kiên định hàng ngày'],
        'audience': 'Người trẻ đang tìm kiếm lối đi riêng và muốn phát huy tối đa năng lực bản thân.',
        'reader_review': 'Sách chỉ ra cách tư duy rất thực tế, không lý thuyết sáo rỗng. Đọc xong có thêm động lực lớn.'
    },
    'DAL-007': {
        'subtitle': 'Tâm lý học đường & Trưởng thành',
        'quote': 'Mỗi bông hoa nở vào một mùa riêng; bạn không cần phải là bản sao hoàn hảo của bất kỳ ai.',
        'format': 'Bìa mềm in màu',
        'weight': '200g',
        'highlights': ['Giải mã tâm lý ganh đua và áp lực đồng trang lứa', '9 câu chuyện thực tế gần gũi với lứa tuổi học sinh', 'Cẩm nang hữu ích cho phụ huynh và giáo viên'],
        'audience': 'Học sinh cấp 2, cấp 3, sinh viên và phụ huynh muốn thấu hiểu con cái.',
        'reader_review': 'Mua cho con gái học lớp 8 đọc, bé rất thích và chia sẻ nhiều tâm sự với mẹ hơn.'
    },
    'DAL-008': {
        'subtitle': 'Tâm lý học đường & Kỷ nguyên số',
        'quote': 'Khi bạn sợ bỏ lỡ thế giới trên màn hình, bạn đang bỏ lỡ cuộc sống thực sự ngay trước mắt mình.',
        'format': 'Bìa mềm in màu',
        'weight': '200g',
        'highlights': ['Phân tích hiện tượng FOMO trong thời đại mạng xã hội', 'Bài học thiết lập ranh giới cá nhân lành mạnh', 'Hình vẽ minh họa tươi sáng, sinh động'],
        'audience': 'Thế hệ Gen Z, người dùng mạng xã hội thường xuyên bị áp lực so sánh.',
        'reader_review': 'Rất thời sự! Giúp các bạn trẻ biết cách buông điện thoại xuống và sống cho hiện tại.'
    },
    'DAL-009': {
        'subtitle': 'Vượt qua mặc cảm & Tự tin nội tại',
        'quote': 'Bạn xứng đáng với những gì mình đạt được bằng mồ hôi và trí tuệ, đừng để nỗi sợ dối lừa bạn.',
        'format': 'Bìa mềm in màu',
        'weight': '180g',
        'highlights': ['Nhận diện hội chứng Imposter Syndrome phổ biến ở người trẻ', 'Phương pháp tự đánh giá năng lực khoa học', 'Lời khuyên thực tiễn giúp xây dựng lòng tự trắc ẩn'],
        'audience': 'Những ai hay tự ti, nghi ngờ thành tựu của mình dù đã nỗ lực hết mình.',
        'reader_review': 'Cuốn sách như một cái ôm ấm áp xoa dịu những âu lo và áp lực vô hình.'
    },
    'DAL-010': {
        'subtitle': 'Tâm lý học hành vi & Thay đổi bản thân',
        'quote': 'Tính cách không phải là tảng đá bất biến, mà là mảnh vườn bạn có thể gieo trồng lại mỗi ngày.',
        'format': 'Bìa mềm tay gập',
        'weight': '380g',
        'highlights': ['Kết hợp trải nghiệm cá nhân táo bạo và nghiên cứu khoa học hành vi', 'Cách rèn luyện thói quen và thích ứng linh hoạt', 'Ấn bản quốc tế bán chạy được NXB Trẻ chuyển ngữ'],
        'audience': 'Người muốn phá vỡ các thói quen cũ và phát triển tính cách tích cực hơn.',
        'reader_review': 'Khoa học nhưng viết rất hóm hỉnh, nhiều thí nghiệm tâm lý thú vị và dễ áp dụng.'
    },
    'DAL-011': {
        'subtitle': 'Kinh tế vĩ mô & Chu kỳ thị trường',
        'quote': 'Thị trường không bao giờ nói dối, chỉ có người tham gia từ chối lắng nghe tiếng thì thầm của nó.',
        'format': 'Bìa mềm tay gập',
        'weight': '450g',
        'highlights': ['Phân tích sâu sắc các cuộc khủng hoảng tài chính toàn cầu', 'Bài học quản trị rủi ro danh mục và tâm lý đám đông', 'Đúc kết từ chuyên gia kỳ cựu phố Wall'],
        'audience': 'Nhà đầu tư, sinh viên kinh tế tài chính và nhà quản trị doanh nghiệp.',
        'reader_review': 'Góc nhìn vĩ mô cực kỳ sâu sắc. Đọc để hiểu tại sao chu kỳ kinh tế lại lặp lại.'
    },
    'DAL-012': {
        'subtitle': 'Thiết kế sáng tạo & Nghề quảng cáo',
        'quote': 'Đẹp thôi chưa đủ; thiết kế giỏi là thiết kế nói được điều thương hiệu muốn gửi gắm một cách thông suốt.',
        'format': 'Bìa mềm in màu toàn phần',
        'weight': '390g',
        'highlights': ['Cẩm nang thực chiến từ Giám đốc sáng tạo Phan Trọng Bình (Bưởi)', 'Nhiều ví dụ case study thị giác trực quan', 'Định hướng nghề nghiệp thực tế cho Creative & Designer'],
        'audience': 'Dân thiết kế đồ họa, chuyên viên marketing và sinh viên ngành truyền thông thị giác.',
        'reader_review': 'Cuốn sách gối đầu giường của bất kỳ ai muốn bước chân vào ngành sáng tạo nội dung thị giác.'
    },
    'DAL-013': {
        'subtitle': 'Tiếp thị nhân văn & Trách nhiệm xã hội',
        'quote': 'Tiếp thị chân chính không thao túng điểm yếu, mà thấu hiểu nỗi đau để cùng khách hàng chữa lành.',
        'format': 'Bìa mềm tay gập',
        'weight': '340g',
        'highlights': ['Góc nhìn nhân văn về thương hiệu trong kỷ nguyên hiện đại', 'Cân bằng giữa lợi nhuận và đạo đức kinh doanh', 'Case study từ thị trường Việt Nam thực tế'],
        'audience': 'Brand Manager, CMO, nhà sáng lập startup và người làm truyền thông.',
        'reader_review': 'Một tiếng nói mới mẻ, tỉnh táo giữa cơn sốt tăng trưởng nóng và chiêu trò tiếp thị.'
    },
    'DAL-014': {
        'subtitle': 'Quản trị phòng ngừa & Giải quyết tận gốc',
        'quote': 'Những người hùng thực sự không phải là người cứu hỏa, mà là người đảm bảo đám cháy không bao giờ bùng phát.',
        'format': 'Bìa mềm tay gập',
        'weight': '520g',
        'highlights': ['Tác phẩm best-seller New York Times của tác giả Dan Heath', 'Phương pháp tư duy hệ thống giải quyết vấn đề từ gốc rễ', 'Ứng dụng mạnh mẽ trong kinh doanh, y tế và đời sống'],
        'audience': 'Lãnh đạo doanh nghiệp, quản lý dự án và người muốn rèn luyện tư duy phản biện.',
        'reader_review': 'Tuyệt vời! Cuốn sách làm thay đổi căn bản cách tôi nhìn nhận và xử lý sự cố trong công ty.'
    },
    'DAL-015': {
        'subtitle': 'Kinh tế chính trị & Lịch sử tiến bộ',
        'quote': 'Công nghệ không tự động đem lại thịnh vượng cho tất cả; sự phân bổ quyền lực mới quyết định ai được hưởng lợi.',
        'format': 'Bìa mềm khổ lớn cao cấp',
        'weight': '720g',
        'highlights': ['Tác phẩm của Daron Acemoglu (Giải Nobel Kinh tế 2024)', 'Nghiên cứu đồ sộ về 1000 năm lịch sử công nghệ và quyền lực', 'Công trình kinh tế học đỉnh cao được dịch thuật chuẩn xác'],
        'audience': 'Nhà nghiên cứu chính sách, học giả, doanh nhân và người quan tâm đến tương lai nhân loại.',
        'reader_review': 'Đỉnh cao của tư duy kinh tế học phát triển. Rất dày dặn và tràn đầy tri thức uyên thâm.'
    },
    'DAL-016': {
        'subtitle': 'Triết học ứng dụng & Trị liệu tâm hồn',
        'quote': 'Triết học không hứa hẹn một cuộc đời không đau đớn, nhưng chỉ cho bạn cách đứng thẳng trong cơn bão.',
        'format': 'Bìa mềm tay gập',
        'weight': '310g',
        'highlights': ['Cách các nhà triết học cổ đại vượt qua mất mát và cô đơn', 'Lời văn dung dị, không hàn lâm, dễ tiếp nhận', 'Liều thuốc tinh thần cho những giai đoạn chênh vênh'],
        'audience': 'Bất kỳ ai đang đối diện với khó khăn, khủng hoảng tuổi trung niên hoặc mất phương hướng.',
        'reader_review': 'Đọc cuốn này thấy lòng nhẹ đi rất nhiều. Triết học hóa ra gần gũi và nâng đỡ ta đến vậy.'
    },
    'DAL-017': {
        'subtitle': 'Tư duy logic & Nhận thức sáng suốt',
        'quote': 'Biết được giới hạn nhận thức của mình chính là bước đầu tiên để không bị thế giới dẫn dụ.',
        'format': 'Bìa mềm tay gập',
        'weight': '300g',
        'highlights': ['Tác giả nổi tiếng Nhật Bản Hiroyuki chỉ ra các bẫy tâm lý thường gặp', 'Rèn luyện khả năng hoài nghi lành mạnh', 'Bảo vệ bản thân trước tin giả và thao túng thông tin'],
        'audience': 'Độc giả muốn nâng cao năng lực tư duy logic và kỹ năng ra quyết định.',
        'reader_review': 'Ngắn gọn, súc tích, đập tan nhiều định kiến lâu nay mình vẫn tin sái cổ.'
    },
    'DAL-018': {
        'subtitle': 'Triết lý tối giản & Bình yên nội tại',
        'quote': 'Sự giản dị không phải là thiếu thốn, mà là sự tự do tột cùng khỏi những đòi hỏi rườm rà không cần thiết.',
        'format': 'Bìa mềm phong cách cổ điển',
        'weight': '230g',
        'highlights': ['Tác phẩm kinh điển vượt thời gian của Charles Wagner', 'Thông điệp sâu sắc về lối sống tối giản thanh thản', 'Dịch phẩm tinh tế từ Nhà xuất bản Trẻ'],
        'audience': 'Người yêu thích lối sống tối giản (Minimalism) và tìm kiếm sự tĩnh tại trong tâm hồn.',
        'reader_review': 'Cuốn sách nhỏ nhưng tư tưởng lớn. Đọc chậm từng chương thấy lòng an yên lạ thường.'
    },
    'DAL-019': {
        'subtitle': 'Tâm lý trưởng thành & Khủng hoảng tuổi 30',
        'quote': 'Ba mươi tuổi không phải là đích đến hoàn hảo, mà là lúc bạn bắt đầu học cách yêu thương chính mình một cách trọn vẹn.',
        'format': 'Bìa mềm tay gập',
        'weight': '290g',
        'highlights': ['Đồng cảm sâu sắc với áp lực sự nghiệp, gia đình và hôn nhân', 'Lời khuyên từ chuyên gia tâm lý Park Yeji', 'Thiết kế bìa nhã nhặn, chất giấy ngà ấm áp'],
        'audience': 'Những người ở ngưỡng cửa 25 - 35 tuổi đang tìm kiếm sự cân bằng trong cuộc sống.',
        'reader_review': 'Từng câu từng chữ như nói hộ nỗi lòng của mình ở tuổi ba mươi. Rất đồng cảm.'
    },
    'DAL-020': {
        'subtitle': 'Thấu hiểu lo âu & Giải tỏa áp lực',
        'quote': 'Lo nghĩ là cơ chế tự vệ tự nhiên, nhưng đừng để nỗi sợ trở thành người lái con tàu cuộc đời bạn.',
        'format': 'Bìa mềm tay gập',
        'weight': '410g',
        'highlights': ['Liệu pháp tâm lý từ bác sĩ tâm thần Kim Hye-nam', 'Phân tích các dạng thức lo âu và cách kiểm soát', 'Sách bán hơn 1 triệu bản tại Hàn Quốc'],
        'audience': 'Người thường xuyên bị overthinking, căng thẳng trong công việc và học tập.',
        'reader_review': 'Bác sĩ Kim viết rất ấm áp và khoa học. Đọc xong thấy nhẹ nhõm hơn hẳn.'
    },
    'DAL-021': {
        'subtitle': 'Văn hóa dân gian & Di sản Nam Bộ',
        'quote': 'Lễ hội là nhịp đập tâm hồn của tiền nhân, nơi con cháu tìm về để tri ân đất mẹ phù sa.',
        'format': 'Bìa cứng in màu toàn phần',
        'weight': '190g',
        'highlights': ['Tranh minh họa lễ hội Nam Bộ rực rỡ, chân thực', 'Giáo dục truyền thống văn hóa dân gian cho trẻ em', 'Ấn bản sách tranh khổ vuông đẹp mắt'],
        'audience': 'Các em thiếu nhi từ 6 - 12 tuổi, giáo viên tiểu học và gia đình yêu mến văn hóa cội nguồn.',
        'reader_review': 'Tranh vẽ cực kỳ đẹp và sinh động, đưa bé về với các lễ hội miền Tây Nam Bộ.'
    },
    'DAL-022': {
        'subtitle': 'Thiên nhiên & Đời sống sông nước',
        'quote': 'Tiếng sóng nước Cửu Long chở theo bao câu hát nghĩa tình của cư dân miệt vườn qua hàng trăm năm.',
        'format': 'Bìa cứng in màu toàn phần',
        'weight': '180g',
        'highlights': ['Khám phá lễ hội sông nước Vĩnh Long, Cần Thơ, Cà Mau', 'Ngôn ngữ kể chuyện mộc mạc, giàu cảm xúc', 'Bồi dưỡng tình yêu thiên nhiên và biển cả'],
        'audience': 'Thiếu nhi, phụ huynh đọc cùng con và người yêu mến cảnh sắc phương Nam.',
        'reader_review': 'Một bộ sách tranh rất nhân văn và bổ ích của NXB Trẻ dành cho các em nhỏ.'
    },
    'DAL-023': {
        'subtitle': 'Bài học nhân cách & Lòng nhân ái',
        'quote': 'Tình yêu thương cho đi không bao giờ mất đi; nó luôn quay trở lại làm ấm áp tâm hồn người trao tặng.',
        'format': 'Bìa mềm in màu',
        'weight': '160g',
        'highlights': ['Tác phẩm thuộc bộ 500 Câu Chuyện Đạo Đức tái bản lần thứ 7', 'Những mẩu chuyện ngắn gọn, sâu sắc và dễ nhớ', 'Công cụ tuyệt vời cho giờ đọc sách gia đình'],
        'audience': 'Trẻ em lứa tuổi tiểu học và các bậc cha mẹ muốn rèn luyện nhân cách cho con.',
        'reader_review': 'Sách kinh điển nhiều năm nay của NXB Trẻ, rất đáng để mua trọn bộ cho con đọc.'
    },
    'DAL-024': {
        'subtitle': 'Bách khoa tri thức thiếu nhi & Hội họa',
        'quote': 'Hội họa là ngôn ngữ của trái tim, nơi mỗi nét vẽ là một giấc mơ đầy màu sắc của bé.',
        'format': 'Khổ lớn 19x26cm in màu sắc nét',
        'weight': '140g',
        'highlights': ['Hỏi đáp khoa học trực quan kích thích tư duy nghệ thuật', 'Minh họa bắt mắt từ họa sĩ Nguyên Khôi', 'Khổ sách lớn dễ lật giở và học tập'],
        'audience': 'Trẻ em tò mò về thế giới nghệ thuật, vẽ tranh và bảo tàng.',
        'reader_review': 'Hình vẽ đẹp, câu hỏi gần gũi, giúp bé hào hứng tìm hiểu về tranh ảnh và màu sắc.'
    },
    'DAL-025': {
        'subtitle': 'Khám phá thế giới & Khoa học tự nhiên',
        'quote': 'Mỗi câu hỏi của bé là một cánh cửa mở ra vũ trụ bao la đầy kỳ thú.',
        'format': 'Khổ lớn 19x26cm in màu sắc nét',
        'weight': '140g',
        'highlights': ['Giải đáp các hiện tượng tự nhiên quanh bé một cách khoa học', 'Hình ảnh trực quan sinh động, khơi gợi trí tò mò', 'Sách giáo dục khoa học chuẩn NXB Trẻ'],
        'audience': 'Trẻ em ham học hỏi, yêu thích khoa học tự nhiên và khám phá vũ trụ.',
        'reader_review': 'Bé nhà mình đọc say sưa, liên tục đặt thêm những câu hỏi thú vị về Trái Đất.'
    }
}

# Đọc danh sách sản phẩm từ CSV
csv_path = DATA_DIR / 'san-pham-duwcsanhlib.csv'
products = []
with csv_path.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sku = row['SKU']
        reg = int(row.get('Regular price', 0) or 0)
        sale = int(row.get('Sale price', 0) or 0)
        discount = 0
        if reg > 0 and sale > 0 and sale < reg:
            discount = round((reg - sale) / reg * 100)
        row['discount_pct'] = discount
        row['rating'] = 5.0
        row['reviews_count'] = 18 + (int(sku.split('-')[-1]) * 7) % 43
        row['sold_count'] = 45 + (int(sku.split('-')[-1]) * 13) % 95
        
        # Bổ sung dữ liệu giàu giá trị
        extra = BOOK_EXTRAS.get(sku, {})
        row['subtitle'] = extra.get('subtitle', row.get('Short description', ''))
        row['quote'] = extra.get('quote', 'Tri thức là ngọn lửa khai phóng tương lai.')
        row['format'] = extra.get('format', 'Bìa mềm tay gập chuẩn NXB Trẻ')
        row['weight'] = extra.get('weight', '300g')
        row['highlights'] = extra.get('highlights', [
            '100% Ấn bản chính thống từ NXB Trẻ',
            'Giấy xốp bãi bằng bảo vệ thị lực, chống lóa',
            'Tặng kèm bookmark DuwcsAnhLib độc quyền'
        ])
        row['audience'] = extra.get('audience', 'Độc giả yêu sách và tìm kiếm tri thức chuẩn mực.')
        row['reader_review'] = extra.get('reader_review', 'Ấn bản rất đẹp, đóng gói cẩn thận và giao nhanh.')
        products.append(row)

# Load content pages
pages_data = {}
for p in ['gioi-thieu', 'lien-he', 'giao-hang', 'doi-tra', 'bao-mat', 'blog-01', 'blog-02', 'blog-03']:
    p_path = CONTENT_DIR / f"{p}.md"
    if p_path.exists():
        pages_data[p] = p_path.read_text(encoding='utf-8')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DuwcsAnhLib — Cửa Hàng Sách & Thư Viện Tri Thức</title>
  <!-- Brand Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Material Symbols -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');
    body { font-family: 'Nunito Sans', sans-serif; background-color: #F8F9FA; color: #1C1C1E; }
    .serif-title { font-family: 'Playfair Display', serif; }
    .brand-red { color: #C92127; }
    .bg-brand-red { background-color: #C92127; }
    .bg-brand-red-hover:hover { background-color: #A5181D; }
    .border-brand-red { border-color: #C92127; }
    .text-brand-red { color: #C92127; }
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
      vertical-align: middle;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .material-symbols-outlined.fill-icon {
      font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    
    /* Billboard Scrim Gradient */
    .billboard-hero {
      background: linear-gradient(90deg, rgba(15, 2, 4, 0.96) 0%, rgba(35, 6, 10, 0.90) 45%, rgba(20, 3, 5, 0.35) 75%, rgba(15, 2, 4, 0.82) 100%),
                  url('/assets/hero-bookstore-bg.jpg') center/cover no-repeat;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- TOP BAR -->
  <div class="bg-[#F8F9FA] border-b border-gray-200 text-xs text-gray-600 py-1.5 px-4">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
      <div class="flex items-center gap-4 text-[11px] sm:text-xs">
        <span class="flex items-center gap-1.5 font-medium text-gray-800">
          <span class="material-symbols-outlined text-sm text-brand-red">call</span>
          Hotline: <strong class="text-brand-red font-extrabold tracking-wide">0933.543.987</strong>
        </span>
        <span class="hidden md:inline-block text-gray-300">|</span>
        <span class="hidden md:flex items-center gap-1.5 text-emerald-700 font-medium">
          <span class="material-symbols-outlined text-sm text-emerald-600">local_shipping</span>
          Miễn phí vận chuyển toàn quốc cho đơn từ 250.000 đ
        </span>
      </div>
      <div class="flex items-center gap-4 text-[11px] sm:text-xs">
        <button onclick="showView('content', 'giao-hang')" class="hover:text-brand-red transition">Chính sách giao hàng</button>
        <span class="text-gray-300">|</span>
        <button onclick="showView('content', 'doi-tra')" class="hover:text-brand-red transition">Chính sách đổi trả</button>
        <span class="text-gray-300">|</span>
        <button onclick="showView('content', 'lien-he')" class="hover:text-brand-red transition font-semibold text-gray-700">Liên hệ hỗ trợ</button>
      </div>
    </div>
  </div>

  <!-- MAIN HEADER -->
  <header class="bg-white sticky top-0 z-40 border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer shrink-0" onclick="showView('home')">
        <img src="/assets/logo-header-symbol.png" alt="DuwcsAnhLib" class="h-12 w-auto object-contain hover:scale-105 transition-transform">
        <div>
          <span class="text-2xl font-black tracking-wider text-brand-red uppercase leading-none block">DuwcsAnh<span class="text-amber-600">Lib</span></span>
          <span class="text-[10px] text-gray-500 font-bold tracking-widest uppercase block mt-0.5">Hiệu Sách & Thư Viện Tri Thức</span>
        </div>
      </div>

      <!-- Smart Search Box -->
      <div class="flex-1 max-w-2xl mx-2 hidden sm:block">
        <div class="relative flex items-center rounded-lg border-2 border-brand-red overflow-hidden shadow-inner bg-white">
          <select id="headerCategorySelect" onchange="handleHeaderCategory()" class="bg-gray-50 text-xs font-semibold text-gray-700 px-3 py-2.5 border-r border-gray-200 outline-none cursor-pointer">
            <option value="All">Tất cả danh mục</option>
            <option value="Văn học">Văn học</option>
            <option value="Kinh tế">Kinh tế & Kinh doanh</option>
            <option value="Tâm lý">Tâm lý & Đời sống</option>
            <option value="Kỹ năng">Kỹ năng phát triển</option>
            <option value="Thiếu nhi">Sách Thiếu nhi</option>
          </select>
          <input type="text" id="headerSearchInput" oninput="handleSearch()" placeholder="Tìm kiếm tựa sách, tác giả, ISBN, Nhà xuất bản..." class="w-full px-3 py-2 text-xs text-gray-800 placeholder-gray-400 focus:outline-none">
          <button onclick="handleSearch()" class="bg-brand-red hover:bg-red-700 text-white px-5 py-2.5 flex items-center justify-center transition cursor-pointer">
            <span class="material-symbols-outlined text-lg">search</span>
          </button>
        </div>
      </div>

      <!-- User Actions: Wishlist & Mini Cart -->
      <div class="flex items-center gap-3 shrink-0">
        <!-- Wishlist Button -->
        <button id="headerWishlistBtn" onclick="openWishlist()" class="p-2 rounded-lg hover:bg-gray-100 text-gray-700 relative hidden md:flex items-center gap-1.5 text-xs font-semibold cursor-pointer transition">
          <span class="material-symbols-outlined text-red-600 fill-icon">favorite</span>
          <span>Yêu thích</span>
          <span id="wishlistCountBadge" class="w-4 h-4 rounded-full bg-brand-red text-white text-[10px] flex items-center justify-center font-bold">3</span>
        </button>

        <!-- Cart Button -->
        <button id="headerCartBtn" onclick="openCart()" class="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-red-50 hover:bg-red-100 border border-red-200 transition text-brand-red cursor-pointer shadow-sm">
          <div class="relative">
            <span class="material-symbols-outlined text-2xl text-brand-red">shopping_cart</span>
            <span id="cartCountBadge" class="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-brand-red text-white text-xs font-black flex items-center justify-center border-2 border-white shadow">0</span>
          </div>
          <div class="text-left hidden sm:block">
            <div class="text-[10px] uppercase font-bold text-gray-500 leading-tight">Giỏ hàng</div>
            <div id="headerCartTotal" class="text-xs font-extrabold text-brand-red leading-tight">0 đ</div>
          </div>
        </button>
      </div>
    </div>

    <!-- SUB NAVIGATION (TASKBAR CHUẨN MỰC, KHÔNG TRÙNG LẶP, CÓ TRANG CHỦ) -->
    <div class="bg-brand-red text-white text-xs font-bold uppercase tracking-wider">
      <div class="max-w-7xl mx-auto px-4 flex items-center justify-between">
        <div class="flex items-center">
          
          <!-- Category Mega Menu Toggle -->
          <div class="relative group">
            <button class="bg-[#A5181D] hover:bg-black/30 py-3 px-4 flex items-center gap-2 cursor-pointer transition">
              <span class="material-symbols-outlined text-lg">menu</span>
              <span>DANH MỤC SẢN PHẨM</span>
              <span class="material-symbols-outlined text-sm opacity-80">expand_more</span>
            </button>
            
            <!-- Dropdown Menu -->
            <div class="absolute left-0 top-full w-64 bg-white text-gray-800 shadow-xl border border-gray-200 rounded-b-xl py-2 hidden group-hover:block z-50">
              <div onclick="filterCatAndShow('Văn học')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-brand-red">auto_stories</span>
                  Văn học & Tản văn
                </span>
                <span class="text-[10px] bg-red-100 text-brand-red px-1.5 py-0.5 rounded font-mono">5</span>
              </div>
              <div onclick="filterCatAndShow('Kinh tế')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-emerald-600">trending_up</span>
                  Kinh tế & Kinh doanh
                </span>
                <span class="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-mono">5</span>
              </div>
              <div onclick="filterCatAndShow('Tâm lý')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-purple-600">psychology</span>
                  Tâm lý & Đời sống
                </span>
                <span class="text-[10px] bg-purple-100 text-purple-800 px-1.5 py-0.5 rounded font-mono">5</span>
              </div>
              <div onclick="filterCatAndShow('Kỹ năng')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-orange-600">lightbulb</span>
                  Kỹ năng phát triển
                </span>
                <span class="text-[10px] bg-orange-100 text-orange-800 px-1.5 py-0.5 rounded font-mono">5</span>
              </div>
              <div onclick="filterCatAndShow('Thiếu nhi')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-blue-600">child_care</span>
                  Sách Thiếu nhi
                </span>
                <span class="text-[10px] bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded font-mono">5</span>
              </div>
            </div>
          </div>

          <!-- Horizontal Nav Links -->
          <div class="hidden lg:flex items-center">
            <a href="/" class="py-3 px-4 hover:bg-black/20 text-white font-bold transition flex items-center gap-1.5">
              <span class="material-symbols-outlined text-base">home</span>
              <span>Trang Chủ</span>
            </a>
            <button onclick="showView('shop')" class="py-3 px-4 hover:bg-black/20 text-white font-bold transition flex items-center gap-1">
              <span>Cửa Hàng</span>
            </button>
            <button onclick="scrollToSection('flashsale-section')" class="py-3 px-4 hover:bg-black/20 text-yellow-300 transition flex items-center gap-1">
              <span class="material-symbols-outlined text-sm text-yellow-300">bolt</span>
              <span>Flash Sale</span>
            </button>
            <button onclick="showView('shop'); filterCatAndShow('Văn học');" class="py-3 px-4 hover:bg-black/20 transition">
              <span>Sách Bán Chạy</span>
            </button>
            <button onclick="showView('blogs')" class="py-3 px-4 hover:bg-black/20 transition">
              <span>Góc Đọc & Review</span>
            </button>
            <button onclick="showView('content', 'gioi-thieu')" class="py-3 px-4 hover:bg-black/20 transition">
              <span>Về DuwcsAnhLib</span>
            </button>
          </div>
        </div>

        <div class="hidden xl:flex items-center text-[11px] text-amber-200 gap-1.5 font-bold">
          <span class="material-symbols-outlined text-sm">verified</span>
          <span>100% Ấn Bản Chính Thức NXB Trẻ</span>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 py-5 space-y-8">

    <!-- VIEW: HOME PAGE -->
    <div id="view-home" class="space-y-8">
      
      <!-- HERO SHOWCASE: 2/3 BILLBOARD BANNER + 1/3 DUAL BANNERS -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        
        <!-- 2/3 Main Billboard Banner (Thiết kế chuẩn điện ảnh theo hình mẫu MoMo / Bánh mì Hữu Liêm) -->
        <div class="lg:col-span-2 relative rounded-2xl overflow-hidden shadow-2xl flex flex-col justify-between min-h-[340px] billboard-hero border border-stone-800">
          
          <!-- Billboard Top Spotlight Lighting Bar -->
          <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 shadow-[0_0_16px_rgba(251,191,36,0.8)]"></div>
          
          <!-- Subtle Glow Spots from lamps -->
          <div class="absolute top-0 left-12 w-28 h-14 bg-amber-300/25 blur-xl pointer-events-none"></div>
          <div class="absolute top-0 left-1/3 w-32 h-14 bg-yellow-200/25 blur-xl pointer-events-none"></div>
          <div class="absolute top-0 right-1/4 w-36 h-16 bg-amber-400/30 blur-xl pointer-events-none"></div>

          <!-- Billboard Typography & CTA on Left Scrim -->
          <div class="p-8 sm:p-11 max-w-lg space-y-3.5 relative z-10 text-white">
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-gradient-to-r from-amber-400 to-yellow-500 text-stone-950 font-black text-[11px] rounded-full uppercase tracking-wider shadow">
              <span class="material-symbols-outlined text-sm">local_fire_department</span>
              <span>ƯU ĐÃI ĐỘC QUYỀN DUWCSANHLIB</span>
            </div>
            
            <h1 class="text-2xl sm:text-4xl font-extrabold serif-title leading-tight drop-shadow-md">
              Hội Sách Tri Thức 2026:<br>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-300 to-amber-400">
                Giảm Đến 30% Tất Cả Ấn Bản
              </span>
            </h1>
            
            <p class="text-stone-200 text-xs sm:text-sm leading-relaxed max-w-md drop-shadow">
              Tuyển tập 25 tác phẩm văn học, kinh tế, tâm lý & kỹ năng kinh điển từ Nhà xuất bản Trẻ. Đóng gói hộp carton 3 lớp bảo vệ gáy sách, giao nhanh toàn quốc.
            </p>
            
            <div class="pt-2 flex flex-wrap items-center gap-3">
              <button onclick="showView('shop')" class="px-6 py-3 bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-yellow-300 hover:to-amber-400 text-stone-950 font-black rounded-xl text-xs uppercase tracking-wider shadow-lg hover:shadow-xl transition transform hover:-translate-y-0.5 flex items-center gap-2 cursor-pointer">
                <span class="material-symbols-outlined text-base">auto_stories</span>
                <span>Khám Phá Toàn Bộ Sách</span>
              </button>
              <button onclick="scrollToSection('flashsale-section')" class="px-5 py-3 bg-white/15 hover:bg-white/25 text-white font-bold rounded-xl text-xs border border-white/25 backdrop-blur-sm transition cursor-pointer flex items-center gap-1.5">
                <span class="material-symbols-outlined text-sm text-yellow-300">bolt</span>
                <span>Xem Flash Sale</span>
              </button>
            </div>
          </div>

          <!-- Bottom Billboard Accreditation Bar -->
          <div class="px-8 py-3 bg-black/60 backdrop-blur-md border-t border-white/10 flex flex-wrap items-center justify-between text-[11px] text-stone-300 gap-2 relative z-10">
            <span class="flex items-center gap-1.5 font-semibold text-amber-200">
              <span class="material-symbols-outlined text-sm">verified</span>
              100% Ấn bản chuẩn hóa từ NXB Trẻ
            </span>
            <span class="flex items-center gap-1.5 font-semibold">
              <span class="material-symbols-outlined text-sm text-amber-400">package_2</span>
              Đóng hộp carton 3 lớp bảo vệ gáy sách
            </span>
            <span class="flex items-center gap-1.5 font-semibold text-emerald-300">
              <span class="material-symbols-outlined text-sm">local_shipping</span>
              Freeship đơn từ 250k
            </span>
          </div>
        </div>

        <!-- 1/3 Side Dual Banners -->
        <div class="flex flex-col gap-4">
          <div onclick="filterCatAndShow('Kinh tế')" class="flex-1 rounded-2xl bg-gradient-to-br from-emerald-900 to-teal-950 text-white p-6 shadow-md flex flex-col justify-between cursor-pointer hover:shadow-lg transition group border border-emerald-800/40">
            <div>
              <span class="text-[10px] font-black uppercase tracking-wider bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">Tủ Sách Khởi Nghiệp</span>
              <h3 class="text-base sm:text-lg font-bold mt-2 group-hover:text-emerald-300 transition leading-snug">Kinh Tế & Lãnh Đạo 4.0</h3>
              <p class="text-xs text-emerald-200/80 mt-1">Đúc kết bài học thực chiến từ các chuyên gia hàng đầu.</p>
            </div>
            <div class="text-xs font-bold text-emerald-400 flex items-center gap-1 mt-4 group-hover:translate-x-1 transition-transform">
              <span>Xem tuyển tập</span>
              <span class="material-symbols-outlined text-xs">arrow_forward</span>
            </div>
          </div>

          <div onclick="filterCatAndShow('Tâm lý')" class="flex-1 rounded-2xl bg-gradient-to-br from-purple-900 to-indigo-950 text-white p-6 shadow-md flex flex-col justify-between cursor-pointer hover:shadow-lg transition group border border-purple-800/40">
            <div>
              <span class="text-[10px] font-black uppercase tracking-wider bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded">Sách Nuôi Dưỡng Tâm Hồn</span>
              <h3 class="text-base sm:text-lg font-bold mt-2 group-hover:text-purple-300 transition leading-snug">Tâm Lý & Đời Sống</h3>
              <p class="text-xs text-purple-200/80 mt-1">Khoảng lặng cần thiết giữa nhịp sống bận rộn.</p>
            </div>
            <div class="text-xs font-bold text-purple-400 flex items-center gap-1 mt-4 group-hover:translate-x-1 transition-transform">
              <span>Khám phá ngay</span>
              <span class="material-symbols-outlined text-xs">arrow_forward</span>
            </div>
          </div>
        </div>

      </div>

      <!-- SECTION 2: 4 SERVICE GUARANTEES -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
        <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center gap-3 shadow-sm hover:border-brand-red transition">
          <div class="w-10 h-10 rounded-lg bg-red-50 text-brand-red flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-2xl">verified</span>
          </div>
          <div>
            <div class="font-extrabold text-gray-900">100% Sách Thật</div>
            <div class="text-[11px] text-gray-500">Chính hãng Nhà xuất bản Trẻ</div>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center gap-3 shadow-sm hover:border-brand-red transition">
          <div class="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-2xl">package_2</span>
          </div>
          <div>
            <div class="font-extrabold text-gray-900">Đóng Gói Chống Móp</div>
            <div class="text-[11px] text-gray-500">Màng co + Hộp carton 3 lớp</div>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center gap-3 shadow-sm hover:border-brand-red transition">
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-2xl">local_shipping</span>
          </div>
          <div>
            <div class="font-extrabold text-gray-900">Freeship Từ 250k</div>
            <div class="text-[11px] text-gray-500">Giao hàng nhanh toàn quốc</div>
          </div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center gap-3 shadow-sm hover:border-brand-red transition">
          <div class="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-2xl">published_with_changes</span>
          </div>
          <div>
            <div class="font-extrabold text-gray-900">Đổi Trả 7 Ngày</div>
            <div class="text-[11px] text-gray-500">Nếu lỗi in ấn hoặc cấn móp</div>
          </div>
        </div>
      </div>

      <!-- SECTION 3: FLASH SALE SECTION -->
      <section id="flashsale-section" class="bg-white rounded-2xl border border-red-200 shadow-sm p-5 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-100 pb-3 gap-3">
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-1.5 text-brand-red font-black text-lg uppercase tracking-wide">
              <span class="material-symbols-outlined text-2xl text-amber-500">bolt</span>
              <span>GIỜ VÀNG SÁCH HAY — FLASH SALE</span>
            </div>
            <div class="flex items-center gap-1 text-xs font-bold bg-stone-900 text-white px-3 py-1 rounded-full shadow">
              <span class="text-[10px] text-stone-400 uppercase tracking-widest mr-1">Kết thúc sau:</span>
              <span id="timerHours" class="bg-red-600 px-1.5 py-0.5 rounded">02</span> :
              <span id="timerMinutes" class="bg-red-600 px-1.5 py-0.5 rounded">45</span> :
              <span id="timerSeconds" class="bg-red-600 px-1.5 py-0.5 rounded">18</span>
            </div>
          </div>
          
          <button onclick="showView('shop')" class="text-xs font-bold text-brand-red hover:underline flex items-center gap-0.5">
            <span>Xem tất cả ưu đãi</span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </button>
        </div>

        <div id="flashSaleGrid" class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <!-- Populated by JS -->
        </div>
      </section>

      <!-- 5 CATEGORIES QUICK TABS -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-6 bg-brand-red rounded-full"></span>
            <h2 class="text-xl font-black text-gray-900 uppercase">Khám Phá Theo Thể Loại</h2>
          </div>
          <button onclick="showView('shop')" class="text-xs font-bold text-brand-red hover:underline flex items-center gap-0.5">
            <span>Xem toàn bộ tủ sách</span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </button>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <div onclick="filterCatAndShow('Văn học')" class="bg-white p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-md transition cursor-pointer text-center group">
            <div class="w-12 h-12 rounded-xl bg-red-50 text-brand-red mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
              <span class="material-symbols-outlined text-2xl">auto_stories</span>
            </div>
            <div class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition">Văn Học & Tản Văn</div>
            <div class="text-[11px] text-gray-500 mt-0.5">5 ấn bản</div>
          </div>
          <div onclick="filterCatAndShow('Kinh tế')" class="bg-white p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-md transition cursor-pointer text-center group">
            <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
              <span class="material-symbols-outlined text-2xl">trending_up</span>
            </div>
            <div class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition">Kinh Tế & Quản Trị</div>
            <div class="text-[11px] text-gray-500 mt-0.5">5 ấn bản</div>
          </div>
          <div onclick="filterCatAndShow('Tâm lý')" class="bg-white p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-md transition cursor-pointer text-center group">
            <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
              <span class="material-symbols-outlined text-2xl">psychology</span>
            </div>
            <div class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition">Tâm Lý & Đời Sống</div>
            <div class="text-[11px] text-gray-500 mt-0.5">5 ấn bản</div>
          </div>
          <div onclick="filterCatAndShow('Kỹ năng')" class="bg-white p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-md transition cursor-pointer text-center group">
            <div class="w-12 h-12 rounded-xl bg-orange-50 text-orange-600 mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
              <span class="material-symbols-outlined text-2xl">lightbulb</span>
            </div>
            <div class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition">Kỹ Năng Sống</div>
            <div class="text-[11px] text-gray-500 mt-0.5">5 ấn bản</div>
          </div>
          <div onclick="filterCatAndShow('Thiếu nhi')" class="bg-white p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-md transition cursor-pointer text-center group">
            <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
              <span class="material-symbols-outlined text-2xl">child_care</span>
            </div>
            <div class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition">Sách Thiếu Nhi</div>
            <div class="text-[11px] text-gray-500 mt-0.5">5 ấn bản</div>
          </div>
        </div>
      </div>

      <!-- PRODUCT TABS SHOWCASE -->
      <section class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-200 pb-3 gap-3">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-6 bg-brand-red rounded-full"></span>
            <h2 class="text-xl font-black text-gray-900 uppercase">Sách Tuyển Chọn Nổi Bật</h2>
          </div>
          
          <div class="flex items-center gap-2 overflow-x-auto no-scrollbar text-xs font-bold">
            <button onclick="switchTabContent('bestseller')" id="tab-btn-bestseller" class="px-3.5 py-1.5 rounded-full bg-brand-red text-white transition">Bán Chạy Nhất</button>
            <button onclick="switchTabContent('new')" id="tab-btn-new" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition">Mới Phát Hành</button>
            <button onclick="switchTabContent('vanhoc')" id="tab-btn-vanhoc" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition">Văn Học Hay</button>
            <button onclick="switchTabContent('kinhte')" id="tab-btn-kinhte" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition">Kinh Doanh</button>
          </div>
        </div>

        <div id="tabProductsGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <!-- Populated by JS -->
        </div>
      </section>

      <!-- SECTION 5: BRAND TRUST STORY & PACKAGING -->
      <section class="bg-[#FFFBEB] rounded-2xl border border-amber-200 p-6 sm:p-10 shadow-sm">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div class="space-y-4">
            <span class="text-xs font-black uppercase tracking-wider text-amber-800 bg-amber-100 px-3 py-1 rounded-full">
              CAM KẾT TỪ DUWCSANHLIB
            </span>
            <h2 class="text-2xl sm:text-3xl font-extrabold serif-title text-amber-950 leading-tight">
              Mỗi Cuốn Sách Đến Tay Bạn Đều Trọn Vẹn Như Mới Rời Nhà In
            </h2>
            <p class="text-xs sm:text-sm text-amber-900 leading-relaxed">
              Chúng tôi hiểu rằng với người yêu sách, một nếp gấp gáy hay góc bìa cấn móp cũng làm giảm đi niềm vui đọc. Vì vậy, DuwcsAnhLib áp dụng quy chuẩn đóng gói 3 lớp bảo vệ chuyên biệt:
            </p>
            <div class="space-y-2 text-xs text-amber-900">
              <div class="flex items-start gap-2">
                <span class="material-symbols-outlined text-amber-700 text-sm mt-0.5">check_circle</span>
                <span><strong>Lớp 1:</strong> Màng co chống ẩm và bảo vệ bề mặt bìa sách.</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="material-symbols-outlined text-amber-700 text-sm mt-0.5">check_circle</span>
                <span><strong>Lớp 2:</strong> Bọc xốp bóng khí (bubble wrap) 2-3 lớp bo tròn 4 góc mép.</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="material-symbols-outlined text-amber-700 text-sm mt-0.5">check_circle</span>
                <span><strong>Lớp 3:</strong> Đóng hộp carton 3 lớp cứng cáp dán băng keo niêm phong thương hiệu.</span>
              </div>
            </div>
            <div class="pt-2">
              <button onclick="showView('content', 'gioi-thieu')" class="px-5 py-2.5 bg-amber-800 hover:bg-amber-900 text-white font-bold rounded-lg text-xs transition cursor-pointer">
                Tìm Hiểu Thêm Về DuwcsAnhLib
              </button>
            </div>
          </div>
          <div class="bg-gradient-to-br from-amber-900 to-red-950 text-white rounded-2xl p-8 flex flex-col justify-center items-center text-center shadow-inner relative overflow-hidden">
            <div class="w-16 h-16 rounded-2xl bg-amber-500/20 text-amber-300 flex items-center justify-center mb-4">
              <span class="material-symbols-outlined text-4xl">verified_user</span>
            </div>
            <h3 class="text-xl font-bold serif-title text-amber-200 mb-2">100% Sách Thật</h3>
            <p class="text-xs text-amber-100 max-w-sm leading-relaxed mb-4">
              "Không kinh doanh sách lậu, sách sao chép trái phép. Tôn trọng bản quyền tác giả là tôn trọng tri thức."
            </p>
            <span class="text-[11px] font-black uppercase tracking-widest text-white/80 border-t border-amber-500/30 pt-3 w-full">
              — Ban Biên Tập DuwcsAnhLib —
            </span>
          </div>
        </div>
      </section>

      <!-- SECTION 6: FEATURED AUTHORS -->
      <section class="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div class="text-center max-w-2xl mx-auto space-y-2">
          <div class="flex items-center justify-center gap-2">
            <span class="w-1.5 h-6 bg-brand-red rounded-full"></span>
            <h2 class="text-xl font-black text-gray-900 uppercase">Gặp Gỡ Các Tác Giả Tiêu Biểu</h2>
          </div>
          <p class="text-xs text-gray-500">Những cây bút tài hoa đồng hành cùng các ấn phẩm tinh tuyển từ Nhà xuất bản Trẻ</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-xl border border-gray-100 bg-gray-50/60 hover:bg-white hover:border-brand-red hover:shadow-md transition text-center space-y-2">
            <div class="w-14 h-14 rounded-full bg-red-100 text-brand-red mx-auto flex items-center justify-center font-bold text-xl">
              <span class="material-symbols-outlined text-2xl">history_edu</span>
            </div>
            <h4 class="font-extrabold text-sm text-gray-900">Học Giả Vương Hồng Sển</h4>
            <p class="text-xs text-gray-500 leading-relaxed">Tác giả tác phẩm <em>"Khám Lớn Sài Gòn"</em> — Nhà văn hóa uyên bác với những trang khảo cứu Nam Bộ sâu sắc.</p>
          </div>
          <div class="p-5 rounded-xl border border-gray-100 bg-gray-50/60 hover:bg-white hover:border-brand-red hover:shadow-md transition text-center space-y-2">
            <div class="w-14 h-14 rounded-full bg-amber-100 text-amber-700 mx-auto flex items-center justify-center font-bold text-xl">
              <span class="material-symbols-outlined text-2xl">record_voice_over</span>
            </div>
            <h4 class="font-extrabold text-sm text-gray-900">GS. Phan Văn Trường</h4>
            <p class="text-xs text-gray-500 leading-relaxed">Tác giả <em>"Chuyện Ta Truyện Tây"</em> — Chuyên gia đàm phán quốc tế, người truyền cảm hứng cho nhiều thế hệ độc giả.</p>
          </div>
          <div class="p-5 rounded-xl border border-gray-100 bg-gray-50/60 hover:bg-white hover:border-brand-red hover:shadow-md transition text-center space-y-2">
            <div class="w-14 h-14 rounded-full bg-blue-100 text-blue-700 mx-auto flex items-center justify-center font-bold text-xl">
              <span class="material-symbols-outlined text-2xl">ink_pen</span>
            </div>
            <h4 class="font-extrabold text-sm text-gray-900">Nhà Văn Trung Sỹ</h4>
            <p class="text-xs text-gray-500 leading-relaxed">Tác giả <em>"Nhà Cũ Trong Phố Cũ"</em> — Ký ức Hà Nội đằm thắm qua từng góc phố quen và phận người bình dị.</p>
          </div>
        </div>
      </section>

      <!-- SECTION 7: TESTIMONIALS & REVIEWS -->
      <section class="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div class="text-center max-w-xl mx-auto space-y-1">
          <span class="text-[10px] font-black uppercase tracking-wider text-brand-red bg-red-50 px-2.5 py-1 rounded-full">
            ĐỘC GIẢ NÓI GÌ VỀ DUWCSANHLIB?
          </span>
          <h2 class="text-xl font-black text-gray-900">Phản Hồi &amp; Đánh Giá Thực Tế</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-xl border border-gray-100 bg-gray-50/50 space-y-2">
            <div class="flex text-amber-400 text-xs">★★★★★</div>
            <p class="text-xs text-gray-600 italic">"Sách được đóng hộp carton rất chắc chắn, mép gáy phẳng phiu không một vết cấn. Đặt đơn chiều hôm trước mà trưa hôm sau đã nhận được rồi!"</p>
            <div class="text-[11px] font-bold text-gray-900">— Trần Minh Hoàng <span class="text-gray-400 font-normal">(Hà Nội)</span></div>
          </div>
          <div class="p-4 rounded-xl border border-gray-100 bg-gray-50/50 space-y-2">
            <div class="flex text-amber-400 text-xs">★★★★★</div>
            <p class="text-xs text-gray-600 italic">"Mua bộ truyện tâm lý học đường cho hai bé ở nhà. Sách in màu đẹp, giấy dày dặn và chuẩn sách thật của NXB Trẻ. Shop tư vấn nhiệt tình."</p>
            <div class="text-[11px] font-bold text-gray-900">— Nguyễn Lê Thảo Vy <span class="text-gray-400 font-normal">(TP.HCM)</span></div>
          </div>
          <div class="p-4 rounded-xl border border-gray-100 bg-gray-50/50 space-y-2">
            <div class="flex text-amber-400 text-xs">★★★★★</div>
            <p class="text-xs text-gray-600 italic">"Cuốn 'Lắng Nghe Khi Thị Trường Lên Tiếng' bản dịch rất chuẩn. Shop còn tặng kèm bookmark và bao bì bọc chống sốc kỹ càng. Rất tin tưởng!"</p>
            <div class="text-[11px] font-bold text-gray-900">— Lê Quốc Bảo <span class="text-gray-400 font-normal">(Đà Nẵng)</span></div>
          </div>
        </div>

        <!-- Call to Action Banner -->
        <div class="bg-gradient-to-r from-brand-red to-red-800 text-white rounded-xl p-6 sm:p-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="space-y-1 text-center sm:text-left">
            <h3 class="text-lg font-bold">Bạn Cần Tư Vấn Chọn Sách Phù Hợp?</h3>
            <p class="text-xs text-red-100">Đội ngũ biên tập DuwcsAnhLib luôn sẵn sàng hỗ trợ bạn tìm kiếm ấn bản ý nghĩa nhất.</p>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <a href="tel:0933543987" class="px-5 py-2.5 bg-yellow-400 hover:bg-yellow-300 text-stone-950 font-bold rounded-lg text-xs shadow-md transition flex items-center gap-1.5 cursor-pointer">
              <span class="material-symbols-outlined text-sm">call</span>
              <span>Hotline: 0933.543.987</span>
            </a>
            <button onclick="showView('shop')" class="px-5 py-2.5 bg-white/20 hover:bg-white/30 text-white font-bold rounded-lg text-xs border border-white/30 transition cursor-pointer">
              Vào Cửa Hàng
            </button>
          </div>
        </div>
      </section>

    </div>

    <!-- VIEW: FULL SHOP CATALOG (WITH FILTER & RICH METADATA) -->
    <div id="view-shop" class="hidden space-y-6">
      
      <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center justify-between text-xs">
        <div class="flex items-center gap-1.5 text-gray-500">
          <a href="/" class="hover:text-brand-red">Trang chủ</a>
          <span>/</span>
          <span class="text-gray-900 font-bold">Cửa hàng sách DuwcsAnhLib</span>
        </div>
        <span id="shopResultTotal" class="font-bold text-brand-red">25 Sản phẩm</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        <!-- Sidebar Filter -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <h3 class="font-black text-sm text-gray-900 uppercase border-b border-gray-100 pb-2">Danh Mục Sách</h3>
            <div class="space-y-1.5 text-xs">
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="All" checked onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Tất cả thể loại</span>
                </span>
                <span class="text-gray-400 font-mono">(25)</span>
              </label>
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="Văn học" onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Văn học & Tản văn</span>
                </span>
                <span class="text-gray-400 font-mono">(5)</span>
              </label>
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="Kinh tế" onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Kinh tế & Kinh doanh</span>
                </span>
                <span class="text-gray-400 font-mono">(5)</span>
              </label>
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="Tâm lý" onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Tâm lý & Đời sống</span>
                </span>
                <span class="text-gray-400 font-mono">(5)</span>
              </label>
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="Kỹ năng" onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Kỹ năng phát triển</span>
                </span>
                <span class="text-gray-400 font-mono">(5)</span>
              </label>
              <label class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <span class="flex items-center gap-2">
                  <input type="radio" name="catFilter" value="Thiếu nhi" onchange="handleSidebarFilter()" class="text-brand-red focus:ring-red-500">
                  <span>Sách Thiếu nhi</span>
                  </span>
                <span class="text-gray-400 font-mono">(5)</span>
              </label>
            </div>

            <h3 class="font-black text-sm text-gray-900 uppercase border-b border-gray-100 pb-2 pt-2">Khoảng Giá</h3>
            <div class="space-y-1.5 text-xs">
              <label class="flex items-center gap-2 p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <input type="radio" name="priceRange" value="all" checked onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Tất cả mức giá</span>
              </label>
              <label class="flex items-center gap-2 p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <input type="radio" name="priceRange" value="under70" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Dưới 70.000 đ</span>
              </label>
              <label class="flex items-center gap-2 p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <input type="radio" name="priceRange" value="70to100" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>70.000 đ – 100.000 đ</span>
              </label>
              <label class="flex items-center gap-2 p-1.5 rounded hover:bg-gray-50 cursor-pointer">
                <input type="radio" name="priceRange" value="above100" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Trên 100.000 đ</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Product Grid -->
        <div class="lg:col-span-3 space-y-4">
          <div class="flex items-center justify-between bg-white p-3 rounded-xl border border-gray-200 text-xs">
            <span class="text-gray-500">Sắp xếp theo:</span>
            <select id="sortBy" onchange="handleSort()" class="bg-gray-50 border border-gray-200 rounded px-2.5 py-1 text-xs font-semibold text-gray-700 outline-none">
              <option value="featured">Nổi bật nhất</option>
              <option value="price-asc">Giá: Thấp đến Cao</option>
              <option value="price-desc">Giá: Cao đến Thấp</option>
              <option value="discount">Giảm giá nhiều nhất</option>
            </select>
          </div>

          <div id="fullCatalogGrid" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <!-- Populated by JS -->
          </div>
        </div>

      </div>
    </div>

    <!-- VIEW: STATIC CONTENT (BLOG / ABOUT / POLICIES) -->
    <div id="view-content" class="hidden bg-white p-6 sm:p-10 rounded-2xl border border-gray-200 shadow-sm max-w-4xl mx-auto space-y-6">
      <div id="contentBody" class="prose max-w-none text-xs sm:text-sm text-gray-700 leading-relaxed">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- VIEW: BLOGS LIST -->
    <div id="view-blogs" class="hidden space-y-6">
      <div class="text-center max-w-xl mx-auto space-y-2">
        <h2 class="text-2xl font-black text-gray-900 uppercase">Góc Đọc &amp; Review Sách DuwcsAnhLib</h2>
        <p class="text-xs text-gray-500">Những bài viết gợi mở tư duy, review chiều sâu và kinh nghiệm chọn sách hay</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div onclick="showView('content', 'blog-01')" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md hover:border-brand-red transition cursor-pointer flex flex-col justify-between">
          <div class="p-5 space-y-2">
            <span class="text-[10px] font-bold text-brand-red bg-red-50 px-2 py-0.5 rounded">TƯ VẤN ĐỌC SÁCH</span>
            <h3 class="font-bold text-sm text-gray-900">5 Cuốn Sách Kinh Điển Khai Phóng Tư Duy Bạn Không Thể Bỏ Lỡ</h3>
            <p class="text-xs text-gray-500 line-clamp-3">Khám phá danh sách 5 tác phẩm định hình tư duy logic, sự kiên định và phong thái sống đĩnh đạc từ NXB Trẻ.</p>
          </div>
          <div class="px-5 py-3 border-t border-gray-100 text-[11px] text-gray-400 font-semibold flex justify-between">
            <span>Biên tập viên DuwcsAnhLib</span>
            <span>Đọc tiếp &rarr;</span>
          </div>
        </div>

        <div onclick="showView('content', 'blog-02')" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md hover:border-brand-red transition cursor-pointer flex flex-col justify-between">
          <div class="p-5 space-y-2">
            <span class="text-[10px] font-bold text-brand-red bg-red-50 px-2 py-0.5 rounded">VĂN HÓA ĐỌC</span>
            <h3 class="font-bold text-sm text-gray-900">Nghệ Thuật Bảo Quản Sách Chuẩn Thư Viện: Từng Nếp Gáy Đều Nguyên Vẹn</h3>
            <p class="text-xs text-gray-500 line-clamp-3">Chia sẻ bí quyết bảo vệ sách trước khí hậu nóng ẩm, cách sắp xếp kệ sách khoa học và bảo tồn vẻ đẹp ấn bản qua năm tháng.</p>
          </div>
          <div class="px-5 py-3 border-t border-gray-100 text-[11px] text-gray-400 font-semibold flex justify-between">
            <span>Chuyên mục Bảo tồn sách</span>
            <span>Đọc tiếp &rarr;</span>
          </div>
        </div>

        <div onclick="showView('content', 'blog-03')" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md hover:border-brand-red transition cursor-pointer flex flex-col justify-between">
          <div class="p-5 space-y-2">
            <span class="text-[10px] font-bold text-brand-red bg-red-50 px-2 py-0.5 rounded">KỸ NĂNG SỐNG</span>
            <h3 class="font-bold text-sm text-gray-900">Vượt Qua Hội Chứng Sợ Bỏ Lỡ (FOMO) Trong Kỷ Nguyên Số</h3>
            <p class="text-xs text-gray-500 line-clamp-3">Những đúc kết quý giá từ bộ truyện tâm lý học đường giúp người trẻ tìm lại sự an định và định vị giá trị của chính mình.</p>
          </div>
          <div class="px-5 py-3 border-t border-gray-100 text-[11px] text-gray-400 font-semibold flex justify-between">
            <span>Tâm lý học ứng dụng</span>
            <span>Đọc tiếp &rarr;</span>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- ENRICHED QUICK VIEW MODAL (RICH METADATA & TABS) -->
  <div id="quickViewModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-3xl w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-gray-200 p-6 sm:p-8 relative">
      <button onclick="closeQuickView()" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center font-bold text-gray-600 transition cursor-pointer">
        <span class="material-symbols-outlined text-base">close</span>
      </button>
      
      <div id="quickViewBody">
        <!-- Rendered by JS -->
      </div>
    </div>
  </div>

  <!-- INTERACTIVE WISHLIST DRAWER (DANH SÁCH YÊU THÍCH) -->
  <div id="wishlistDrawer" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex justify-end">
    <div class="bg-white w-full max-w-md h-full flex flex-col shadow-2xl p-6 overflow-y-auto">
      
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <h3 class="text-base font-black text-gray-900 uppercase flex items-center gap-2">
          <span class="material-symbols-outlined text-brand-red fill-icon text-xl">favorite</span>
          <span>SÁCH YÊU THÍCH CỦA BẠN</span>
          <span id="wishlistDrawerBadge" class="text-xs font-extrabold px-2 py-0.5 rounded-full bg-red-100 text-brand-red">0 cuốn</span>
        </h3>
        <button onclick="closeWishlist()" class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center font-bold text-gray-600 cursor-pointer">
          <span class="material-symbols-outlined text-base">close</span>
        </button>
      </div>

      <!-- Wishlist Items Container -->
      <div id="wishlistItemsContainer" class="flex-1 py-4 space-y-3 overflow-y-auto">
        <!-- Populated by JS -->
      </div>

      <!-- Wishlist Footer Actions -->
      <div class="border-t border-gray-200 pt-4 space-y-2">
        <button onclick="addAllWishlistToCart()" class="w-full py-3 bg-brand-red hover:bg-red-700 text-white font-extrabold rounded-xl text-xs uppercase tracking-wider shadow-md transition flex items-center justify-center gap-2 cursor-pointer">
          <span class="material-symbols-outlined text-base">add_shopping_cart</span>
          <span>Thêm Tất Cả Vào Giỏ Hàng</span>
        </button>
        <button onclick="closeWishlist()" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-xl text-xs transition">
          Tiếp tục chọn sách
        </button>
      </div>

    </div>
  </div>

  <!-- SLIDE-OUT CART & CHECKOUT DRAWER -->
  <div id="cartDrawer" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex justify-end">
    <div class="bg-white w-full max-w-md h-full flex flex-col shadow-2xl p-6 overflow-y-auto">
      
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <h3 class="text-base font-black text-gray-900 uppercase flex items-center gap-2">
          <span>GIỎ HÀNG CỦA BẠN</span>
          <span id="drawerBadge" class="text-xs font-extrabold px-2 py-0.5 rounded-full bg-red-100 text-brand-red">0 cuốn</span>
        </h3>
        <button onclick="closeCart()" class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center font-bold text-gray-600 cursor-pointer">
          <span class="material-symbols-outlined text-base">close</span>
        </button>
      </div>

      <!-- Free Shipping Progress -->
      <div class="py-3 border-b border-gray-100">
        <div class="flex justify-between text-[11px] mb-1 font-semibold">
          <span id="freeshipNotice">Thêm 250.000 đ để được FREESHIP</span>
          <span id="freeshipPct" class="text-brand-red font-bold">0%</span>
        </div>
        <div class="w-full bg-gray-200 h-1.5 rounded-full overflow-hidden">
          <div id="freeshipBar" class="bg-brand-red h-full w-0 transition-all duration-300"></div>
        </div>
      </div>

      <!-- Items List -->
      <div id="cartItemsContainer" class="flex-1 py-3 space-y-3 overflow-y-auto">
        <!-- Populated by JS -->
      </div>

      <!-- Footer Checkout Actions -->
      <div class="border-t border-gray-200 pt-4 space-y-3">
        
        <!-- Voucher Input -->
        <div class="flex gap-2">
          <input type="text" id="voucherCode" placeholder="Mã giảm giá (Thử: DUWCSANH10 hoặc TRIAN)" class="flex-1 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs outline-none uppercase font-mono">
          <button onclick="applyVoucher()" class="px-3 py-1.5 bg-gray-800 hover:bg-black text-white rounded text-xs font-bold transition">Áp dụng</button>
        </div>

        <div class="space-y-1.5 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-200">
          <div class="flex justify-between">
            <span>Tạm tính sách:</span>
            <span id="drawerSubtotal" class="font-bold text-gray-900">0 đ</span>
          </div>
          <div class="flex justify-between">
            <span>Giảm giá voucher:</span>
            <span id="drawerDiscount" class="font-bold text-emerald-600">0 đ</span>
          </div>
          <div class="flex justify-between">
            <span>Phí vận chuyển:</span>
            <span id="drawerShipping" class="font-bold text-gray-900">25.000 đ</span>
          </div>
          <div class="flex justify-between text-sm font-black text-brand-red pt-2 border-t border-gray-200">
            <span>TỔNG CỘNG:</span>
            <span id="drawerTotal" class="text-base text-brand-red">0 đ</span>
          </div>
        </div>

        <div id="checkoutFormBlock" class="space-y-2">
          <input type="text" id="custName" placeholder="Họ và tên người nhận" value="Nguyễn Văn A" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
          <input type="text" id="custPhone" placeholder="Số điện thoại" value="0933543987" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
          <input type="text" id="custAddress" placeholder="Địa chỉ giao sách" value="Khu dân cư / Văn phòng làm việc" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
          <button onclick="processCheckout()" class="w-full py-3 bg-brand-red bg-brand-red-hover text-white font-black rounded-xl text-xs uppercase tracking-wider shadow-md transition cursor-pointer">
            Xác Nhận Đặt Hàng (Thanh Toán Khi Nhận Sách - COD)
          </button>
        </div>

        <div id="orderSuccessBlock" class="hidden p-4 rounded-xl bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs space-y-2">
          <div class="font-bold text-sm text-emerald-800 flex items-center gap-1.5">
            <span class="material-symbols-outlined text-lg text-emerald-600">check_circle</span>
            <span>ĐẶT HÀNG THÀNH CÔNG!</span>
          </div>
          <p>Mã đơn hàng: <strong id="orderCodeGenerated">#DAL-1082</strong></p>
          <p>Đơn hàng đã được tiếp nhận. Đội ngũ DuwcsAnhLib sẽ liên hệ qua hotline <strong>0933.543.987</strong> để xác nhận và điều phối vận chuyển.</p>
          <button onclick="resetCart()" class="w-full py-2 bg-emerald-700 text-white rounded font-bold mt-2">Tiếp tục mua sách</button>
        </div>

      </div>

    </div>
  </div>

  <!-- FLOATING TOAST NOTIFICATION (KHÔNG MỞ DRAWER, HIỂN THỊ THÔNG BÁO TINH TẾ) -->
  <div id="toastNotification" class="fixed bottom-6 right-6 z-50 transform translate-y-24 opacity-0 transition-all duration-300 pointer-events-none flex items-center gap-3 bg-stone-900/95 text-white px-5 py-3.5 rounded-2xl shadow-2xl border border-stone-700 backdrop-blur-md max-w-md">
    <div class="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
      <span class="material-symbols-outlined text-lg">check_circle</span>
    </div>
    <div class="text-xs flex-1">
      <div id="toastMessage" class="font-bold text-white leading-tight">Đã thêm vào giỏ hàng</div>
      <div class="text-[11px] text-stone-400 mt-0.5">Bấm biểu tượng giỏ hàng ở góc phải để thanh toán.</div>
    </div>
    <button onclick="openCart()" class="pointer-events-auto px-3 py-1.5 bg-brand-red hover:bg-red-700 text-white rounded-lg text-xs font-bold transition shrink-0 cursor-pointer">
      Xem giỏ
    </button>
  </div>

  <!-- MEGA FOOTER -->
  <footer class="bg-white border-t border-gray-200 mt-16 text-gray-600 text-xs">
    
    <!-- Newsletter Bar -->
    <div class="bg-[#F8F9FA] border-b border-gray-200 py-6 px-4">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined text-3xl text-brand-red">mail</span>
          <div>
            <h4 class="font-black text-sm text-gray-900 uppercase">Đăng Ký Nhận Bản Tin Ưu Đãi</h4>
            <p class="text-xs text-gray-500">Nhận ngay voucher giảm giá 10% và thông tin ấn bản mới phát hành</p>
          </div>
        </div>
        <div class="flex w-full md:w-auto">
          <input type="email" placeholder="Nhập địa chỉ email của bạn..." class="px-4 py-2 border border-gray-300 rounded-l-lg text-xs outline-none w-64">
          <button onclick="alert('Cảm ơn bạn đã đăng ký nhận bản tin DuwcsAnhLib!')" class="px-5 py-2 bg-brand-red hover:bg-red-700 text-white font-bold rounded-r-lg text-xs uppercase transition">Đăng ký</button>
        </div>
      </div>
    </div>

    <!-- Footer Columns -->
    <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-8">
      
      <!-- Col 1 -->
      <div class="space-y-3">
        <div class="flex items-center gap-2 cursor-pointer" onclick="showView('shop')">
          <img src="/assets/site-icon-512.png" alt="DuwcsAnhLib" class="w-8 h-8 rounded-lg object-contain shadow-sm">
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
        </div>
        <div class="pt-1">
          <a href="/" class="text-[11px] text-gray-400 hover:text-brand-red underline">
            &larr; Xem lại Giới thiệu &amp; Landing Page
          </a>
        </div>
        <p class="text-xs text-gray-500 leading-relaxed">
          Hệ thống hiệu sách trực tuyến hàng đầu dành cho độc giả yêu sách. Cam kết 100% ấn bản chuẩn hóa từ Nhà xuất bản Trẻ.
        </p>
        <div class="text-[12px] text-gray-800 font-bold flex items-center gap-1.5">
          <span class="material-symbols-outlined text-sm text-brand-red">phone_in_talk</span>
          Hotline: <span class="text-brand-red">0933 543 987</span>
        </div>
      </div>

      <!-- Col 2 -->
      <div class="space-y-2">
        <h4 class="font-bold text-gray-900 uppercase">Dịch Vụ & Hỗ Trợ</h4>
        <ul class="space-y-1.5 text-xs text-gray-500">
          <li><button onclick="showView('content', 'giao-hang')" class="hover:text-brand-red">Điều khoản giao hàng</button></li>
          <li><button onclick="showView('content', 'doi-tra')" class="hover:text-brand-red">Chính sách đổi trả & hoàn tiền</button></li>
          <li><button onclick="showView('content', 'bao-mat')" class="hover:text-brand-red">Chính sách bảo mật thông tin</button></li>
          <li><button onclick="showView('content', 'lien-he')" class="hover:text-brand-red">Hệ thống liên hệ</button></li>
        </ul>
      </div>

      <!-- Col 3 -->
      <div class="space-y-2">
        <h4 class="font-bold text-gray-900 uppercase">Danh Mục Tuyển Chọn</h4>
        <ul class="space-y-1.5 text-xs text-gray-500">
          <li><button onclick="filterCatAndShow('Văn học')" class="hover:text-brand-red">Văn học Việt Nam & Thế giới</button></li>
          <li><button onclick="filterCatAndShow('Kinh tế')" class="hover:text-brand-red">Kinh tế, Khởi nghiệp & Quản trị</button></li>
          <li><button onclick="filterCatAndShow('Tâm lý')" class="hover:text-brand-red">Tâm lý học ứng dụng</button></li>
          <li><button onclick="filterCatAndShow('Kỹ năng')" class="hover:text-brand-red">Kỹ năng mềm & Phát triển bản thân</button></li>
          <li><button onclick="filterCatAndShow('Thiếu nhi')" class="hover:text-brand-red">Sách tranh & Văn học thiếu nhi</button></li>
        </ul>
      </div>

      <!-- Col 4 -->
      <div class="space-y-3">
        <h4 class="font-bold text-gray-900 uppercase">Đối Tác Vận Chuyển & Thanh Toán</h4>
        <div class="flex flex-wrap gap-2 text-xs font-semibold text-gray-600">
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">VNPost</span>
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">ViettelPost</span>
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">GHTK</span>
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">MoMo</span>
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">VNPAY</span>
          <span class="px-2 py-1 bg-gray-100 rounded border border-gray-200">COD</span>
        </div>
        <div class="pt-2">
          <span class="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 text-white rounded text-[11px] font-bold">
            <span class="material-symbols-outlined text-xs">verified</span>
            ĐÃ THÔNG BÁO BỘ CÔNG THƯƠNG
          </span>
        </div>
      </div>

    </div>

    <div class="bg-gray-100 py-4 px-4 text-center text-[11px] text-gray-500 border-t border-gray-200">
      © 2026 DuwcsAnhLib. Bản quyền phân phối sách thuộc về Nhà xuất bản Trẻ & Hệ thống DuwcsAnhLib. Hotline: 0933.543.987.
    </div>
  </footer>

  <!-- JAVASCRIPT LOGIC CHUYÊN NGHIỆP -->
  <script>
    const allProducts = __PRODUCTS_JSON__;
    const allPages = __PAGES_JSON__;
    let cart = [];
    let wishlist = ['DAL-001', 'DAL-006', 'DAL-011']; // 3 tựa sách yêu thích mẫu ban đầu
    let voucherDiscount = 0;
    let toastTimeout = null;

    function formatVND(num) {
      return new Intl.NumberFormat('vi-VN').format(num) + ' đ';
    }

    // Hiển thị thông báo nhỏ (Toast) khi thêm vào giỏ hoặc yêu thích
    function showToast(message, subtitle = 'Bấm biểu tượng giỏ hàng ở góc phải để thanh toán.') {
      const toast = document.getElementById('toastNotification');
      const msgEl = document.getElementById('toastMessage');
      if (!toast || !msgEl) return;
      
      msgEl.innerHTML = message;
      toast.classList.remove('translate-y-24', 'opacity-0', 'pointer-events-none');
      toast.classList.add('translate-y-0', 'opacity-100');
      
      if (toastTimeout) clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {
        toast.classList.add('translate-y-24', 'opacity-0', 'pointer-events-none');
        toast.classList.remove('translate-y-0', 'opacity-100');
      }, 3200);
    }

    // Wishlist (Yêu thích) Logic
    function updateWishlistUI() {
      const badge = document.getElementById('wishlistCountBadge');
      const drawerBadge = document.getElementById('wishlistDrawerBadge');
      if (badge) badge.textContent = wishlist.length;
      if (drawerBadge) drawerBadge.textContent = wishlist.length + ' cuốn';

      const container = document.getElementById('wishlistItemsContainer');
      if (!container) return;

      if (wishlist.length === 0) {
        container.innerHTML = `
          <div class="text-center py-12 text-gray-400 text-xs space-y-3">
            <span class="material-symbols-outlined text-4xl text-gray-300">favorite_border</span>
            <p>Bạn chưa lưu cuốn sách nào vào danh sách yêu thích.<br>Hãy bấm vào biểu tượng trái tim trên các cuốn sách bạn thích nhé!</p>
          </div>
        `;
        return;
      }

      container.innerHTML = wishlist.map(sku => {
        const p = allProducts.find(x => x.SKU === sku);
        if (!p) return '';
        const sale = parseInt(p['Sale price'] || p['Regular price'] || 0);
        const coverSrc = `/assets/covers/${sku}.png`;
        return `
          <div class="flex items-center gap-3 p-3 rounded-xl bg-gray-50 border border-gray-200 text-xs">
            <img src="${coverSrc}" alt="${p['Name']}" class="w-12 h-16 object-cover rounded-lg shadow-sm border border-gray-200">
            <div class="flex-1 min-w-0">
              <div class="font-bold text-gray-900 line-clamp-1">${p['Name']}</div>
              <div class="text-gray-500 text-[11px]">${p['Attribute 1 value(s)']}</div>
              <div class="font-black text-brand-red mt-1">${formatVND(sale)}</div>
            </div>
            <div class="flex flex-col gap-1 shrink-0">
              <button onclick="addToCart('${sku}')" class="px-2.5 py-1 bg-red-50 hover:bg-brand-red text-brand-red hover:text-white rounded text-[11px] font-bold transition flex items-center gap-1 cursor-pointer">
                <span class="material-symbols-outlined text-xs">shopping_cart</span>
                <span>Thêm giỏ</span>
              </button>
              <button onclick="toggleWishlist('${sku}')" class="text-gray-400 hover:text-brand-red text-[10px] text-center cursor-pointer transition">
                Xóa
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function toggleWishlist(sku, event) {
      if (event) event.stopPropagation();
      const p = allProducts.find(x => x.SKU === sku);
      const name = p ? p['Name'] : 'Sách';
      
      const idx = wishlist.indexOf(sku);
      if (idx > -1) {
        wishlist.splice(idx, 1);
        showToast(`Đã xóa <strong>${name}</strong> khỏi danh sách yêu thích.`);
      } else {
        wishlist.push(sku);
        showToast(`Đã lưu <strong>${name}</strong> vào danh sách yêu thích!`, 'Xem lại trong mục Yêu thích ở góc trên.');
      }
      
      updateWishlistUI();
      // Re-render grids to update heart status
      renderFlashSale();
      const currentTab = document.querySelector('[id^="tab-btn-"][class*="bg-brand-red"]');
      if (currentTab) {
        const tabKey = currentTab.id.replace('tab-btn-', '');
        switchTabContent(tabKey);
      }
      handleSidebarFilter();
    }

    function openWishlist() {
      updateWishlistUI();
      document.getElementById('wishlistDrawer').classList.remove('hidden');
    }

    function closeWishlist() {
      document.getElementById('wishlistDrawer').classList.add('hidden');
    }

    function addAllWishlistToCart() {
      if (wishlist.length === 0) return;
      wishlist.forEach(sku => {
        const p = allProducts.find(x => x.SKU === sku);
        if (!p) return;
        const sale = parseInt(p['Sale price'] || p['Regular price'] || 0);
        const existing = cart.find(x => x.sku === sku);
        if (existing) {
          existing.qty++;
        } else {
          cart.push({ sku: sku, name: p['Name'], price: sale, qty: 1 });
        }
      });
      updateCartUI();
      closeWishlist();
      showToast(`Đã thêm toàn bộ <strong>${wishlist.length} cuốn yêu thích</strong> vào giỏ hàng!`);
    }

    // Render Flash Sale Items
    function renderFlashSale() {
      const container = document.getElementById('flashSaleGrid');
      if (!container) return;
      const sorted = [...allProducts].sort((a,b) => b.discount_pct - a.discount_pct).slice(0, 4);
      container.innerHTML = sorted.map(p => createProductCardHTML(p, true)).join('');
    }

    // Render Product Card
    function createProductCardHTML(p, isFlashSale = false) {
      const reg = parseInt(p['Regular price'] || 0);
      const sale = parseInt(p['Sale price'] || reg);
      const sku = p['SKU'];
      const coverSrc = `/assets/covers/${sku}.png`;
      const discount = p.discount_pct || 10;
      const sold = p.sold_count || 30;
      const isLiked = wishlist.includes(sku);

      return `
        <div class="bg-white rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-xl transition-all duration-300 p-3 flex flex-col justify-between group relative overflow-hidden">
          
          <!-- Discount Badge on Top Left -->
          ${discount > 0 ? `
            <div class="absolute top-2 left-2 z-10 bg-brand-red text-white text-[10px] font-extrabold px-1.5 py-0.5 rounded shadow">
              -${discount}%
            </div>
          ` : ''}

          <!-- Favorite Heart Button on Top Right -->
          <button onclick="toggleWishlist('${sku}', event)" class="absolute top-2 right-2 z-10 w-7 h-7 rounded-full bg-white/90 hover:bg-white text-gray-500 hover:text-brand-red shadow flex items-center justify-center transition cursor-pointer" title="Lưu vào danh sách yêu thích">
            <span class="material-symbols-outlined text-base ${isLiked ? 'fill-icon text-brand-red' : ''}">favorite</span>
          </button>

          <!-- Book Cover with Quick View Overlay -->
          <div class="relative overflow-hidden rounded-lg bg-gray-50 aspect-[2/3] cursor-pointer" onclick="openQuickView('${sku}')">
            <img src="${coverSrc}" alt="${p['Name']}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" onerror="this.onerror=null; this.src='/assets/logo-duwcsanhlib.png'">
            
            <!-- Quick View Button Overlay -->
            <div class="absolute inset-0 bg-black/35 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center p-2">
              <span class="px-3 py-1.5 bg-white text-gray-900 rounded-full text-xs font-bold shadow-md hover:bg-brand-red hover:text-white transition flex items-center gap-1">
                <span class="material-symbols-outlined text-xs">visibility</span>
                <span>Xem nhanh</span>
              </span>
            </div>
          </div>

          <!-- Book Info -->
          <div class="pt-3 space-y-1">
            <div class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">${p['Attribute 1 value(s)']}</div>
            <h3 class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition line-clamp-2 leading-snug cursor-pointer h-8" onclick="openQuickView('${sku}')">
              ${p['Name']}
            </h3>
            
            <!-- Star Ratings -->
            <div class="flex items-center gap-0.5 text-amber-500 pt-0.5">
              <span class="material-symbols-outlined text-sm fill-icon text-amber-400">star</span>
              <span class="material-symbols-outlined text-sm fill-icon text-amber-400">star</span>
              <span class="material-symbols-outlined text-sm fill-icon text-amber-400">star</span>
              <span class="material-symbols-outlined text-sm fill-icon text-amber-400">star</span>
              <span class="material-symbols-outlined text-sm fill-icon text-amber-400">star</span>
              <span class="text-gray-400 text-[10px] ml-1">(${p.reviews_count})</span>
            </div>

            <!-- Price Row (Dual Price) -->
            <div class="flex items-baseline gap-2 pt-1">
              <span class="text-sm sm:text-base font-black text-brand-red">${formatVND(sale)}</span>
              ${reg > sale ? `<span class="text-[11px] text-gray-400 line-through">${formatVND(reg)}</span>` : ''}
            </div>

            <!-- Flash Sale Progress Bar -->
            ${isFlashSale ? `
              <div class="pt-1.5">
                <div class="w-full bg-red-100 h-2 rounded-full overflow-hidden">
                  <div class="bg-brand-red h-full" style="width: ${Math.min(100, sold * 2)}%"></div>
                </div>
                <div class="text-[10px] text-brand-red font-bold mt-0.5">Đã bán ${sold} cuốn</div>
              </div>
            ` : ''}
          </div>

          <!-- Add to Cart Button (KHÔNG TỰ ĐỘNG BẬT DRAWER, CHỈ BẬT TOAST) -->
          <button onclick="addToCart('${sku}')" class="mt-3 w-full py-1.5 bg-red-50 hover:bg-brand-red text-brand-red hover:text-white border border-red-200 hover:border-brand-red rounded-lg text-xs font-bold transition flex items-center justify-center gap-1 cursor-pointer">
            <span class="material-symbols-outlined text-sm">shopping_cart</span>
            <span>Thêm giỏ hàng</span>
          </button>
        </div>
      `;
    }

    // Tab Content Switcher
    function switchTabContent(tabKey) {
      ['bestseller', 'new', 'vanhoc', 'kinhte'].forEach(t => {
        const btn = document.getElementById('tab-btn-' + t);
        if (!btn) return;
        if (t === tabKey) {
          btn.className = 'px-3.5 py-1.5 rounded-full bg-brand-red text-white transition';
        } else {
          btn.className = 'px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition';
        }
      });

      let filtered = [];
      if (tabKey === 'bestseller') {
        filtered = [...allProducts].sort((a,b) => b.sold_count - a.sold_count).slice(0, 8);
      } else if (tabKey === 'new') {
        filtered = [...allProducts].slice(0, 8);
      } else if (tabKey === 'vanhoc') {
        filtered = allProducts.filter(p => p['Categories'].includes('Văn học')).slice(0, 8);
      } else if (tabKey === 'kinhte') {
        filtered = allProducts.filter(p => p['Categories'].includes('Kinh tế')).slice(0, 8);
      }
      const grid = document.getElementById('tabProductsGrid');
      if (grid) {
        grid.innerHTML = filtered.map(p => createProductCardHTML(p)).join('');
      }
    }

    // Enriched Quick View Modal
    function openQuickView(sku) {
      const p = allProducts.find(x => x['SKU'] === sku);
      if (!p) return;
      const reg = parseInt(p['Regular price'] || 0);
      const sale = parseInt(p['Sale price'] || reg);
      const coverSrc = `/assets/covers/${sku}.png`;
      const modal = document.getElementById('quickViewModal');
      const body = document.getElementById('quickViewBody');
      const isLiked = wishlist.includes(sku);

      body.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
          
          <!-- Col Trái: Ảnh bìa lớn & nhãn -->
          <div class="md:col-span-5 space-y-3">
            <div class="rounded-2xl overflow-hidden bg-gray-50 border border-gray-200 shadow-md aspect-[2/3] relative">
              <img src="${coverSrc}" alt="${p['Name']}" class="w-full h-full object-cover">
              ${p.discount_pct > 0 ? `
                <span class="absolute top-3 left-3 bg-brand-red text-white text-xs font-black px-2.5 py-1 rounded-md shadow">
                  -${p.discount_pct}%
                </span>
              ` : ''}
            </div>

            <!-- Cam kết đóng gói nhanh -->
            <div class="p-3 bg-amber-50 border border-amber-200 rounded-xl text-[11px] text-amber-900 space-y-1">
              <div class="font-bold flex items-center gap-1 text-amber-800">
                <span class="material-symbols-outlined text-sm">shield</span>
                <span>Cam kết DuwcsAnhLib:</span>
              </div>
              <div>• 100% Ấn bản chính thống từ NXB Trẻ</div>
              <div>• Đóng hộp carton 3 lớp bảo vệ gáy sách</div>
              <div>• Đổi trả 7 ngày nếu cấn móp hoặc lỗi in</div>
            </div>
          </div>

          <!-- Col Phải: Chi tiết thông số & Nội dung -->
          <div class="md:col-span-7 space-y-4">
            <div>
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-black px-2.5 py-1 rounded-full bg-red-100 text-brand-red uppercase tracking-wider">${p['Categories']}</span>
                <span class="text-xs text-gray-500 font-mono">Mã: <strong>${sku}</strong></span>
              </div>
              <h2 class="text-xl sm:text-2xl font-black text-gray-900 mt-2 leading-snug">${p['Name']}</h2>
              <div class="text-xs text-gray-600 mt-1 font-medium">${p.subtitle || ''}</div>
            </div>

            <!-- Giá & Tồn kho -->
            <div class="flex items-baseline gap-3 p-3 bg-red-50/60 rounded-xl border border-red-100">
              <span class="text-2xl font-black text-brand-red">${formatVND(sale)}</span>
              ${reg > sale ? `<span class="text-sm text-gray-400 line-through">${formatVND(reg)}</span>` : ''}
              <span class="text-xs font-bold text-emerald-700 ml-auto flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">check_circle</span>
                <span>Còn hàng (${p['Stock']} cuốn)</span>
              </span>
            </div>

            <!-- Câu trích dẫn đắt giá -->
            <div class="p-3.5 bg-stone-50 border-l-4 border-brand-red rounded-r-xl italic text-xs text-stone-700 leading-relaxed">
              "${p.quote}"
            </div>

            <!-- Bảng thuộc tính chuẩn sách -->
            <div class="grid grid-cols-2 gap-2 text-xs text-gray-700 bg-gray-50 p-3 rounded-xl border border-gray-200">
              <div><span class="text-gray-400">Tác giả:</span> <strong class="text-gray-900 block">${p['Attribute 1 value(s)']}</strong></div>
              <div><span class="text-gray-400">Nhà xuất bản:</span> <strong class="text-gray-900 block">${p['Attribute 2 value(s)']}</strong></div>
              <div><span class="text-gray-400">Năm xuất bản:</span> <span class="block">${p['Attribute 3 value(s)']}</span></div>
              <div><span class="text-gray-400">Số trang &amp; Khổ:</span> <span class="block">${p['Attribute 4 value(s)']} tr. • ${p['Attribute 6 value(s)']}</span></div>
              <div><span class="text-gray-400">Quy cách bìa:</span> <span class="block">${p.format}</span></div>
              <div><span class="text-gray-400">Mã ISBN:</span> <span class="font-mono block text-gray-800">${p['Attribute 7 value(s)']}</span></div>
            </div>

            <!-- Nút hành động -->
            <div class="pt-2 flex gap-3">
              <button onclick="addToCart('${sku}'); closeQuickView();" class="flex-1 py-3 bg-brand-red hover:bg-red-700 text-white font-extrabold rounded-xl text-xs uppercase shadow-md transition cursor-pointer flex items-center justify-center gap-2">
                <span class="material-symbols-outlined text-base">shopping_cart</span>
                <span>Thêm Vào Giỏ Hàng</span>
              </button>
              <button onclick="toggleWishlist('${sku}'); closeQuickView();" class="px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-bold transition flex items-center gap-1 cursor-pointer">
                <span class="material-symbols-outlined text-base ${isLiked ? 'fill-icon text-brand-red' : ''}">favorite</span>
                <span>${isLiked ? 'Đã thích' : 'Lưu'}</span>
              </button>
            </div>
          </div>

        </div>

        <!-- Khối giới thiệu chi tiết -->
        <div class="mt-6 pt-5 border-t border-gray-200 text-xs text-gray-700 space-y-3">
          <h4 class="font-black text-sm text-gray-900 uppercase">Tóm Tắt Tác Phẩm &amp; Giá Trị Đọc:</h4>
          <div class="leading-relaxed space-y-2 text-stone-700">${p['Description']}</div>
          
          <div class="pt-2 p-3 bg-gray-50 rounded-xl border border-gray-100">
            <span class="font-bold text-gray-900 block mb-1">Đánh giá tiêu biểu từ độc giả:</span>
            <p class="italic text-gray-600">"${p.reader_review}"</p>
          </div>
        </div>
      `;
      modal.classList.remove('hidden');
    }

    function closeQuickView() {
      document.getElementById('quickViewModal').classList.add('hidden');
    }

    // Cart Management
    function addToCart(sku) {
      const p = allProducts.find(x => x['SKU'] === sku);
      if (!p) return;
      const sale = parseInt(p['Sale price'] || p['Regular price'] || 0);
      const existing = cart.find(x => x.sku === sku);
      if (existing) {
        existing.qty++;
      } else {
        cart.push({
          sku: sku,
          name: p['Name'],
          price: sale,
          qty: 1
        });
      }
      updateCartUI();
      // HIỂN THỊ THÔNG BÁO NHỎ (TOAST), KHÔNG TỰ ĐỘNG BẬT DRAWER
      showToast(`Đã thêm <strong>${p['Name']}</strong> vào giỏ hàng thành công!`);
    }

    function updateCartUI() {
      const totalQty = cart.reduce((acc, x) => acc + x.qty, 0);
      document.getElementById('cartCountBadge').textContent = totalQty;
      document.getElementById('drawerBadge').textContent = totalQty + ' cuốn';
      
      const subtotal = cart.reduce((acc, x) => acc + (x.price * x.qty), 0);
      document.getElementById('headerCartTotal').textContent = formatVND(subtotal);
      document.getElementById('drawerSubtotal').textContent = formatVND(subtotal);

      // Freeship calculation (250,000 threshold)
      const freeThreshold = 250000;
      let shipping = 25000;
      if (subtotal >= freeThreshold || totalQty === 0) {
        shipping = 0;
        document.getElementById('freeshipNotice').textContent = 'Bạn đã đủ điều kiện FREESHIP toàn quốc!';
        document.getElementById('freeshipPct').textContent = '100%';
        document.getElementById('freeshipBar').style.width = '100%';
      } else {
        const remaining = freeThreshold - subtotal;
        const pct = Math.round((subtotal / freeThreshold) * 100);
        document.getElementById('freeshipNotice').textContent = `Thêm ${formatVND(remaining)} để được FREESHIP`;
        document.getElementById('freeshipPct').textContent = pct + '%';
        document.getElementById('freeshipBar').style.width = pct + '%';
      }

      document.getElementById('drawerShipping').textContent = shipping === 0 ? 'Miễn phí' : formatVND(shipping);
      
      const grandTotal = Math.max(0, subtotal - voucherDiscount + (subtotal > 0 ? shipping : 0));
      document.getElementById('drawerTotal').textContent = formatVND(grandTotal);

      // Render cart items
      const container = document.getElementById('cartItemsContainer');
      if (cart.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-400 text-xs">Giỏ hàng của bạn đang trống.<br>Hãy chọn thêm sách để trải nghiệm!</div>`;
        return;
      }

      container.innerHTML = cart.map(item => `
        <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 border border-gray-200 text-xs">
          <div class="flex-1 pr-2">
            <div class="font-bold text-gray-900 line-clamp-1">${item.name}</div>
            <div class="text-gray-500 font-mono text-[11px] mt-0.5">${item.sku} • <strong class="text-brand-red">${formatVND(item.price)}</strong></div>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="changeQty('${item.sku}', -1)" class="w-6 h-6 rounded bg-gray-200 font-bold hover:bg-gray-300 cursor-pointer">-</button>
            <span class="font-bold text-gray-800 px-1">${item.qty}</span>
            <button onclick="changeQty('${item.sku}', 1)" class="w-6 h-6 rounded bg-gray-200 font-bold hover:bg-gray-300 cursor-pointer">+</button>
            <button onclick="removeCartItem('${item.sku}')" class="text-gray-400 hover:text-brand-red ml-2 font-bold cursor-pointer flex items-center">
              <span class="material-symbols-outlined text-sm">close</span>
            </button>
          </div>
        </div>
      `).join('');
    }

    function changeQty(sku, delta) {
      const item = cart.find(x => x.sku === sku);
      if (!item) return;
      item.qty += delta;
      if (item.qty <= 0) {
        cart = cart.filter(x => x.sku !== sku);
      }
      updateCartUI();
    }

    function removeCartItem(sku) {
      cart = cart.filter(x => x.sku !== sku);
      updateCartUI();
    }

    function openCart() {
      document.getElementById('cartDrawer').classList.remove('hidden');
    }

    function closeCart() {
      document.getElementById('cartDrawer').classList.add('hidden');
    }

    function applyVoucher() {
      const code = document.getElementById('voucherCode').value.trim().toUpperCase();
      if (code === 'DUWCSANH10' || code === 'TRIAN10' || code === 'TRIAN') {
        const subtotal = cart.reduce((acc, x) => acc + (x.price * x.qty), 0);
        voucherDiscount = Math.round(subtotal * 0.1);
        document.getElementById('drawerDiscount').textContent = '-' + formatVND(voucherDiscount);
        showToast('Áp dụng thành công voucher giảm giá 10%!');
        updateCartUI();
      } else {
        alert('Mã không hợp lệ. Vui lòng thử: DUWCSANH10 hoặc TRIAN10');
      }
    }

    function processCheckout() {
      if (cart.length === 0) {
        alert("Giỏ hàng đang trống! Vui lòng chọn ít nhất 1 cuốn sách.");
        return;
      }
      const randomId = 'DAL-' + Math.floor(1000 + Math.random() * 9000);
      document.getElementById('orderCodeGenerated').textContent = '#' + randomId;
      document.getElementById('checkoutFormBlock').classList.add('hidden');
      document.getElementById('orderSuccessBlock').classList.remove('hidden');
    }

    function resetCart() {
      cart = [];
      voucherDiscount = 0;
      updateCartUI();
      document.getElementById('checkoutFormBlock').classList.remove('hidden');
      document.getElementById('orderSuccessBlock').classList.add('hidden');
      closeCart();
      showView('shop');
    }

    // Search and Filters
    function handleSearch() {
      const query = document.getElementById('headerSearchInput').value.toLowerCase().trim();
      const cat = document.getElementById('headerCategorySelect').value;
      showView('shop');
      filterFullCatalog(query, cat);
    }

    function handleHeaderCategory() {
      handleSearch();
    }

    function handleSidebarFilter() {
      const selectedCat = document.querySelector('input[name="catFilter"]:checked').value;
      const selectedPrice = document.querySelector('input[name="priceRange"]:checked').value;
      filterFullCatalog('', selectedCat, selectedPrice);
    }

    function handleSort() {
      handleSidebarFilter();
    }

    function filterFullCatalog(q = '', cat = 'All', priceRange = 'all') {
      let filtered = [...allProducts];

      if (cat !== 'All') {
        filtered = filtered.filter(p => p['Categories'].includes(cat));
      }
      if (q) {
        filtered = filtered.filter(p => 
          p['Name'].toLowerCase().includes(q) || 
          p['Attribute 1 value(s)'].toLowerCase().includes(q) ||
          p['SKU'].toLowerCase().includes(q)
        );
      }
      if (priceRange === 'under70') {
        filtered = filtered.filter(p => parseInt(p['Sale price']) < 70000);
      } else if (priceRange === '70to100') {
        filtered = filtered.filter(p => {
          const pr = parseInt(p['Sale price']);
          return pr >= 70000 && pr <= 100000;
        });
      } else if (priceRange === 'above100') {
        filtered = filtered.filter(p => parseInt(p['Sale price']) > 100000);
      }

      // Sort
      const sortType = document.getElementById('sortBy') ? document.getElementById('sortBy').value : 'featured';
      if (sortType === 'price-asc') {
        filtered.sort((a,b) => parseInt(a['Sale price']) - parseInt(b['Sale price']));
      } else if (sortType === 'price-desc') {
        filtered.sort((a,b) => parseInt(b['Sale price']) - parseInt(a['Sale price']));
      } else if (sortType === 'discount') {
        filtered.sort((a,b) => b.discount_pct - a.discount_pct);
      }

      const totalEl = document.getElementById('shopResultTotal');
      if (totalEl) totalEl.textContent = filtered.length + ' Sản phẩm';
      
      const grid = document.getElementById('fullCatalogGrid');
      if (grid) grid.innerHTML = filtered.map(p => createProductCardHTML(p)).join('');
    }

    function filterCatAndShow(cat) {
      showView('shop');
      const radio = document.querySelector(`input[name="catFilter"][value="${cat}"]`);
      if (radio) radio.checked = true;
      document.getElementById('headerCategorySelect').value = cat;
      filterFullCatalog('', cat);
    }

    // View Navigation
    function showView(viewName, contentKey) {
      ['home', 'shop', 'content', 'blogs'].forEach(v => {
        document.getElementById('view-' + v).classList.add('hidden');
      });
      document.getElementById('view-' + viewName).classList.remove('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });

      if (viewName === 'shop') {
        handleSidebarFilter();
      } else if (viewName === 'content' && contentKey) {
        renderContent(contentKey);
      }
    }

    function renderContent(key) {
      const raw = allPages[key] || "Đang cập nhật nội dung...";
      let html = raw.replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mb-4 text-brand-red">$1</h1>')
                    .replace(/^## (.*$)/gim, '<h2 class="text-lg font-bold mt-6 mb-2 text-gray-800">$1</h2>')
                    .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong>$1</strong>')
                    .replace(/\\n\\n/gim, '</p><p class="mb-3">');
      document.getElementById('contentBody').innerHTML = '<p class="mb-3">' + html + '</p>';
    }

    function scrollToSection(id) {
      showView('home');
      setTimeout(() => {
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }

    // Countdown Timer Loop
    let countdown = 2 * 3600 + 45 * 60 + 18;
    setInterval(() => {
      if (countdown > 0) countdown--;
      const h = Math.floor(countdown / 3600);
      const m = Math.floor((countdown % 3600) / 60);
      const s = countdown % 60;
      const elH = document.getElementById('timerHours');
      const elM = document.getElementById('timerMinutes');
      const elS = document.getElementById('timerSeconds');
      if (elH) elH.textContent = String(h).padStart(2, '0');
      if (elM) elM.textContent = String(m).padStart(2, '0');
      if (elS) elS.textContent = String(s).padStart(2, '0');
    }, 1000);

    // Initial load
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('cat');
    if (catParam) {
      filterCatAndShow(catParam);
    } else {
      showView('shop');
    }
    renderFlashSale();
    switchTabContent('bestseller');
    updateWishlistUI();
    updateCartUI();
  </script>
</body>
</html>
"""

class DuwcsAnhLibServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            ico_file = ASSETS_DIR / 'favicon.ico'
            if ico_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'image/x-icon')
                self.end_headers()
                self.wfile.write(ico_file.read_bytes())
                return

        if self.path.startswith('/assets/'):
            rel_path = self.path[len('/assets/'):]
            target_file = ASSETS_DIR / rel_path
            if target_file.exists() and target_file.is_file():
                self.send_response(200)
                if target_file.suffix == '.png':
                    self.send_header('Content-Type', 'image/png')
                elif target_file.suffix in ['.jpg', '.jpeg']:
                    self.send_header('Content-Type', 'image/jpeg')
                elif target_file.suffix == '.ico':
                    self.send_header('Content-Type', 'image/x-icon')
                self.end_headers()
                self.wfile.write(target_file.read_bytes())
                return
            else:
                self.send_error(404, "Asset Not Found")
                return

        # Route Landing Page chuẩn
        if self.path in ['/landing', '/landing.html', '/landing-page'] or self.path.startswith('/landing?'):
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        # Truy cập gốc (/) LUÔN LUÔN hiển thị Landing Page đầu tiên
        if self.path in ['/', '/index.html'] or self.path.startswith('/?'):
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        # Khi người dùng vào Cửa hàng (/shop) hoặc /home
        if self.path.startswith('/shop') or self.path in ['/home']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            rendered_html = HTML_TEMPLATE.replace(
                '__PRODUCTS_JSON__', json.dumps(products, ensure_ascii=False)
            ).replace(
                '__PAGES_JSON__', json.dumps(pages_data, ensure_ascii=False)
            )
            self.wfile.write(rendered_html.encode('utf-8'))
            return

        super().do_GET()

def start_server(port=8080):
    handler = DuwcsAnhLibServer
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("=" * 65)
            print(f" DUWCSANHLIB 2026 PRODUCTION SERVER STARTED!")
            print(f" URL: http://localhost:{port}")
            print(f" Landing Page: http://localhost:{port}/")
            print(f" Cửa Hàng (Shop): http://localhost:{port}/shop")
            print(f" Hotline: 0933.543.987")
            print("=" * 65)
            try:
                webbrowser.open(f"http://localhost:{port}")
            except Exception:
                pass
            httpd.serve_forever()
    except OSError as e:
        if "10048" in str(e):
            alt_port = port + 1
            print(f"[!] Cổng {port} đang bận, tự động chuyển sang cổng {alt_port}...")
            start_server(alt_port)
        else:
            raise

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    start_server(port)
'''

output_file.write_text(NEW_TEST_WEB_CODE, encoding='utf-8')
print("[2] test_local_web.py đã được cập nhật thành công!")

