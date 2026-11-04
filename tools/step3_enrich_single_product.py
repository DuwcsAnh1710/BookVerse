"""Bổ sung tính năng Trang Chi Tiết Sản Phẩm (Single Product Page) chuẩn CRO và WooCommerce Flatsome vào test_local_web.py:
1. View riêng biệt: id="view-product".
2. Hàm renderProductDetail(sku) với bố cục 2 cột, breadcrumbs, trích dẫn, bảng thông số, nút 'Mua Ngay' COD, 4 tabs chuyên sâu và Carousel sách cùng thể loại.
3. Hỗ trợ route /product?sku=DAL-xxx trên server HTTP nội bộ.
4. Điều hướng mượt mà: Click vào tên sách hoặc bìa sách để vào xem trang chi tiết đầy đủ; click nút Xem nhanh để mở modal Quick View.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
web_file = ROOT / 'test_local_web.py'

content = web_file.read_text(encoding='utf-8')

# 1. Thêm view-product vào HTML template
view_product_html = """
    <!-- VIEW: DEDICATED SINGLE PRODUCT PAGE (CHUẨN WOOCOMMERCE & FLATSOME) -->
    <div id="view-product" class="hidden space-y-8">
      <div id="productDetailContainer">
        <!-- Rendered by JS -->
      </div>
    </div>
