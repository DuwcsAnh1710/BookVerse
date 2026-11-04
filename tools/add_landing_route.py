from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'test_local_web.py'
text = p.read_text(encoding='utf-8')

# 1. Add /landing route
old_route = "        if self.path in ['/', '/index.html', '/home', '/shop']:"
new_route = """        if self.path in ['/landing', '/landing.html', '/landing-page']:
            landing_file = ROOT / 'duwcsanhlib' / 'landing-page.html'
            if landing_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(landing_file.read_bytes())
                return

        if self.path in ['/', '/index.html', '/home', '/shop']:"""

assert old_route in text, "old_route not found"
text = text.replace(old_route, new_route, 1)

# 2. Add Landing Page Link button in Nav bar
old_nav = """          <!-- Horizontal Nav Links -->
          <div class="hidden lg:flex items-center">
            <button onclick="showView('home')" class="py-3 px-4 hover:bg-black/20 transition flex items-center gap-1">
              <span>Trang chủ</span>
            </button>"""

new_nav = """          <!-- Horizontal Nav Links -->
          <div class="hidden lg:flex items-center">
            <a href="/landing" class="py-2 px-3.5 bg-yellow-400 hover:bg-yellow-300 text-stone-950 font-black rounded-lg text-xs uppercase tracking-wider shadow-sm mr-2 flex items-center gap-1 transition">
              <span class="material-symbols-outlined text-sm text-stone-950">rocket_launch</span>
              <span>Xem Landing Page</span>
            </a>
            <button onclick="showView('home')" class="py-3 px-4 hover:bg-black/20 transition flex items-center gap-1">
              <span>Trang chủ</span>
            </button>"""

assert old_nav in text, "old_nav not found"
text = text.replace(old_nav, new_nav, 1)

p.write_text(text, encoding='utf-8')
print("Successfully integrated /landing route and Nav button in test_local_web.py!")

