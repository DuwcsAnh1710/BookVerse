import sys
import json
import re
from pathlib import Path

ROOT = Path("d:/VSCode/HKDN/BookVerse")
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

import test_local_web
from tools.checkout_template import CHECKOUT_VIEW_HTML
from tools.checkout_js import CHECKOUT_JS

print("Starting Master Unified Web Builder with 4 Fixes (Logo, Landing Page, Mega Menu, MoMo)...")

# 1. Read landing page from duwcsanhlib/landing-page.html
landing_raw = (ROOT / "duwcsanhlib" / "landing-page.html").read_text(encoding="utf-8")

start_header = landing_raw.find('<header class="bg-white/95')
if start_header == -1:
    start_header = landing_raw.find('<header')
end_footer = landing_raw.find('</footer>')

if start_header == -1 or end_footer == -1:
    raise ValueError("Could not find header or footer in duwcsanhlib/landing-page.html")

landing_full = landing_raw[start_header:end_footer + len('</footer>')]

# Asset paths to relative assets/
landing_full = landing_full.replace('href="/assets/', 'href="assets/')
landing_full = landing_full.replace('src="/assets/', 'src="assets/')
landing_full = landing_full.replace("'/assets/", "'assets/")
landing_full = landing_full.replace('"/assets/', '"assets/')

# Clean up confusing "3 lớp"
for pattern in [
    (r'quy chuẩn đóng gói 3 lớp bảo vệ chuyên biệt', 'quy chuẩn đóng gói bảo vệ chuyên biệt'),
    (r'Hộp carton sóng 3 lớp', 'Hộp carton sóng chuyên dụng'),
    (r'chống sốc 3 lớp cẩn thận', 'chống sốc cẩn thận'),
    (r'Hộp Carton 3 Lớp', 'Đóng Gói Chống Sốc'),
    (r'hộp carton 3 lớp', 'hộp carton bảo vệ'),
    (r'3 lớp', 'chuyên dụng')
]:
    landing_full = re.sub(pattern[0], pattern[1], landing_full, flags=re.IGNORECASE)

landing_view_html = f"""
  <!-- VIEW: LANDING PAGE ONBOARDING (Chỉ xuất hiện lần đầu tiên, giao diện độc lập toàn màn hình) -->
  <div id="view-landing" class="hidden min-h-screen flex flex-col bg-[#FAF8F5]">
    {landing_full}
  </div>
"""

# 2. Render base store HTML from test_local_web
rendered_html = test_local_web.HTML_TEMPLATE.replace(
    '__PRODUCTS_JSON__', json.dumps(test_local_web.products, ensure_ascii=False)
).replace(
    '__PAGES_JSON__', json.dumps(test_local_web.pages_data, ensure_ascii=False)
)

rendered_html = rendered_html.replace('href="/assets/', 'href="assets/')
rendered_html = rendered_html.replace('src="/assets/', 'src="assets/')
rendered_html = rendered_html.replace("'/assets/", "'assets/")
rendered_html = rendered_html.replace('"/assets/', '"assets/')
rendered_html = rendered_html.replace('`/assets/', '`assets/')
rendered_html = rendered_html.replace('url(/assets/', 'url(assets/')
rendered_html = rendered_html.replace('url(\'/assets/', 'url(\'assets/')
rendered_html = rendered_html.replace('url("/assets/', 'url("assets/')

# Clean up confusing "3 lớp" mentions
for pattern in [
    (r'quy chuẩn đóng gói 3 lớp bảo vệ chuyên biệt', 'quy chuẩn đóng gói bảo vệ chuyên biệt'),
    (r'Hộp carton sóng 3 lớp', 'Hộp carton sóng chuyên dụng'),
    (r'Hộp carton cứng 3 lớp', 'Hộp carton cứng cáp'),
    (r'chống sốc 3 lớp cẩn thận', 'chống sốc cẩn thận'),
    (r'Hộp Carton 3 Lớp', 'Đóng Gói Chống Sốc'),
    (r'hộp carton 3 lớp', 'hộp carton bảo vệ'),
    (r'Màng co \+ Hộp carton 3 lớp', 'Màng co + Hộp carton bảo vệ'),
    (r'Quy chuẩn 3 lớp đóng gói đặc quyền DuwcsAnhLib', 'Quy chuẩn đóng gói đặc quyền DuwcsAnhLib'),
    (r'Quy chuẩn đóng gói 3 lớp bảo vệ', 'Quy chuẩn đóng gói bảo vệ gáy sách'),
    (r'Thùng carton 3 lớp', 'Thùng carton chống va đập'),
    (r'Đóng hộp carton 3 lớp bảo vệ gáy sách', 'Đóng hộp carton bảo vệ gáy sách'),
    (r'2-3 lớp', 'nhiều lớp'),
    (r'3 lớp', 'chuyên dụng')
]:
    rendered_html = re.sub(pattern[0], pattern[1], rendered_html, flags=re.IGNORECASE)

# Mobile Responsiveness Fixes
rendered_html = rendered_html.replace(
    '<html lang="vi">',
    '<html lang="vi" class="overflow-x-hidden w-full">'
)
rendered_html = rendered_html.replace(
    '<body class="min-h-screen flex flex-col antialiased">',
    '<body class="min-h-screen flex flex-col antialiased overflow-x-hidden w-full max-w-full">'
)

