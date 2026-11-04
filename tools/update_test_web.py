import sys
from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'test_local_web.py'
text = p.read_text(encoding='utf-8')

# 1. Head favicons
old_head = '<title>DuwcsAnhLib — Hiệu Sách & Thư Viện Tri Thức</title>\n  <script src="https://cdn.tailwindcss.com"></script>'
new_head = '''<title>DuwcsAnhLib — Hiệu Sách & Thư Viện Tri Thức</title>
  <!-- Brand Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <script src="https://cdn.tailwindcss.com"></script>'''

assert old_head in text, 'old_head not found'
text = text.replace(old_head, new_head, 1)

# 2. Header Logo Symbol: replace DA badge with logo-header-symbol.png
old_logo = '''      <!-- Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer shrink-0" onclick="showView('home')">
        <div class="w-11 h-11 rounded-xl bg-brand-red text-white flex items-center justify-center font-black text-xl shadow-md border-2 border-amber-300">
          DA
        </div>
        <div>
          <span class="text-2xl font-black tracking-wider text-brand-red uppercase leading-none block">DuwcsAnh<span class="text-amber-600">Lib</span></span>
          <span class="text-[10px] text-gray-500 font-bold tracking-widest uppercase block mt-0.5">Hiệu Sách & Thư Viện Tri Thức</span>
        </div>
      </div>'''

new_logo = '''      <!-- Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer shrink-0" onclick="showView('home')">
        <img src="/assets/logo-header-symbol.png" alt="DuwcsAnhLib" class="h-12 w-auto object-contain hover:scale-105 transition-transform">
        <div>
          <span class="text-2xl font-black tracking-wider text-brand-red uppercase leading-none block">DuwcsAnh<span class="text-amber-600">Lib</span></span>
          <span class="text-[10px] text-gray-500 font-bold tracking-widest uppercase block mt-0.5">Hiệu Sách & Thư Viện Tri Thức</span>
        </div>
      </div>'''

assert old_logo in text, 'old_logo not found'
text = text.replace(old_logo, new_logo, 1)

# 3. Footer Logo
old_footer = '''      <!-- Col 1 -->
      <div class="space-y-3">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-brand-red text-white flex items-center justify-center font-bold">DA</div>
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
        </div>'''

new_footer = '''      <!-- Col 1 -->
      <div class="space-y-3">
        <div class="flex items-center gap-2 cursor-pointer" onclick="showView('home')">
          <img src="/assets/site-icon-512.png" alt="DuwcsAnhLib" class="w-8 h-8 rounded-lg object-contain shadow-sm">
          <span class="font-black text-base text-brand-red uppercase">DuwcsAnhLib</span>
        </div>'''

assert old_footer in text, 'old_footer not found'
text = text.replace(old_footer, new_footer, 1)

# 4. Server routes
old_server = '''class DuwcsAnhLibServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/assets/'):'''

new_server = '''class DuwcsAnhLibServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            ico_file = ASSETS_DIR / 'favicon.ico'
            if ico_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'image/x-icon')
                self.end_headers()
                self.wfile.write(ico_file.read_bytes())
                return

        if self.path.startswith('/assets/'):'''

assert old_server in text, 'old_server not found'
text = text.replace(old_server, new_server, 1)

# 5. Server ico MIME type
old_mime = '''                elif target_file.suffix == '.jpg':
                    self.send_header('Content-Type', 'image/jpeg')'''

new_mime = '''                elif target_file.suffix in ['.jpg', '.jpeg']:
                    self.send_header('Content-Type', 'image/jpeg')
                elif target_file.suffix == '.ico':
                    self.send_header('Content-Type', 'image/x-icon')'''

assert old_mime in text, 'old_mime not found'
text = text.replace(old_mime, new_mime, 1)

# 6. allow_reuse_address & fallback port
old_start = '''def start_server(port=8080):
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
        httpd.serve_forever()'''

new_start = '''def start_server(port=8080):
    handler = DuwcsAnhLibServer
    socketserver.TCPServer.allow_reuse_address = True
    try:
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
    except OSError as e:
        if "10048" in str(e):
            alt_port = port + 1
            print(f"[!] Cổng {port} đang bận, tự động chuyển sang cổng {alt_port}...")
            start_server(alt_port)
        else:
            raise'''

assert old_start in text, 'old_start not found'
text = text.replace(old_start, new_start, 1)

p.write_text(text, encoding='utf-8')
print('test_local_web.py successfully updated!')

