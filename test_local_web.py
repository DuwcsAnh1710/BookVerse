"""Ứng dụng Web Hiệu Sách Trực Tuyến DuwcsAnhLib
Sử dụng Google Material Symbols (không dùng generic emoji)
Hotline chính thức: 0933 543 987
Giao diện thương mại điện tử chuyên nghiệp, chuẩn mực.
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

# Load products from CSV
csv_path = DATA_DIR / 'san-pham-duwcsanhlib.csv'
products = []
with csv_path.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        reg = int(row.get('Regular price', 0) or 0)
        sale = int(row.get('Sale price', 0) or 0)
        discount = 0
        if reg > 0 and sale > 0 and sale < reg:
            discount = round((reg - sale) / reg * 100)
        row['discount_pct'] = discount
        row['rating'] = 5.0
        row['reviews_count'] = 18 + (int(row['SKU'].split('-')[-1]) * 7) % 43
        row['sold_count'] = 45 + (int(row['SKU'].split('-')[-1]) * 13) % 95
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
  <title>DuwcsAnhLib — Hiệu Sách & Thư Viện Tri Thức</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Material Symbols -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');
    body { font-family: 'Nunito Sans', sans-serif; background-color: #F0F2F5; color: #1C1C1E; }
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
        <div class="w-11 h-11 rounded-xl bg-brand-red text-white flex items-center justify-center font-black text-xl shadow-md border-2 border-amber-300">
          DA
        </div>
        <div>
          <span class="text-2xl font-black tracking-wider text-brand-red uppercase leading-none block">DuwcsAnh<span class="text-amber-600">Lib</span></span>
          <span class="text-[10px] text-gray-500 font-bold tracking-widest uppercase block mt-0.5">Hiệu Sách & Thư Viện Tri Thức</span>
        </div>
      </div>

      <!-- Smart Search Box -->
      <div class="flex-1 max-w-2xl mx-2 hidden sm:block">
        <div class="relative flex items-center rounded-lg border-2 border-brand-red overflow-hidden shadow-inner bg-white">
          <select id="headerCategorySelect" onchange="handleHeaderCategory()" class="bg-gray-50 text-xs font-semibold text-gray-700 px-3 py-2.5 border-r border-gray-200 outline-none cursor-pointer">
            <option value="All">Tất cả danh mục (25)</option>
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

      <!-- User Actions & Mini Cart -->
      <div class="flex items-center gap-3 shrink-0">
        <!-- Wishlist -->
        <button onclick="alert('Đã lưu 3 tựa sách yêu thích!')" class="p-2 rounded-lg hover:bg-gray-100 text-gray-700 relative hidden md:flex items-center gap-1.5 text-xs font-semibold cursor-pointer">
          <span class="material-symbols-outlined text-gray-600">favorite_border</span>
          <span>Yêu thích</span>
          <span class="w-4 h-4 rounded-full bg-amber-500 text-white text-[10px] flex items-center justify-center font-bold">3</span>
        </button>

        <!-- Dropdown Cart Button -->
        <button onclick="openCart()" class="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-red-50 hover:bg-red-100 border border-red-200 transition text-brand-red cursor-pointer shadow-sm">
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

    <!-- SUB NAVIGATION -->
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
            <button onclick="showView('home')" class="py-3 px-4 hover:bg-black/20 transition flex items-center gap-1">
              <span>Trang chủ</span>
            </button>
            <button onclick="scrollToSection('flashsale-section')" class="py-3 px-4 hover:bg-black/20 text-yellow-300 transition flex items-center gap-1">
              <span class="material-symbols-outlined text-sm text-yellow-300">bolt</span>
              <span>Flash Sale</span>
            </button>
            <button onclick="showView('shop'); filterCatAndShow('Văn học');" class="py-3 px-4 hover:bg-black/20 transition">
              <span>Sách Bán Chạy</span>
            </button>
            <button onclick="showView('shop')" class="py-3 px-4 hover:bg-black/20 transition">
              <span>Tủ Sách Tuyển Chọn (25 Sách)</span>
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
      
      <!-- HERO SHOWCASE: 2/3 SLIDER + 1/3 DUAL BANNERS -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        
        <!-- 2/3 Main Slider Banner -->
        <div class="lg:col-span-2 relative rounded-2xl overflow-hidden bg-gradient-to-r from-red-950 via-brand-red to-amber-900 text-white p-8 sm:p-12 shadow-md flex flex-col justify-between min-h-[320px]">
          <div class="max-w-lg space-y-3 relative z-10">
            <span class="inline-block px-3 py-1 bg-yellow-400 text-stone-900 font-extrabold text-[11px] rounded-full uppercase tracking-wider shadow">
              ƯU ĐÃI ĐỘC QUYỀN DUWCSANHLIB
            </span>
            <h1 class="text-2xl sm:text-4xl font-extrabold serif-title leading-tight">
              Hội Sách Tri Thức 2026:<br><span class="text-yellow-300">Giảm Đến 30% Tất Cả Ấn Bản</span>
            </h1>
            <p class="text-red-100 text-xs sm:text-sm leading-relaxed">
              Trọn bộ 25 tác phẩm văn học, kinh tế, tâm lý, kỹ năng và thiếu nhi chính hãng từ Nhà xuất bản Trẻ. Đóng gói bảo quản kỹ lưỡng, giao nhanh toàn quốc.
            </p>
            <div class="pt-2 flex flex-wrap gap-3">
              <button onclick="showView('shop')" class="px-5 py-2.5 bg-yellow-400 hover:bg-yellow-300 text-stone-950 font-bold rounded-lg text-xs shadow-md transition cursor-pointer uppercase">
                Khám Phá Toàn Bộ Sách
              </button>
              <button onclick="scrollToSection('flashsale-section')" class="px-5 py-2.5 bg-white/20 hover:bg-white/30 text-white font-bold rounded-lg text-xs border border-white/30 transition cursor-pointer flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">bolt</span>
                <span>Xem Flash Sale</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 1/3 Dual Promo Banners -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-4">
          <!-- Promo 1 -->
          <div onclick="filterCatAndShow('Kinh tế')" class="rounded-2xl p-5 bg-gradient-to-br from-emerald-800 to-teal-950 text-white flex flex-col justify-between shadow-sm cursor-pointer hover:shadow-md transition group">
            <div>
              <span class="text-[10px] font-bold bg-emerald-500 text-white px-2 py-0.5 rounded uppercase">Tủ Sách Khởi Nghiệp</span>
              <h3 class="font-bold text-base mt-2 group-hover:text-yellow-300 transition">Kinh Tế & Lãnh Đạo 4.0</h3>
              <p class="text-xs text-emerald-200 mt-1">Đúc kết bài học thực chiến từ các chuyên gia hàng đầu.</p>
            </div>
            <div class="text-xs font-bold text-yellow-300 mt-3 flex items-center gap-1">
              <span>Xem tuyển tập</span>
              <span class="material-symbols-outlined text-xs">arrow_forward</span>
            </div>
          </div>

          <!-- Promo 2 -->
          <div onclick="filterCatAndShow('Tâm lý')" class="rounded-2xl p-5 bg-gradient-to-br from-purple-900 to-indigo-950 text-white flex flex-col justify-between shadow-sm cursor-pointer hover:shadow-md transition group">
            <div>
              <span class="text-[10px] font-bold bg-purple-500 text-white px-2 py-0.5 rounded uppercase">Sách Nuôi Dưỡng Tâm Hồn</span>
              <h3 class="font-bold text-base mt-2 group-hover:text-yellow-300 transition">Tâm Lý & Đời Sống</h3>
              <p class="text-xs text-purple-200 mt-1">Khoảng lặng cần thiết giữa nhịp sống bận rộn.</p>
            </div>
            <div class="text-xs font-bold text-yellow-300 mt-3 flex items-center gap-1">
              <span>Khám phá ngay</span>
              <span class="material-symbols-outlined text-xs">arrow_forward</span>
            </div>
          </div>
        </div>

      </div>

      <!-- USP SERVICE FEATURES -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 bg-white p-4 rounded-2xl border border-gray-200 shadow-sm">
        <div class="flex items-center gap-3 p-2">
          <div class="w-10 h-10 rounded-xl bg-red-50 text-brand-red flex items-center justify-center font-bold text-xl shrink-0">
            <span class="material-symbols-outlined text-2xl text-brand-red">local_shipping</span>
          </div>
          <div>
            <div class="font-bold text-xs text-gray-900">Giao Hàng Toàn Quốc</div>
            <div class="text-[11px] text-gray-500">Miễn phí cho đơn từ 250k</div>
          </div>
        </div>
        <div class="flex items-center gap-3 p-2">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-xl shrink-0">
            <span class="material-symbols-outlined text-2xl text-emerald-600">verified</span>
          </div>
          <div>
            <div class="font-bold text-xs text-gray-900">100% Sách Thật</div>
            <div class="text-[11px] text-gray-500">Ấn bản chính thức NXB Trẻ</div>
          </div>
        </div>
        <div class="flex items-center gap-3 p-2">
          <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-xl shrink-0">
            <span class="material-symbols-outlined text-2xl text-amber-600">sync_alt</span>
          </div>
          <div>
            <div class="font-bold text-xs text-gray-900">Đổi Trả Dễ Dàng</div>
            <div class="text-[11px] text-gray-500">Đổi mới trong vòng 7 ngày</div>
          </div>
        </div>
        <div class="flex items-center gap-3 p-2">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-xl shrink-0">
            <span class="material-symbols-outlined text-2xl text-blue-600">support_agent</span>
          </div>
          <div>
            <div class="font-bold text-xs text-gray-900">Hotline: 0933.543.987</div>
            <div class="text-[11px] text-gray-500">Hỗ trợ độc giả 08:00 - 21:00</div>
          </div>
        </div>
      </div>

      <!-- FLASH SALE SECTION -->
      <section id="flashsale-section" class="bg-white rounded-2xl border border-red-200 shadow-md overflow-hidden">
        
        <!-- Header Flash Sale with Countdown -->
        <div class="bg-gradient-to-r from-red-600 via-brand-red to-orange-600 p-4 text-white flex flex-col sm:flex-row items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-2xl text-yellow-300">bolt</span>
            <h2 class="text-xl font-black uppercase tracking-wider">FLASH SALE HÔM NAY</h2>
            <span class="text-xs bg-yellow-400 text-stone-900 font-extrabold px-2 py-0.5 rounded uppercase">Giá Tốt Nhất</span>
          </div>
          
          <!-- Countdown Timer -->
          <div class="flex items-center gap-2 text-xs font-bold">
            <span class="text-white/90">Kết thúc sau:</span>
            <div class="flex items-center gap-1 text-stone-950 font-black">
              <span id="timerHours" class="bg-white px-2 py-1 rounded shadow-sm">02</span> :
              <span id="timerMinutes" class="bg-white px-2 py-1 rounded shadow-sm">45</span> :
              <span id="timerSeconds" class="bg-white px-2 py-1 rounded shadow-sm">18</span>
            </div>
          </div>
        </div>

        <!-- Flash Sale Items Grid -->
        <div id="flashSaleGrid" class="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
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
            <span>Xem tất cả 25 sách</span>
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
            <h2 class="text-xl font-black text-gray-900 uppercase">Sách Tuyển Chọn</h2>
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

    </div>

    <!-- VIEW: FULL SHOP CATALOG (25 BOOKS WITH FILTERS) -->
    <div id="view-shop" class="hidden space-y-6">
      
      <div class="bg-white p-4 rounded-xl border border-gray-200 flex items-center justify-between text-xs">
        <div class="flex items-center gap-1.5 text-gray-500">
          <button onclick="showView('home')" class="hover:text-brand-red">Trang chủ</button>
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
          </div>

          <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <h3 class="font-black text-sm text-gray-900 uppercase border-b border-gray-100 pb-2">Khoảng Giá</h3>
            <div class="space-y-1.5 text-xs">
              <label class="flex items-center gap-2 p-1 cursor-pointer">
                <input type="radio" name="priceRange" value="all" checked onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Tất cả mức giá</span>
              </label>
              <label class="flex items-center gap-2 p-1 cursor-pointer">
                <input type="radio" name="priceRange" value="under70" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Dưới 70.000 đ</span>
              </label>
              <label class="flex items-center gap-2 p-1 cursor-pointer">
                <input type="radio" name="priceRange" value="70to100" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>70.000 đ – 100.000 đ</span>
              </label>
              <label class="flex items-center gap-2 p-1 cursor-pointer">
                <input type="radio" name="priceRange" value="above100" onchange="handleSidebarFilter()" class="text-brand-red">
                <span>Trên 100.000 đ</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Main Products Grid -->
        <div class="lg:col-span-3 space-y-4">
          <div class="bg-white p-3 rounded-xl border border-gray-200 flex items-center justify-between text-xs">
            <div class="text-gray-600">Sắp xếp theo:</div>
            <select id="sortBy" onchange="handleSort()" class="bg-gray-50 border border-gray-300 rounded px-2.5 py-1 text-xs outline-none">
              <option value="featured">Phổ biến nhất</option>
              <option value="price-asc">Giá thấp đến cao</option>
              <option value="price-desc">Giá cao đến thấp</option>
              <option value="discount">Giảm giá nhiều nhất</option>
            </select>
          </div>

          <div id="fullCatalogGrid" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <!-- Populated by JS -->
          </div>
        </div>

      </div>

    </div>

    <!-- VIEW: CONTENT -->
    <div id="view-content" class="hidden max-w-4xl mx-auto bg-white p-6 sm:p-10 rounded-2xl border border-gray-200 shadow-sm space-y-4">
      <button onclick="showView('home')" class="text-xs font-bold text-brand-red hover:underline mb-2 inline-flex items-center gap-1">
        <span class="material-symbols-outlined text-sm">arrow_back</span>
        <span>Quay lại Trang chủ</span>
      </button>
      <div id="contentBody" class="prose max-w-none text-gray-800 leading-relaxed text-sm">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- VIEW: BLOGS / GÓC ĐỌC -->
    <div id="view-blogs" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-gray-200">
        <h2 class="text-2xl font-black text-gray-900">Góc Đọc & Bài Viết DuwcsAnhLib</h2>
        <p class="text-xs text-gray-500 mt-1">Những chia sẻ, tản văn và cảm hứng xây dựng thói quen đọc sách mỗi ngày.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-red-100 text-brand-red uppercase">Thói quen đọc</span>
            <h3 class="text-base font-bold text-gray-900 leading-snug">Khởi đầu ngày mới cùng thói quen đọc 15 phút</h3>
            <p class="text-xs text-gray-600 line-clamp-3">Dành 15 phút mỗi buổi sáng cho một vài trang sách có thể tạo nên sự chuyển biến bất ngờ cho tư duy và tâm trạng của bạn...</p>
          </div>
          <button onclick="showView('content', 'blog-01')" class="text-xs font-bold text-brand-red hover:underline pt-2 inline-flex items-center gap-1">
            <span>Đọc chi tiết</span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </button>
        </div>
        <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 uppercase">Gợi ý tác phẩm</span>
            <h3 class="text-base font-bold text-gray-900 leading-snug">5 tựa sách kinh điển nên có trên giá sách của bạn</h3>
            <p class="text-xs text-gray-600 line-clamp-3">Dù xu hướng đọc có thay đổi theo thời gian, những giá trị nguyên bản trong các tác phẩm văn học kinh điển vẫn luôn giữ nguyên sức hút...</p>
          </div>
          <button onclick="showView('content', 'blog-02')" class="text-xs font-bold text-brand-red hover:underline pt-2 inline-flex items-center gap-1">
            <span>Đọc chi tiết</span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </button>
        </div>
        <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800 uppercase">Phương pháp nuôi dạy</span>
            <h3 class="text-base font-bold text-gray-900 leading-snug">Nghệ thuật chọn sách cho trẻ em theo từng độ tuổi</h3>
            <p class="text-xs text-gray-600 line-clamp-3">Đọc sách cùng con không chỉ giúp bồi đắp vốn từ và trí tưởng tượng mà còn là cầu nối gắn kết tình cảm gia đình...</p>
          </div>
          <button onclick="showView('content', 'blog-03')" class="text-xs font-bold text-brand-red hover:underline pt-2 inline-flex items-center gap-1">
            <span>Đọc chi tiết</span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </button>
        </div>
      </div>
    </div>

  </main>

  <!-- QUICK VIEW MODAL -->
  <div id="quickViewModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-gray-200 p-6 sm:p-8 relative">
      <button onclick="closeQuickView()" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center font-bold text-gray-600 transition cursor-pointer">
        <span class="material-symbols-outlined text-base">close</span>
      </button>
      
      <div id="quickViewBody">
        <!-- Rendered by JS -->
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
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-brand-red text-white flex items-center justify-center font-bold">DA</div>
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
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

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const allProducts = __PRODUCTS_JSON__;
    const allPages = __PAGES_JSON__;
    let cart = [];
    let voucherDiscount = 0;

    function formatVND(num) {
      return new Intl.NumberFormat('vi-VN').format(num) + ' đ';
    }

    // Render Flash Sale Items
    function renderFlashSale() {
      const container = document.getElementById('flashSaleGrid');
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

      return `
        <div class="bg-white rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-xl transition-all duration-300 p-3 flex flex-col justify-between group relative overflow-hidden">
          
          <!-- Discount Badge on Top Left -->
          ${discount > 0 ? `
            <div class="absolute top-2 left-2 z-10 bg-brand-red text-white text-[10px] font-extrabold px-1.5 py-0.5 rounded shadow">
              -${discount}%
            </div>
          ` : ''}

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

          <!-- Add to Cart Button -->
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
      document.getElementById('tabProductsGrid').innerHTML = filtered.map(p => createProductCardHTML(p)).join('');
    }

    // Quick View Modal
    function openQuickView(sku) {
      const p = allProducts.find(x => x['SKU'] === sku);
      if (!p) return;
      const reg = parseInt(p['Regular price'] || 0);
      const sale = parseInt(p['Sale price'] || reg);
      const coverSrc = `/assets/covers/${sku}.png`;
      const modal = document.getElementById('quickViewModal');
      const body = document.getElementById('quickViewBody');

      body.innerHTML = `
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="rounded-xl overflow-hidden bg-gray-50 border border-gray-200 shadow-inner">
            <img src="${coverSrc}" alt="${p['Name']}" class="w-full h-auto object-cover">
          </div>
          <div class="space-y-4">
            <div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-red-100 text-brand-red uppercase">${p['Categories']}</span>
              <h2 class="text-lg sm:text-xl font-bold text-gray-900 mt-2 leading-snug">${p['Name']}</h2>
              <div class="text-xs text-gray-500 mt-1">Mã sản phẩm: <span class="font-mono font-bold text-gray-800">${sku}</span> | Nhà xuất bản Trẻ</div>
            </div>

            <!-- Price -->
            <div class="flex items-baseline gap-2">
              <span class="text-2xl font-black text-brand-red">${formatVND(sale)}</span>
              ${reg > sale ? `<span class="text-sm text-gray-400 line-through">${formatVND(reg)}</span>` : ''}
              ${p.discount_pct > 0 ? `<span class="text-xs font-bold text-white bg-brand-red px-1.5 py-0.5 rounded">-${p.discount_pct}%</span>` : ''}
            </div>

            <!-- Attributes table -->
            <div class="bg-gray-50 p-3 rounded-lg border border-gray-200 text-xs space-y-1.5 text-gray-700">
              <div class="flex justify-between"><strong>Tác giả:</strong> <span>${p['Attribute 1 value(s)']}</span></div>
              <div class="flex justify-between"><strong>Nhà xuất bản:</strong> <span>${p['Attribute 2 value(s)']}</span></div>
              <div class="flex justify-between"><strong>Năm xuất bản:</strong> <span>${p['Attribute 3 value(s)']}</span></div>
              <div class="flex justify-between"><strong>Số trang:</strong> <span>${p['Attribute 4 value(s)']} trang</span></div>
              <div class="flex justify-between"><strong>Khổ sách:</strong> <span>${p['Attribute 6 value(s)']}</span></div>
              <div class="flex justify-between"><strong>ISBN:</strong> <span class="font-mono">${p['Attribute 7 value(s)']}</span></div>
            </div>

            <!-- Action buttons -->
            <div class="pt-2 flex gap-3">
              <button onclick="addToCart('${sku}'); closeQuickView(); openCart();" class="flex-1 py-3 bg-brand-red hover:bg-red-700 text-white font-bold rounded-xl text-xs uppercase shadow transition cursor-pointer flex items-center justify-center gap-1.5">
                <span class="material-symbols-outlined text-sm">shopping_cart</span>
                <span>Thêm Vào Giỏ Hàng</span>
              </button>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-gray-200 text-xs text-gray-700 space-y-2">
          <h4 class="font-bold text-sm text-gray-900 uppercase">Giới thiệu tác phẩm:</h4>
          <div>${p['Description']}</div>
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
      openCart();
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
        alert('Áp dụng mã ưu đãi 10% thành công!');
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

      document.getElementById('shopResultTotal').textContent = filtered.length + ' Sản phẩm';
      document.getElementById('fullCatalogGrid').innerHTML = filtered.map(p => createProductCardHTML(p)).join('');
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
      document.getElementById('timerHours').textContent = String(h).padStart(2, '0');
      document.getElementById('timerMinutes').textContent = String(m).padStart(2, '0');
      document.getElementById('timerSeconds').textContent = String(s).padStart(2, '0');
    }, 1000);

    // Initial load
    renderFlashSale();
    switchTabContent('bestseller');
    updateCartUI();
  </script>
</body>
</html>
"""

class DuwcsAnhLibServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/assets/'):
            rel_path = self.path[len('/assets/'):]
            target_file = ASSETS_DIR / rel_path
            if target_file.exists() and target_file.is_file():
                self.send_response(200)
                if target_file.suffix == '.png':
                    self.send_header('Content-Type', 'image/png')
                elif target_file.suffix == '.jpg':
                    self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(target_file.read_bytes())
                return
            else:
                self.send_error(404, "Asset Not Found")
                return

        if self.path in ['/', '/index.html', '/home', '/shop']:
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
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("=" * 60)
        print(f" DUWCSANHLIB PRODUCTION-GRADE LOCAL SERVER STARTED!")
        print(f" URL: http://localhost:{port}")
        print(f" Hotline: 0933.543.987")
        print("=" * 60)
        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass
        httpd.serve_forever()

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    start_server(port)