# Micro-effects CSS & Print Styles
micro_css = """
    /* Modern 2026 Micro-effects & Animations */
    .hidden { display: none !important; }

    @keyframes float-hero {
      0%, 100% { transform: translateY(0px) rotate(0deg); }
      50% { transform: translateY(-12px) rotate(0.8deg); }
    }
    .animate-float {
      animation: float-hero 5s ease-in-out infinite;
    }

    @keyframes pulse-glow {
      0% { transform: scale(0.92); opacity: 0.55; }
      50% { transform: scale(1.12); opacity: 0.95; }
      100% { transform: scale(0.92); opacity: 0.55; }
    }
    .glow-aura {
      animation: pulse-glow 4.5s ease-in-out infinite;
    }

    @keyframes shimmer-sweep {
      0% { transform: translateX(-150%) rotate(25deg); }
      35% { transform: translateX(250%) rotate(25deg); }
      100% { transform: translateX(250%) rotate(25deg); }
    }
    .shimmer-btn {
      position: relative;
      overflow: hidden;
    }
    .shimmer-btn::after {
      content: '';
      position: absolute;
      top: -100%;
      left: -100%;
      width: 60%;
      height: 300%;
      background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.45), transparent);
      animation: shimmer-sweep 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }

    /* Frosted Glass */
    .glass-card {
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.16);
    }

    /* Ambient Hero Background */
    .hero-library-bg {
      background-image: 
        radial-gradient(circle at 80% 30%, rgba(245, 158, 11, 0.22) 0%, transparent 50%),
        radial-gradient(circle at 20% 70%, rgba(201, 33, 39, 0.28) 0%, transparent 60%),
        linear-gradient(135deg, rgba(45, 4, 7, 0.93) 0%, rgba(110, 18, 22, 0.88) 45%, rgba(22, 3, 5, 0.96) 100%),
        url('assets/hero-bookstore-bg.jpg');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }

    /* Print Styles for Order Invoice */
    @media print {
      body {
        background: white !important;
        color: black !important;
      }
      #storeHeader, #storeFooter, #cartDrawer, #quickViewModal, button, .no-print {
        display: none !important;
      }
      #view-order-success {
        display: block !important;
        max-width: 100% !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
      }
    }
"""
rendered_html = rendered_html.replace('</style>', micro_css + '\n  </style>')

# Mark IDs on storeMain, storeFooter
rendered_html = rendered_html.replace(
    '<main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 py-5 space-y-8">',
    '<main id="storeMain" class="flex-1 max-w-7xl mx-auto w-full px-3 sm:px-6 py-4 sm:py-5 space-y-8 overflow-hidden">'
)
rendered_html = rendered_html.replace(
    '<footer class="bg-[#1C1917] text-gray-300 pt-12 pb-6 border-t border-gray-800">',
    '<footer id="storeFooter" class="bg-[#1C1917] text-gray-300 pt-12 pb-6 border-t border-gray-800 w-full overflow-hidden">'
)