"""

if 'id="view-product"' not in content:
    content = content.replace('<!-- VIEW: BLOGS LIST -->', view_product_html + '\n    <!-- VIEW: BLOGS LIST -->')

# 2. Bổ sung hàm renderProductDetail và nâng cấp showView trong JS
product_js_code = """
    // Render Dedicated Single Product Page
    function renderProductDetail(sku) {
      const p = allProducts.find(x => x.SKU === sku);
      if (!p) return;
      const reg = parseInt(p['Regular price'] || 0);
      const sale = parseInt(p['Sale price'] || reg);
      const coverSrc = `/assets/covers/${sku}.png`;
      const isLiked = wishlist.includes(sku);
      
      // Sách liên quan cùng thể loại (ngoại trừ cuốn hiện tại)
      const related = allProducts.filter(x => x.Categories === p.Categories && x.SKU !== sku).slice(0, 4);

      const container = document.getElementById('productDetailContainer');
      container.innerHTML = `
        <!-- Breadcrumbs -->
        <div class="bg-white p-3.5 rounded-xl border border-gray-200 flex items-center justify-between text-xs">
          <div class="flex items-center gap-1.5 text-gray-500 flex-wrap">
            <a href="/" class="hover:text-brand-red">Trang chủ</a>
            <span>/</span>
            <button onclick="showView('shop')" class="hover:text-brand-red">Cửa hàng sách</button>
            <span>/</span>
            <button onclick="filterCatAndShow('${p['Categories']}')" class="hover:text-brand-red font-semibold text-gray-700">${p['Categories']}</button>
            <span>/</span>
            <span class="text-gray-900 font-bold truncate max-w-xs">${p['Name']}</span>
          </div>
          <button onclick="showView('shop')" class="text-brand-red font-bold hover:underline flex items-center gap-1 shrink-0">
            <span class="material-symbols-outlined text-xs">arrow_back</span>
            <span>Quay lại cửa hàng</span>
          </button>
        </div>

        <!-- Main Product Section (2 Columns) -->
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 sm:p-10">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            <!-- Col Left: Large Book Cover & Trust badges (5 cols) -->
            <div class="lg:col-span-5 space-y-4">
              <div class="rounded-2xl overflow-hidden bg-gray-50 border border-gray-200 shadow-md aspect-[2/3] relative group">
                <img src="${coverSrc}" alt="${p['Name']}" class="w-full h-full object-cover">
                ${p.discount_pct > 0 ? `
                  <span class="absolute top-4 left-4 bg-brand-red text-white text-xs font-black px-3 py-1 rounded-lg shadow-md">
                    GIẢM ${p.discount_pct}%
                  </span>
                ` : ''}
                <button onclick="toggleWishlist('${sku}', event)" class="absolute top-4 right-4 w-9 h-9 rounded-full bg-white/90 hover:bg-white text-gray-500 hover:text-brand-red shadow flex items-center justify-center transition cursor-pointer" title="Lưu sách">
                  <span class="material-symbols-outlined text-xl ${isLiked ? 'fill-icon text-brand-red' : ''}">favorite</span>
                </button>
              </div>

              <!-- Quy chuẩn đóng gói 3 lớp bảo vệ -->
              <div class="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 space-y-2">
                <div class="font-black text-amber-950 flex items-center gap-1.5 uppercase tracking-wide">
                  <span class="material-symbols-outlined text-base text-amber-700">shield</span>
                  <span>Đặc quyền bảo vệ ấn bản DuwcsAnhLib:</span>
                </div>
                <div class="space-y-1 text-[11px] text-amber-800">
                  <div>✓ <strong>100% Ấn bản chuẩn hóa</strong> từ Nhà xuất bản Trẻ, không sách lậu.</div>
                  <div>✓ <strong>Bọc bóng khí + Thùng carton 3 lớp</strong> bo góc chống cấn móp mép gáy.</div>
                  <div>✓ <strong>Đổi trả 1-đổi-1 trong 7 ngày</strong> nếu lỗi kỹ thuật từ nhà in.</div>
                  <div>✓ <strong>Miễn phí vận chuyển toàn quốc</strong> cho đơn từ 250.000 đ.</div>
                </div>
              </div>
            </div>

            <!-- Col Right: Product Info & Actions (7 cols) -->
            <div class="lg:col-span-7 space-y-5">
              
              <div>
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-0.5 bg-red-100 text-brand-red rounded-full text-[10px] font-black uppercase tracking-wider">${p['Categories']}</span>
                  <span class="text-xs text-gray-400 font-mono">SKU: <strong>${sku}</strong></span>
                  <span class="text-xs text-emerald-700 font-bold ml-auto flex items-center gap-1">
                    <span class="material-symbols-outlined text-sm">check_circle</span>
                    <span>Còn ${p['Stock']} cuốn</span>
                  </span>
                </div>
                
                <h1 class="text-2xl sm:text-3xl font-black text-gray-900 mt-2 serif-title leading-snug">${p['Name']}</h1>
                <p class="text-xs sm:text-sm text-gray-600 mt-1 font-medium italic">${p.subtitle || ''}</p>
                
                <!-- Rating Social Proof -->
                <div class="flex items-center gap-2 mt-2 pt-1 border-t border-gray-100 text-xs">
                  <div class="flex text-amber-400">
                    <span class="material-symbols-outlined text-base fill-icon text-amber-400">star</span>
                    <span class="material-symbols-outlined text-base fill-icon text-amber-400">star</span>
                    <span class="material-symbols-outlined text-base fill-icon text-amber-400">star</span>
                    <span class="material-symbols-outlined text-base fill-icon text-amber-400">star</span>
                    <span class="material-symbols-outlined text-base fill-icon text-amber-400">star</span>
                  </div>
                  <span class="font-bold text-gray-900">5.0 / 5.0</span>
                  <span class="text-gray-400">•</span>
                  <span class="text-gray-500">${p.reviews_count} đánh giá</span>
                  <span class="text-gray-400">•</span>
                  <span class="text-brand-red font-bold">Đã bán ${p.sold_count} cuốn</span>
                </div>
              </div>

              <!-- Price Box -->
              <div class="p-4 bg-red-50/70 border border-red-100 rounded-2xl flex items-baseline gap-3">
                <span class="text-3xl font-black text-brand-red">${formatVND(sale)}</span>
                ${reg > sale ? `<span class="text-sm text-gray-400 line-through">${formatVND(reg)}</span>` : ''}
                ${p.discount_pct > 0 ? `
                  <span class="text-xs font-black text-white bg-brand-red px-2 py-0.5 rounded shadow">
                    Tiết kiệm ${formatVND(reg - sale)} (${p.discount_pct}%)
                  </span>
                ` : ''}
              </div>

              <!-- Signature Quote -->
              <div class="p-4 bg-stone-50 border-l-4 border-brand-red rounded-r-2xl italic text-xs sm:text-sm text-stone-700 leading-relaxed shadow-inner">
                "${p.quote}"
              </div>

              <!-- Key Highlights Bullet Points -->
              <div class="space-y-1.5 text-xs text-gray-700">
                <div class="font-bold text-gray-900 uppercase text-[11px] tracking-wider">Điểm nổi bật của ấn bản:</div>
                ${(p.highlights || []).map(h => `
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-sm text-brand-red">check_circle</span>
                    <span>${h}</span>
                  </div>
                `).join('')}
              </div>

              <!-- Quick Specs Table -->
              <div class="grid grid-cols-2 gap-2 text-xs text-gray-700 bg-gray-50 p-4 rounded-xl border border-gray-200">
                <div><span class="text-gray-400">Tác giả:</span> <strong class="text-gray-900 block">${p['Attribute 1 value(s)']}</strong></div>
                <div><span class="text-gray-400">Nhà xuất bản:</span> <strong class="text-gray-900 block">${p['Attribute 2 value(s)']}</strong></div>
                <div><span class="text-gray-400">Năm xuất bản:</span> <span class="block">${p['Attribute 3 value(s)']}</span></div>
                <div><span class="text-gray-400">Số trang & Khổ:</span> <span class="block">${p['Attribute 4 value(s)']} tr. • ${p['Attribute 6 value(s)']}</span></div>
                <div><span class="text-gray-400">Quy cách bìa:</span> <span class="block">${p.format}</span></div>
                <div><span class="text-gray-400">Mã ISBN:</span> <span class="font-mono block text-gray-800">${p['Attribute 7 value(s)']}</span></div>
              </div>

              <!-- Action CTAs: Add to Cart + Buy Now -->
              <div class="pt-3 space-y-3">
                <div class="flex items-center gap-3">
                  <div class="flex items-center border border-gray-300 rounded-xl overflow-hidden bg-white shrink-0">
                    <button onclick="decrementDetailQty()" class="px-3.5 py-3 bg-gray-100 hover:bg-gray-200 font-bold text-gray-700 cursor-pointer">-</button>
                    <input type="number" id="detailQtyInput" value="1" min="1" max="10" class="w-12 text-center text-xs font-bold outline-none border-none py-2" readonly>
                    <button onclick="incrementDetailQty()" class="px-3.5 py-3 bg-gray-100 hover:bg-gray-200 font-bold text-gray-700 cursor-pointer">+</button>
                  </div>
                  
                  <button onclick="addDetailToCart('${sku}')" class="flex-1 py-3.5 bg-red-50 hover:bg-red-100 border-2 border-brand-red text-brand-red font-black rounded-xl text-xs uppercase tracking-wider transition flex items-center justify-center gap-2 cursor-pointer shadow-sm">
                    <span class="material-symbols-outlined text-base">shopping_cart</span>
                    <span>Thêm Vào Giỏ Hàng</span>
                  </button>

                  <button onclick="buyNowDetail('${sku}')" class="flex-1 py-3.5 bg-brand-red bg-brand-red-hover text-white font-black rounded-xl text-xs uppercase tracking-wider shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2 cursor-pointer">
                    <span class="material-symbols-outlined text-base">bolt</span>
                    <span>Mua Ngay (COD)</span>
                  </button>
                </div>
              </div>

            </div>

          </div>

          <!-- Product Details Tabs (4 Tabs) -->
          <div class="mt-12 pt-8 border-t border-gray-200 space-y-6">
            <div class="flex items-center gap-3 border-b border-gray-200 pb-3 text-xs font-bold overflow-x-auto no-scrollbar">
              <button onclick="switchProductTab('desc')" id="prod-tab-desc" class="px-4 py-2 rounded-xl bg-brand-red text-white transition">Giới Thiệu Tác Phẩm</button>
              <button onclick="switchProductTab('specs')" id="prod-tab-specs" class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition">Thông Số Xuất Bản</button>
              <button onclick="switchProductTab('pack')" id="prod-tab-pack" class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition">Quy Cách Đóng Gói</button>
              <button onclick="switchProductTab('review')" id="prod-tab-review" class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition">Độc Giả Đánh Giá (${p.reviews_count})</button>
            </div>

            <div id="prodTabContentDesc" class="prose max-w-none text-xs sm:text-sm text-gray-700 leading-relaxed space-y-3">
              ${p['Description']}
              <div class="p-4 bg-gray-50 rounded-xl border border-gray-200 text-xs">
                <strong>Đối tượng độc giả khuyên đọc:</strong> ${p.audience}
              </div>
            </div>

            <div id="prodTabContentSpecs" class="hidden text-xs text-gray-700 space-y-3">
              <table class="w-full max-w-xl border border-gray-200 rounded-xl overflow-hidden">
                <tr class="bg-gray-50 border-b border-gray-200"><th class="text-left p-3 text-gray-500 w-1/3">Tác giả</th><td class="p-3 font-bold text-gray-900">${p['Attribute 1 value(s)']}</td></tr>
                <tr class="border-b border-gray-200"><th class="text-left p-3 text-gray-500">Nhà xuất bản</th><td class="p-3 font-bold text-gray-900">${p['Attribute 2 value(s)']}</td></tr>
                <tr class="bg-gray-50 border-b border-gray-200"><th class="text-left p-3 text-gray-500">Năm xuất bản</th><td class="p-3">${p['Attribute 3 value(s)']}</td></tr>
                <tr class="border-b border-gray-200"><th class="text-left p-3 text-gray-500">Số trang</th><td class="p-3">${p['Attribute 4 value(s)']} trang</td></tr>
                <tr class="bg-gray-50 border-b border-gray-200"><th class="text-left p-3 text-gray-500">Kích thước khổ sách</th><td class="p-3">${p['Attribute 6 value(s)']}</td></tr>
                <tr class="border-b border-gray-200"><th class="text-left p-3 text-gray-500">Định dạng bìa</th><td class="p-3">${p.format}</td></tr>
                <tr class="bg-gray-50 border-b border-gray-200"><th class="text-left p-3 text-gray-500">Trọng lượng sách</th><td class="p-3">${p.weight}</td></tr>
                <tr class="border-b border-gray-200"><th class="text-left p-3 text-gray-500">Mã ISBN</th><td class="p-3 font-mono">${p['Attribute 7 value(s)']}</td></tr>
                <tr class="bg-gray-50"><th class="text-left p-3 text-gray-500">Đơn vị phân phối</th><td class="p-3 font-bold text-brand-red">DuwcsAnhLib Official Store</td></tr>
              </table>
            </div>

            <div id="prodTabContentPack" class="hidden text-xs text-gray-700 space-y-4">
              <div class="bg-[#FFFBEB] p-6 rounded-2xl border border-amber-200 space-y-3">
                <h4 class="font-bold text-sm text-amber-950 uppercase">Quy chuẩn 3 lớp đóng gói đặc quyền DuwcsAnhLib</h4>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div class="bg-white p-3.5 rounded-xl border border-amber-200 space-y-1">
                    <span class="font-black text-amber-900 block text-[11px]">Lớp 1: Màng co</span>
                    <p class="text-[11px] text-gray-600">Bảo vệ bề mặt bìa và chống bụi ẩm trong kho.</p>
                  </div>
                  <div class="bg-white p-3.5 rounded-xl border border-amber-200 space-y-1">
                    <span class="font-black text-amber-900 block text-[11px]">Lớp 2: Xốp bóng khí</span>
                    <p class="text-[11px] text-gray-600">Bọc 2-3 lớp bao bọc 4 góc gáy chống va đập.</p>
                  </div>
                  <div class="bg-white p-3.5 rounded-xl border border-amber-200 space-y-1">
                    <span class="font-black text-amber-900 block text-[11px]">Lớp 3: Hộp carton</span>
                    <p class="text-[11px] text-gray-600">Hộp carton cứng 3 lớp dán băng keo niêm phong.</p>
                  </div>
                </div>
              </div>
            </div>

            <div id="prodTabContentReview" class="hidden text-xs text-gray-700 space-y-4">
              <div class="p-4 bg-gray-50 rounded-xl border border-gray-200 space-y-2">
                <div class="flex items-center gap-1 text-amber-400">★★★★★</div>
                <p class="italic text-gray-800 text-xs">"${p.reader_review}"</p>
                <div class="text-[11px] font-bold text-gray-500">— Độc giả xác thực mua hàng tại DuwcsAnhLib</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Related Books Carousel (Sách cùng thể loại) -->
        ${related.length > 0 ? `
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-6 bg-brand-red rounded-full"></span>
                <h2 class="text-xl font-black text-gray-900 uppercase">Tác Phẩm Cùng Thể Loại '${p['Categories']}'</h2>
              </div>
              <button onclick="filterCatAndShow('${p['Categories']}')" class="text-xs font-bold text-brand-red hover:underline">
                Xem toàn bộ &rarr;
              </button>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              ${related.map(r => createProductCardHTML(r)).join('')}
            </div>
          </div>
        ` : ''}
      `;
    }

    function incrementDetailQty() {
      const input = document.getElementById('detailQtyInput');
      if (input && parseInt(input.value) < 10) input.value = parseInt(input.value) + 1;
    }

    function decrementDetailQty() {
      const input = document.getElementById('detailQtyInput');
      if (input && parseInt(input.value) > 1) input.value = parseInt(input.value) - 1;
    }

    function addDetailToCart(sku) {
      const input = document.getElementById('detailQtyInput');
      const qty = input ? parseInt(input.value) || 1 : 1;
      const p = allProducts.find(x => x.SKU === sku);
      if (!p) return;
      const sale = parseInt(p['Sale price'] || p['Regular price'] || 0);
      const existing = cart.find(x => x.sku === sku);
      if (existing) {
        existing.qty += qty;
      } else {
        cart.push({ sku: sku, name: p['Name'], price: sale, qty: qty });
      }
      updateCartUI();
      showToast(`Đã thêm <strong>${qty} cuốn ${p['Name']}</strong> vào giỏ hàng!`);
    }

    function buyNowDetail(sku) {
      addDetailToCart(sku);
      openCart();
    }

    function switchProductTab(tab) {
      ['desc', 'specs', 'pack', 'review'].forEach(t => {
        const btn = document.getElementById('prod-tab-' + t);
        const pane = document.getElementById('prodTabContent' + t.charAt(0).toUpperCase() + t.slice(1));
        if (btn) {
          if (t === tab) {
            btn.className = 'px-4 py-2 rounded-xl bg-brand-red text-white transition';
          } else {
            btn.className = 'px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition';
          }
        }
        if (pane) {
          if (t === tab) pane.classList.remove('hidden');
          else pane.classList.add('hidden');
        }
      });
    }
