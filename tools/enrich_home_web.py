from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'test_local_web.py'
text = p.read_text(encoding='utf-8')

target = '''        <div id="tabProductsGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <!-- Populated by JS -->
        </div>
      </section>

    </div>'''

replacement = '''        <div id="tabProductsGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
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

    </div>'''

if target in text:
    text = text.replace(target, replacement, 1)
    p.write_text(text, encoding='utf-8')
    print('Updated test_local_web.py with full Landing Page sections!')
else:
    print('Target not found in test_local_web.py')