# 3. COMPLETE MASTER HEADER REPLACEMENT
# Fix 1: Exact crisp logo (logo-header.png)
# Fix 3: DANH MỤC SẢN PHẨM Mega menu dropdown is fully visible (removed overflow-hidden from storeHeader & taskbar)
master_header_html = """
  <!-- STORE HEADER (CHUẨN UI/UX: LOGO CHUẨN ĐẸP, TÌM KIẾM + YÊU THÍCH, TASKBAR TƯƠNG TÁC SÁNG VÀNG, MEGA MENU CLICK CHUẨN) -->
  <header id="storeHeader" class="bg-white sticky top-0 z-40 border-b border-gray-200 shadow-sm w-full max-w-full">
    <!-- Utility top bar (desktop) -->
    <div class="bg-stone-50 border-b border-gray-100 text-[11px] text-gray-500 py-1 px-4 hidden sm:block">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <span class="flex items-center gap-1"><span class="material-symbols-outlined text-xs text-brand-red">call</span> Hotline: <strong>0933.543.987</strong></span>
          <span class="flex items-center gap-1"><span class="material-symbols-outlined text-xs text-emerald-600">local_shipping</span> Miễn phí vận chuyển toàn quốc cho đơn từ 250.000 đ</span>
        </div>
        <div class="flex items-center gap-4 text-[10px]">
          <a href="javascript:void(0)" onclick="showView('content', 'chinh-sach-giao-hang')" class="hover:text-brand-red">Chính sách giao hàng</a>
          <a href="javascript:void(0)" onclick="showView('content', 'chinh-sach-doi-tra')" class="hover:text-brand-red">Chính sách đổi trả</a>
          <a href="javascript:void(0)" onclick="showView('content', 'lien-he')" class="hover:text-brand-red">Liên hệ hỗ trợ</a>
        </div>
      </div>
    </div>

    <!-- Main Header Bar -->
    <div class="max-w-7xl mx-auto px-3 sm:px-4 py-2 sm:py-2.5">
      <div class="flex items-center justify-between gap-2 sm:gap-4">
        
        <!-- Logo Brand: Logo chuẩn DuwcsAnhLib -->
        <a href="javascript:void(0)" onclick="enterStore()" class="flex items-center gap-2 shrink-0 cursor-pointer group" title="DuwcsAnhLib - Hiệu Sách &amp; Thư Viện Tri Thức">
          <img src="assets/logo-header.png" alt="DuwcsAnhLib" class="h-10 sm:h-12 w-auto object-contain group-hover:opacity-90 transition">
        </a>

        <!-- Search Bar with Category Filter (Desktop) -->
        <div class="hidden md:flex flex-1 max-w-xl mx-2 lg:mx-6">
          <div class="relative flex items-center w-full rounded-lg border-2 border-brand-red overflow-hidden shadow-inner bg-white">
            <select id="headerCategorySelect" onchange="syncSearchCategory(this.value)" class="bg-gray-50 text-xs font-semibold text-gray-700 px-3 py-2 border-r border-gray-200 outline-none cursor-pointer">
              <option value="All">Tất cả danh mục</option>
              <option value="Văn học">Văn học</option>
              <option value="Kinh tế">Kinh tế</option>
              <option value="Tâm lý">Tâm lý</option>
              <option value="Kỹ năng">Kỹ năng</option>
              <option value="Thiếu nhi">Thiếu nhi</option>
            </select>
            <input type="text" id="headerSearchInput" oninput="syncSearchQuery(this.value)" onkeyup="if(event.key==='Enter') handleSearch()" placeholder="Tìm kiếm tựa sách, tác giả, ISBN, Nhà xuất bản..." class="flex-1 px-3 py-2 text-xs text-gray-800 placeholder-gray-400 focus:outline-none min-w-0">
            <button onclick="handleSearch()" class="bg-brand-red hover:bg-red-700 text-white px-5 py-2 flex items-center justify-center transition cursor-pointer shrink-0" title="Tìm kiếm">
              <span class="material-symbols-outlined text-lg">search</span>
            </button>
          </div>
        </div>

        <!-- Right Action Buttons: Wishlist & Cart -->
        <div class="flex items-center gap-2 sm:gap-3 shrink-0">
          
          <!-- Wishlist Button -->
          <button id="headerWishlistBtn" onclick="openWishlistDrawer()" class="flex items-center gap-1.5 px-2.5 sm:px-3 py-2 rounded-lg hover:bg-gray-100 transition text-gray-700 cursor-pointer" title="Danh sách yêu thích">
            <span class="material-symbols-outlined text-xl text-brand-red">favorite</span>
            <span class="text-xs font-semibold hidden lg:inline">Yêu thích</span>
            <span id="wishlistCountBadge" class="w-4 h-4 rounded-full bg-brand-red text-white text-[10px] flex items-center justify-center font-bold">3</span>
          </button>

          <!-- Cart Button -->
          <button id="headerCartBtn" onclick="openCart()" class="flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3.5 py-2 rounded-lg bg-red-50 hover:bg-red-100 border border-red-200 transition text-brand-red cursor-pointer shadow-sm">
            <div class="relative">
              <span class="material-symbols-outlined text-xl">shopping_cart</span>
              <span id="cartCountBadge" class="absolute -top-1.5 -right-2 bg-brand-red text-white text-[10px] font-black rounded-full h-4 w-4 flex items-center justify-center">0</span>
            </div>
            <div class="text-left hidden sm:block">
              <div class="text-[9px] uppercase font-bold text-gray-500 leading-tight">GIỎ HÀNG</div>
              <div id="headerCartTotal" class="text-xs font-black text-brand-red leading-tight">0 đ</div>
            </div>
          </button>
        </div>

      </div>

      <!-- Mobile Search Bar -->
      <div class="mt-2.5 block md:hidden w-full">
        <div class="relative flex items-center rounded-lg border-2 border-brand-red overflow-hidden shadow-inner bg-white w-full">
          <select id="mobileCategorySelect" onchange="syncSearchCategory(this.value)" class="bg-gray-50 text-[11px] font-semibold text-gray-700 px-2 py-2 border-r border-gray-200 outline-none cursor-pointer max-w-[110px] truncate">
            <option value="All">Tất cả</option>
            <option value="Văn học">Văn học</option>
            <option value="Kinh tế">Kinh tế</option>
            <option value="Tâm lý">Tâm lý</option>
            <option value="Kỹ năng">Kỹ năng</option>
            <option value="Thiếu nhi">Thiếu nhi</option>
          </select>
          <input type="text" id="mobileSearchInput" oninput="syncSearchQuery(this.value)" onkeyup="if(event.key==='Enter') handleSearch()" placeholder="Tìm kiếm sách, tác giả..." class="w-full px-2.5 py-2 text-xs text-gray-800 placeholder-gray-400 focus:outline-none min-w-0">
          <button onclick="handleSearch()" class="bg-brand-red hover:bg-red-700 text-white px-3.5 py-2 flex items-center justify-center transition cursor-pointer shrink-0" title="Tìm kiếm">
            <span class="material-symbols-outlined text-base">search</span>
          </button>
        </div>
      </div>
    </div>

    <!-- SUB NAVIGATION TASKBAR (Z-INDEX 30, NO OVERFLOW-HIDDEN ĐỂ DROPDOWN KHÔNG BỊ CẮT) -->
    <div class="bg-brand-red text-white text-xs font-bold uppercase tracking-wider w-full relative z-30">
      <div class="max-w-7xl mx-auto px-2 sm:px-4 flex items-center justify-between w-full min-w-0">
        <div class="flex items-center w-full min-w-0">
          
          <!-- Category Mega Menu Toggle (Clickable Button + Dropdown + Arrow Animation) -->
          <div class="relative shrink-0" id="categoryMegaMenuWrapper">
            <button id="categoryMegaMenuBtn" onclick="toggleCategoryMegaMenu(event)" class="bg-[#A5181D] hover:bg-black/30 py-3 px-3 sm:px-4 flex items-center gap-1.5 sm:gap-2 cursor-pointer transition select-none text-white font-bold border-b-2 border-transparent">
              <span class="material-symbols-outlined text-base sm:text-lg">menu</span>
              <span class="text-[11px] sm:text-xs">DANH MỤC SẢN PHẨM</span>
              <span id="categoryMegaMenuArrow" class="material-symbols-outlined text-sm opacity-80 transition-transform duration-200">expand_more</span>
            </button>
            
            <!-- Dropdown Menu: Đầy đủ 6 lựa chọn thể loại + Tất cả -->
            <div id="categoryMegaMenuDropdown" class="hidden absolute left-0 top-full w-64 bg-white text-gray-800 shadow-2xl border border-gray-200 rounded-b-xl py-2 z-50">
              <div onclick="selectCategoryFromMenu('All')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-bold text-xs border-b border-gray-100 text-brand-red">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-brand-red">menu_book</span>
                  Tất Cả Sản Phẩm
                </span>
                <span class="text-[10px] bg-red-100 text-brand-red px-1.5 py-0.5 rounded font-mono font-bold">25</span>
              </div>
              <div onclick="selectCategoryFromMenu('Văn học')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-brand-red">auto_stories</span>
                  Văn học &amp; Tản văn
                </span>
                <span class="text-[10px] bg-red-100 text-brand-red px-1.5 py-0.5 rounded font-mono font-bold">5</span>
              </div>
              <div onclick="selectCategoryFromMenu('Kinh tế')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-emerald-600">trending_up</span>
                  Kinh tế &amp; Kinh doanh
                </span>
                <span class="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-mono font-bold">5</span>
              </div>
              <div onclick="selectCategoryFromMenu('Tâm lý')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-purple-600">psychology</span>
                  Tâm lý &amp; Đời sống
                </span>
                <span class="text-[10px] bg-purple-100 text-purple-800 px-1.5 py-0.5 rounded font-mono font-bold">5</span>
              </div>
              <div onclick="selectCategoryFromMenu('Kỹ năng')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs border-b border-gray-100">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-orange-600">lightbulb</span>
                  Kỹ năng phát triển
                </span>
                <span class="text-[10px] bg-orange-100 text-orange-800 px-1.5 py-0.5 rounded font-mono font-bold">5</span>
              </div>
              <div onclick="selectCategoryFromMenu('Thiếu nhi')" class="px-4 py-2.5 hover:bg-red-50 hover:text-brand-red flex items-center justify-between cursor-pointer transition font-semibold text-xs">
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-base text-blue-600">child_care</span>
                  Sách Thiếu nhi
                </span>
                <span class="text-[10px] bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded font-mono font-bold">5</span>
              </div>
            </div>
          </div>

          <!-- Horizontal Nav Links: Tất cả 6 box đều có ID, hover vàng, active vàng rực rỡ + underline vàng -->
          <div class="flex items-center overflow-x-auto whitespace-nowrap scrollbar-none text-xs min-w-0 flex-1">
            <button onclick="navClick('home')" id="nav-btn-home" class="py-3 px-3 sm:px-4 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1.5 cursor-pointer border-b-2 border-transparent shrink-0">
              <span class="material-symbols-outlined text-base">storefront</span>
              <span>Cửa Hàng</span>
            </button>
            <button onclick="navClick('shop')" id="nav-btn-shop" class="py-3 px-3 sm:px-4 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1 cursor-pointer border-b-2 border-transparent shrink-0">
              <span class="material-symbols-outlined text-base">menu_book</span>
              <span>Tất Cả</span>
            </button>
            <button onclick="navClick('flashsale')" id="nav-btn-flashsale" class="py-3 px-3 sm:px-3.5 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1 cursor-pointer border-b-2 border-transparent shrink-0">
              <span class="material-symbols-outlined text-base text-yellow-300">bolt</span>
              <span>Flash Sale</span>
            </button>
            <button onclick="navClick('bestseller')" id="nav-btn-bestseller" class="py-3 px-3 sm:px-3.5 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1 cursor-pointer border-b-2 border-transparent shrink-0">
              <span>Sách Bán Chạy</span>
            </button>
            <button onclick="navClick('blogs')" id="nav-btn-blogs" class="py-3 px-3 sm:px-3.5 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1 cursor-pointer border-b-2 border-transparent shrink-0">
              <span>Góc Đọc &amp; Review</span>
            </button>
            <button onclick="navClick('gioithieu')" id="nav-btn-gioithieu" class="py-3 px-3 sm:px-3.5 hover:bg-black/25 hover:text-amber-300 text-white font-bold transition flex items-center gap-1 cursor-pointer border-b-2 border-transparent shrink-0">
              <span>Về DuwcsAnhLib</span>
            </button>
          </div>
        </div>

        <div class="hidden xl:flex items-center text-[11px] text-amber-200 gap-1.5 font-bold shrink-0 pl-3">
          <span class="material-symbols-outlined text-sm">verified</span>
          <span>100% Ấn Bản Chính Thức NXB Trẻ</span>
        </div>
      </div>
    </div>
  </header>
"""