"""

if 'function renderProductDetail' not in content:
    content = content.replace('// Render Flash Sale Items', product_js_code + '\n    // Render Flash Sale Items')

# Cập nhật showView để nhận tham số product
content = content.replace(
    "['home', 'shop', 'content', 'blogs'].forEach(v => {",
    "['home', 'shop', 'content', 'blogs', 'product'].forEach(v => {"
)

content = content.replace(
    "if (viewName === 'shop') {\n        handleSidebarFilter();\n      } else if (viewName === 'content' && contentKey) {\n        renderContent(contentKey);\n      }",
    "if (viewName === 'shop') {\n        handleSidebarFilter();\n      } else if (viewName === 'content' && contentKey) {\n        renderContent(contentKey);\n      } else if (viewName === 'product' && contentKey) {\n        renderProductDetail(contentKey);\n      }"
)

# Cập nhật createProductCardHTML: Click vào ảnh hoặc tên sách sẽ mở trang chi tiết sản phẩm
content = content.replace(
    """<div class="relative overflow-hidden rounded-lg bg-gray-50 aspect-[2/3] cursor-pointer" onclick="openQuickView('${sku}')">""",
    """<div class="relative overflow-hidden rounded-lg bg-gray-50 aspect-[2/3] cursor-pointer" onclick="showView('product', '${sku}')">"""
)

content = content.replace(
    """<h3 class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition line-clamp-2 leading-snug cursor-pointer h-8" onclick="openQuickView('${sku}')">""",
    """<h3 class="font-bold text-xs text-gray-900 group-hover:text-brand-red transition line-clamp-2 leading-snug cursor-pointer h-8" onclick="showView('product', '${sku}')">"""
)

# Cập nhật server route cho /product
route_target = """        # Khi người dùng vào Cửa hàng (/shop) hoặc /home
        if self.path.startswith('/shop') or self.path in ['/home']:"""

route_replacement = """        # Khi người dùng vào xem trực tiếp trang sản phẩm (/product) hoặc Cửa hàng (/shop)
        if self.path.startswith('/product') or self.path.startswith('/shop') or self.path in ['/home']:"""

content = content.replace(route_target, route_replacement)

# Cập nhật initial load script cho /product?sku=...
init_target = """    // Initial load
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('cat');
    if (catParam) {
      filterCatAndShow(catParam);
    } else {
      showView('shop');
    }"""

init_replacement = """    // Initial load
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('cat');
    const skuParam = urlParams.get('sku');
    if (skuParam) {
      showView('product', skuParam);
    } else if (catParam) {
      filterCatAndShow(catParam);
    } else {
      showView('shop');
    }"""

content = content.replace(init_target, init_replacement)

web_file.write_text(content, encoding='utf-8')
print("test_local_web.py đã được nâng cấp Trang Chi Tiết Sản Phẩm thành công!")

