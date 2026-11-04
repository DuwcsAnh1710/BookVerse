from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'test_local_web.py'
text = p.read_text(encoding='utf-8')

# 1. Remove the "Xem Landing Page" button from navbar
old_nav_btn = """          <!-- Horizontal Nav Links -->
          <div class="hidden lg:flex items-center">
            <a href="/landing" class="py-2 px-3.5 bg-yellow-400 hover:bg-yellow-300 text-stone-950 font-black rounded-lg text-xs uppercase tracking-wider shadow-sm mr-2 flex items-center gap-1 transition">
              <span class="material-symbols-outlined text-sm text-stone-950">rocket_launch</span>
              <span>Xem Landing Page</span>
            </a>
            <button onclick="showView('home')" class="py-3 px-4 hover:bg-black/20 transition flex items-center gap-1">
              <span>Trang chủ</span>
            </button>"""

new_nav_btn = """          <!-- Horizontal Nav Links -->
          <div class="hidden lg:flex items-center">
            <button onclick="showView('shop')" class="py-3 px-4 hover:bg-black/20 text-white font-bold transition flex items-center gap-1">
              <span>Cửa Hàng Sách (25 Sách)</span>
            </button>"""

if old_nav_btn in text:
    text = text.replace(old_nav_btn, new_nav_btn, 1)
    print("[OK] Removed 'Xem Landing Page' button from store navbar")

# 2. Add discreet link in store footer to revisit Landing Page if desired
old_footer_link = """        <div class="flex items-center gap-2 cursor-pointer" onclick="showView('home')">
          <img src="/assets/site-icon-512.png" alt="DuwcsAnhLib" class="w-8 h-8 rounded-lg object-contain shadow-sm">
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
        </div>"""

new_footer_link = """        <div class="flex items-center gap-2 cursor-pointer" onclick="showView('shop')">
          <img src="/assets/site-icon-512.png" alt="DuwcsAnhLib" class="w-8 h-8 rounded-lg object-contain shadow-sm">
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
        </div>
        <div class="pt-1">
          <a href="/landing?view=landing" onclick="localStorage.removeItem('duwcsanhlib_has_entered_store')" class="text-[11px] text-gray-400 hover:text-brand-red underline">
            &larr; Xem lại Giới thiệu &amp; Landing Page
          </a>
        </div>"""

if old_footer_link in text:
    text = text.replace(old_footer_link, new_footer_link, 1)
    print("[OK] Added discreet reset link in footer")

# 3. Update initial script in HTML_TEMPLATE to show shop and handle ?cat=
old_init = """    // Initial load
    renderFlashSale();
    switchTabContent('bestseller');
    updateCartUI();"""

new_init = """    // Initial load
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('cat');
    if (catParam) {
      filterCatAndShow(catParam);
    } else {
      showView('shop');
    }
    renderFlashSale();
    switchTabContent('bestseller');
    updateCartUI();"""

if old_init in text:
    text = text.replace(old_init, new_init, 1)
    print("[OK] Updated initial load to default to shop")

# 4. Update do_GET routing:
old_do_get = """        if self.path in ['/landing', '/landing.html', '/landing-page']:
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        if self.path in ['/', '/index.html', '/home', '/shop']:"""

new_do_get = """        if self.path in ['/landing', '/landing.html', '/landing-page'] or self.path.startswith('/landing?'):
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        # Trang chu mac dinh se luon vao Landing Page truoc tien
        if self.path in ['/', '/index.html'] or self.path.startswith('/?'):
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        # Khi da vao cua hang (/shop) thi phuc vu truc tiep giao dien Cua Hang
        if self.path.startswith('/shop') or self.path in ['/home']:"""

if old_do_get in text:
    text = text.replace(old_do_get, new_do_get, 1)
    print("[OK] Updated routing in do_GET")

p.write_text(text, encoding='utf-8')
print("Successfully updated test_local_web.py flow!")