header_pattern = r'<header class="bg-white sticky top-0 z-40 border-b border-gray-200 shadow-sm">[\s\S]*?</header>'
header_match = re.search(header_pattern, rendered_html)
if not header_match:
    raise ValueError("Could not find original header in rendered_html")

full_header_and_landing = landing_view_html + "\n" + master_header_html
rendered_html = rendered_html[:header_match.start()] + full_header_and_landing + rendered_html[header_match.end():]

# 4. Insert Flatsome Checkout View & Order Success View inside <main id="storeMain">
main_end_pos = rendered_html.find('</main>')
if main_end_pos == -1:
    raise ValueError("Could not find </main> in rendered_html")

rendered_html = rendered_html[:main_end_pos] + "\n" + CHECKOUT_VIEW_HTML + "\n  " + rendered_html[main_end_pos:]

# 5. Update Cart Drawer Checkout Button
drawer_checkout_old = r'<div id="checkoutFormBlock" class="space-y-2">[\s\S]*?Xác Nhận Đặt Hàng \(Thanh Toán Khi Nhận Sách - COD\)[\s\S]*?</button>\s*</div>'
drawer_checkout_new = """<div class="space-y-2.5">
          <button onclick="closeCart(); showView('checkout');" class="w-full py-3.5 bg-brand-red hover:bg-red-700 text-white font-black rounded-xl text-xs uppercase tracking-wider shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer">
            <span class="material-symbols-outlined text-base">payments</span>
            <span>Tiến Hành Thanh Toán (Flatsome Checkout)</span>
          </button>
          <div class="text-center">
            <button onclick="document.getElementById('drawerQuickCheckoutToggle').classList.toggle('hidden')" class="text-[11px] text-gray-500 hover:text-brand-red underline cursor-pointer">
              Hoặc đặt nhanh tại giỏ hàng &darr;
            </button>
          </div>
          <div id="drawerQuickCheckoutToggle" class="hidden space-y-2 pt-2 border-t border-gray-100">
            <input type="text" id="custName" placeholder="Họ và tên người nhận" value="Nguyễn Văn A" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
            <input type="text" id="custPhone" placeholder="Số điện thoại" value="0933543987" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
            <input type="text" id="custAddress" placeholder="Địa chỉ giao sách" value="Khu dân cư / Văn phòng làm việc" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs outline-none">
            <button onclick="processCheckout()" class="w-full py-2.5 bg-stone-800 hover:bg-black text-white font-bold rounded-xl text-xs uppercase tracking-wider transition cursor-pointer">
              Xác Nhận Đặt Nhanh (COD)
            </button>
          </div>
        </div>"""

rendered_html, drawer_subs = re.subn(drawer_checkout_old, drawer_checkout_new, rendered_html)

# 6. Update Product Card HTML
new_card_func = """function createProductCardHTML(p, isFlashSale = false) {
      const reg = parseInt(p['Regular price'] || 0);
      const sale = parseInt(p['Sale price'] || reg);
      const discountPct = reg > sale ? Math.round(((reg - sale) / reg) * 100) : 0;
      const sku = p['SKU'];
      const coverSrc = `assets/covers/${sku}.png`;
      const isLiked = wishlist.includes(sku);
      const sold = parseInt(p['Custom field: sales_count'] || '18');

      return `
        <div class="group relative bg-white border border-gray-200 rounded-xl p-2.5 sm:p-3 hover:shadow-xl hover:border-red-300 transition-all duration-300 flex flex-col justify-between overflow-hidden">
          
          <!-- Badges & Wishlist -->
          <div class="relative w-full aspect-[3/4] bg-stone-100 rounded-lg overflow-hidden flex items-center justify-center">
            ${discountPct > 0 ? `
              <span class="absolute top-2 left-2 bg-brand-red text-white text-[10px] sm:text-xs font-black px-1.5 py-0.5 rounded shadow z-10">-${discountPct}%</span>
            ` : ''}
            
            <button onclick="toggleWishlist('${sku}')" class="absolute top-2 right-2 w-7 h-7 rounded-full bg-white/90 hover:bg-white text-gray-400 hover:text-brand-red shadow flex items-center justify-center transition z-10 cursor-pointer" title="Yêu thích">
              <span class="material-symbols-outlined text-sm ${isLiked ? 'text-brand-red fill-icon' : ''}">favorite</span>
            </button>

            <!-- Book Cover Image with hover zoom -->
            <img src="${coverSrc}" alt="${p['Name']}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 cursor-pointer" onclick="showView('product', '${sku}')" loading="lazy">
            
            <!-- Quick View Overlay Button -->
            <div class="absolute inset-x-0 bottom-0 p-2 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex justify-center">
              <button onclick="openQuickView('${sku}')" class="w-full py-1.5 bg-white hover:bg-brand-red text-gray-800 hover:text-white rounded-md text-[11px] font-bold shadow transition flex items-center justify-center gap-1 cursor-pointer">
                <span class="material-symbols-outlined text-xs">visibility</span>
                <span>Xem Nhanh</span>
              </button>
            </div>
          </div>

          <!-- Card Content -->
          <div class="pt-2 flex-1 flex flex-col justify-between">
            <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider truncate">${p['Attribute 1 value(s)']}</div>
            <h3 class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition line-clamp-2 leading-snug cursor-pointer h-8" onclick="showView('product', '${sku}')" title="${p['Name']}">
              ${p['Name']}
            </h3>
            
            <!-- Star Ratings -->
            <div class="flex items-center gap-0.5 text-amber-400 text-xs pt-0.5">
              <span class="material-symbols-outlined text-xs fill-icon">star</span>
              <span class="material-symbols-outlined text-xs fill-icon">star</span>
              <span class="material-symbols-outlined text-xs fill-icon">star</span>
              <span class="material-symbols-outlined text-xs fill-icon">star</span>
              <span class="material-symbols-outlined text-xs fill-icon">star</span>
              <span class="text-gray-400 text-[10px] ml-1">(${p.reviews_count || 24})</span>
            </div>

            <!-- Price -->
            <div class="flex items-baseline gap-2 pt-0.5">
              <span class="text-sm sm:text-base font-black text-brand-red">${formatVND(sale)}</span>
              ${reg > sale ? `<span class="text-[11px] text-gray-400 line-through">${formatVND(reg)}</span>` : ''}
            </div>

            ${isFlashSale ? `
              <div class="pt-1">
                <div class="w-full bg-red-100 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-brand-red h-full" style="width: ${Math.min(100, sold * 2)}%"></div>
                </div>
                <div class="text-[10px] text-brand-red font-bold mt-0.5">Đã bán ${sold} cuốn</div>
              </div>
            ` : ''}
          </div>

          <!-- Add to Cart Button (Always Visible) -->
          <button onclick="addToCart('${sku}')" class="mt-2.5 w-full py-1.5 bg-red-50 hover:bg-brand-red text-brand-red hover:text-white border border-red-200 hover:border-brand-red rounded-lg text-xs font-bold transition flex items-center justify-center gap-1 cursor-pointer">
            <span class="material-symbols-outlined text-sm">shopping_cart</span>
            <span>Thêm giỏ hàng</span>
          </button>
        </div>
      `;
    }"""

rendered_html, card_subs = re.subn(
    r"function createProductCardHTML\(p, isFlashSale = false\) \{[\s\S]*?return `[\s\S]*?`;\s*\}",
    new_card_func,
    rendered_html
)

# 7. Update buyNowDetail to directly open Flatsome Checkout
buy_now_old = r"function buyNowDetail\(sku\) \{[\s\S]*?openCart\(\);\s*\}"
buy_now_new = """function buyNowDetail(sku) {
      addDetailToCart(sku);
      closeCart();
      showView('checkout');
    }"""
rendered_html, buy_now_subs = re.subn(buy_now_old, buy_now_new, rendered_html)

# 8. MASTER JAVASCRIPT CONTROLLERS
new_master_controllers = f"""
    // === CATEGORY MEGA MENU CONTROLLERS ===
    function toggleCategoryMegaMenu(event) {{
      if (event) {{
        event.stopPropagation();
      }}
      const dropdown = document.getElementById('categoryMegaMenuDropdown');
      const arrow = document.getElementById('categoryMegaMenuArrow');
      if (!dropdown) return;
      const isHidden = dropdown.classList.contains('hidden');
      if (isHidden) {{
        dropdown.classList.remove('hidden');
        dropdown.style.display = 'block';
        if (arrow) arrow.style.transform = 'rotate(180deg)';
      }} else {{
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
        if (arrow) arrow.style.transform = 'rotate(0deg)';
      }}
    }}

    function selectCategoryFromMenu(cat) {{
      const dropdown = document.getElementById('categoryMegaMenuDropdown');
      const arrow = document.getElementById('categoryMegaMenuArrow');
      if (dropdown) {{
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
      }}
      if (arrow) arrow.style.transform = 'rotate(0deg)';
      
      showView('shop');
      filterCatAndShow(cat);
      setActiveNavButton('shop');
    }}

    // Close Mega Menu when clicking outside
    document.addEventListener('click', function(e) {{
      const wrapper = document.getElementById('categoryMegaMenuWrapper');
      const dropdown = document.getElementById('categoryMegaMenuDropdown');
      const arrow = document.getElementById('categoryMegaMenuArrow');
      if (wrapper && dropdown && !wrapper.contains(e.target)) {{
        dropdown.classList.add('hidden');
        dropdown.style.display = 'none';
        if (arrow) arrow.style.transform = 'rotate(0deg)';
      }}
    }});

    // === TASKBAR INTERACTION & GOLDEN HIGHLIGHTS ===
    function setActiveNavButton(item) {{
      const allNavs = ['home', 'shop', 'flashsale', 'bestseller', 'blogs', 'gioithieu'];
      allNavs.forEach(k => {{
        const btn = document.getElementById('nav-btn-' + k);
        if (btn) {{
          if (k === item) {{
            btn.classList.add('bg-black/30', 'text-amber-300', 'font-extrabold', 'border-b-2', 'border-amber-300');
            btn.classList.remove('text-white', 'border-transparent');
          }} else {{
            btn.classList.remove('bg-black/30', 'text-amber-300', 'font-extrabold', 'border-b-2', 'border-amber-300');
            btn.classList.add('text-white', 'border-transparent');
          }}
        }}
      }});
    }}

    function navClick(item) {{
      setActiveNavButton(item);
      if (item === 'home') {{
        showView('home');
      }} else if (item === 'shop') {{
        showView('shop');
        filterCatAndShow('All');
      }} else if (item === 'flashsale') {{
        showView('home');
        setTimeout(() => scrollToSection('flashsale-section'), 80);
      }} else if (item === 'bestseller') {{
        showView('home');
        switchTabContent('bestseller');
        setTimeout(() => scrollToSection('tab-products-section'), 80);
      }} else if (item === 'blogs') {{
        showView('blogs');
      }} else if (item === 'gioithieu') {{
        showView('content', 'gioi-thieu');
      }}
    }}

    // === SYNC SEARCH CONTROLLERS (DESKTOP + MOBILE) ===
    function syncSearchCategory(cat) {{
      const desktop = document.getElementById('headerCategorySelect');
      const mobile = document.getElementById('mobileCategorySelect');
      if (desktop) desktop.value = cat;
      if (mobile) mobile.value = cat;
      handleSearch();
    }}

    function syncSearchQuery(query) {{
      const desktop = document.getElementById('headerSearchInput');
      const mobile = document.getElementById('mobileSearchInput');
      if (desktop) desktop.value = query;
      if (mobile) mobile.value = query;
      handleSearch();
    }}

    function handleSearch() {{
      const desktopInput = document.getElementById('headerSearchInput');
      const mobileInput = document.getElementById('mobileSearchInput');
      const query = (desktopInput?.value || mobileInput?.value || '').trim().toLowerCase();
      
      const desktopCat = document.getElementById('headerCategorySelect')?.value || 'All';
      const mobileCat = document.getElementById('mobileCategorySelect')?.value || 'All';
      const cat = desktopCat !== 'All' ? desktopCat : mobileCat;

      showView('shop');
      setActiveNavButton('shop');
      filterFullCatalog(query, cat);
    }}

    function handleHeaderCategory() {{
      handleSearch();
    }}

    function handleSidebarFilter() {{
      const selectedCatEl = document.querySelector('input[name="catFilter"]:checked');
      const selectedPriceEl = document.querySelector('input[name="priceRange"]:checked');
      const selectedCat = selectedCatEl ? selectedCatEl.value : 'All';
      const selectedPrice = selectedPriceEl ? selectedPriceEl.value : 'all';
      filterFullCatalog('', selectedCat, selectedPrice);
    }}

    function handleSort() {{
      handleSidebarFilter();
    }}

    function filterFullCatalog(q = '', cat = 'All', priceRange = 'all') {{
      let filtered = [...allProducts];

      if (cat !== 'All') {{
        filtered = filtered.filter(p => p['Categories'].includes(cat));
      }}
      if (q) {{
        filtered = filtered.filter(p => 
          p['Name'].toLowerCase().includes(q) || 
          p['Attribute 1 value(s)'].toLowerCase().includes(q) ||
          p['SKU'].toLowerCase().includes(q)
        );
      }}
      if (priceRange === 'under70') {{
        filtered = filtered.filter(p => parseInt(p['Sale price']) < 70000);
      }} else if (priceRange === '70to100') {{
        filtered = filtered.filter(p => {{
          const pr = parseInt(p['Sale price']);
          return pr >= 70000 && pr <= 100000;
        }});
      }} else if (priceRange === 'above100') {{
        filtered = filtered.filter(p => parseInt(p['Sale price']) > 100000);
      }}

      // Sort
      const sortType = document.getElementById('sortBy') ? document.getElementById('sortBy').value : 'featured';
      if (sortType === 'price-low') {{
        filtered.sort((a, b) => parseInt(a['Sale price']) - parseInt(b['Sale price']));
      }} else if (sortType === 'price-high') {{
        filtered.sort((a, b) => parseInt(b['Sale price']) - parseInt(a['Sale price']));
      }} else if (sortType === 'name-az') {{
        filtered.sort((a, b) => a['Name'].localeCompare(b['Name']));
      }}

      // Update counter
      const countEl = document.getElementById('fullCatalogCount');
      if (countEl) countEl.textContent = `${{filtered.length}} Sản phẩm`;

      // Render cards
      const container = document.getElementById('fullCatalogGrid');
      if (container) {{
        if (filtered.length === 0) {{
          container.innerHTML = `
            <div class="col-span-full py-16 text-center text-gray-500 bg-white rounded-2xl border border-gray-200 p-8 space-y-3">
              <span class="material-symbols-outlined text-5xl text-brand-red">menu_book</span>
              <p class="font-bold text-sm text-gray-700">Không tìm thấy ấn bản sách phù hợp.</p>
              <p class="text-xs text-gray-400">Vui lòng thử từ khóa khác hoặc bấm nút bên dưới để xem toàn bộ danh mục.</p>
              <button onclick="filterCatAndShow('All')" class="px-5 py-2 bg-brand-red text-white text-xs font-bold rounded-lg hover:bg-red-700 transition cursor-pointer">Xem Tất Cả 25 Sách</button>
            </div>
          `;
        }} else {{
          container.innerHTML = filtered.map(p => createProductCardHTML(p, false)).join('');
        }}
      }}
    }}

    function filterCatAndShow(cat) {{
      const radios = document.querySelectorAll('input[name="catFilter"]');
      radios.forEach(r => {{
        if (r.value === cat) r.checked = true;
      }});
      
      const deskCat = document.getElementById('headerCategorySelect');
      const mobCat = document.getElementById('mobileCategorySelect');
      if (deskCat) deskCat.value = (cat === 'All' ? 'All' : cat);
      if (mobCat) mobCat.value = (cat === 'All' ? 'All' : cat);

      filterFullCatalog('', cat);
    }}

    // === MASTER VIEW CONTROLLER ===
    // Hỗ trợ đầy đủ: 'landing', 'home', 'shop', 'content', 'blogs', 'product', 'checkout', 'order-success'
    function showView(viewName, contentKey) {{
      const views = ['landing', 'home', 'shop', 'content', 'blogs', 'product', 'checkout', 'order-success'];
      views.forEach(v => {{
        const el = document.getElementById('view-' + v);
        if (el) {{
          el.classList.add('hidden');
          el.style.display = 'none';
        }}
      }});

      const target = document.getElementById('view-' + viewName);
      if (target) {{
        target.classList.remove('hidden');
        target.style.display = 'block';
      }}
      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      // Toggle Store Header, Main, Footer visibility
      const storeHeader = document.getElementById('storeHeader');
      const storeMain = document.getElementById('storeMain');
      const storeFooter = document.getElementById('storeFooter');

      if (viewName === 'landing') {{
        if (storeHeader) storeHeader.style.display = 'none';
        if (storeMain) storeMain.style.display = 'none';
        if (storeFooter) storeFooter.style.display = 'none';
      }} else {{
        if (storeHeader) storeHeader.style.display = 'block';
        if (storeMain) storeMain.style.display = 'block';
        if (storeFooter) storeFooter.style.display = 'block';
      }}

      // Update nav button active highlights
      if (viewName === 'home') {{
        setActiveNavButton('home');
      }} else if (viewName === 'shop') {{
        setActiveNavButton('shop');
        handleSidebarFilter();
      }} else if (viewName === 'blogs') {{
        setActiveNavButton('blogs');
      }} else if (viewName === 'content' && contentKey === 'gioi-thieu') {{
        setActiveNavButton('gioithieu');
        renderContent(contentKey);
      }} else if (viewName === 'content' && contentKey) {{
        renderContent(contentKey);
      }} else if (viewName === 'product' && contentKey) {{
        renderProductDetail(contentKey);
      }} else if (viewName === 'checkout') {{
        renderCheckoutPage();
      }}
    }}

    // Khi người dùng bấm vào cửa hàng từ Landingpage: ghi nhớ phiên và mở Cửa Hàng
    function enterStore(cat) {{
      try {{
        sessionStorage.setItem('duwcsanhlib_entered_store', '1');
        localStorage.removeItem('duwcsanhlib_visited'); // Xóa cờ cũ
      }} catch(e) {{}}
      
      if (cat && cat !== 'All') {{
        showView('shop');
        filterCatAndShow(cat);
        setActiveNavButton('shop');
      }} else if (cat === 'All') {{
        showView('shop');
        filterCatAndShow('All');
        setActiveNavButton('shop');
      }} else {{
        // Trang đầu tiên trong cửa hàng là "Cửa Hàng" (view-home)
        showView('home');
        setActiveNavButton('home');
      }}
    }}

    {CHECKOUT_JS}
"""

controller_pattern = r"function handleSearch\(\) \{[\s\S]*?renderProductDetail\(contentKey\);\s*\}\s*\}"
rendered_html, show_view_subs = re.subn(
    controller_pattern,
    new_master_controllers,
    rendered_html
)

# 9. Update updateCartUI to sync with Checkout Page
update_cart_hook = """      // Sync with full Flatsome Checkout view if visible
      const checkoutEl = document.getElementById('view-checkout');
      if (checkoutEl && !checkoutEl.classList.contains('hidden') && typeof renderCheckoutPage === 'function') {
        renderCheckoutPage();
      }
    }"""
rendered_html = re.sub(
    r"(function updateCartUI\(\) \{[\s\S]*?container\.innerHTML = cart\.map[\s\S]*?`\)\.join\(''\);\s*)(\})",
    r"\1" + "\n" + update_cart_hook,
    rendered_html
)

# 10. Update Initial Load block
# Fix 2: Landing page ALWAYS appears on first visit (fresh session), or when visiting landing.html / ?view=landing
initial_load_block = """      // Initial load: Landingpage hiện vào lần đầu tiên mở trang web trong phiên
      try {
        localStorage.removeItem('duwcsanhlib_visited'); // Xóa cờ vĩnh viễn cũ để không bị kẹt
      } catch(e) {}

      const urlParams = new URLSearchParams(window.location.search);
      const catParam = urlParams.get('cat');
      const skuParam = urlParams.get('sku');
      const viewParam = urlParams.get('view');
      const pageParam = urlParams.get('page');
      const isLandingPath = window.location.pathname.endsWith('landing.html');
      
      let enteredStore = false;
      try {
        enteredStore = sessionStorage.getItem('duwcsanhlib_entered_store') === '1';
      } catch(e) {}

      if (skuParam) {
        showView('product', skuParam);
      } else if (catParam) {
        showView('shop');
        filterCatAndShow(catParam);
        setActiveNavButton('shop');
      } else if (viewParam === 'checkout') {
        showView('checkout');
      } else if (viewParam === 'order-success') {
        showView('order-success');
      } else if (viewParam === 'shop') {
        showView('shop');
        setActiveNavButton('shop');
      } else if (viewParam === 'home') {
        showView('home');
        setActiveNavButton('home');
      } else if (viewParam === 'landing' || isLandingPath) {
        showView('landing');
      } else if (pageParam) {
        showView('content', pageParam);
      } else if (!enteredStore) {
        // Lần đầu tiên truy cập: Hiện Landing Page sạch đẹp toàn màn hình
        showView('landing');
      } else {
        // Đã từng bấm Khám Phá Cửa Hàng trong phiên này: Vào thẳng "Cửa Hàng" (view-home)
        showView('home');
        setActiveNavButton('home');
      }
      renderFlashSale();
      switchTabContent('bestseller');
      updateWishlistUI();
      updateCartUI();"""

rendered_html, init_subs = re.subn(
    r"// Initial load[\s\S]*?updateCartUI\(\);",
    initial_load_block,
    rendered_html
)

# Save to duwcsanhlib-static-web as index.html, store.html, landing.html
STATIC_DIR = ROOT / "duwcsanhlib-static-web"
(STATIC_DIR / "index.html").write_text(rendered_html, encoding="utf-8")
(STATIC_DIR / "store.html").write_text(rendered_html, encoding="utf-8")
(STATIC_DIR / "landing.html").write_text(rendered_html, encoding="utf-8")

print(f"Master Unified Web Application generated successfully! Size: {len(rendered_html)} bytes")
