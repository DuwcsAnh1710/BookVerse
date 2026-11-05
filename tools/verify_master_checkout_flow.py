"""
Master Verification Test Suite for DuwcsAnhLib
Tests:
1. Mobile Responsiveness (Viewport 440x956 iPhone 16 Pro Max without overflow)
2. Logo & Header Elements (logo-header.png, search sync, wishlist badge)
3. Taskbar Golden Amber Highlight on All 6 Tabs
4. DANH MỤC SẢN PHẨM Mega Menu Dropdown Toggle & Category Filtering
5. Landing Page Onboarding & Store Entry Transition
6. Flatsome Checkout Flow (Empty state, Cart listing, Voucher calculation)
7. MoMo QR & COD Order Placement with Dynamic QR & 1-Click Copy
"""
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("d:/VSCode/HKDN/BookVerse")
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = ROOT / 'duwcsanhlib-static-web' / 'index.html'

if not html_path.exists():
    print(f"Error: {html_path} does not exist. Run build_master_unified_web.py first.")
    sys.exit(1)

raw_html = html_path.read_text(encoding='utf-8')

test_js = """
<script>
window.alert = function(msg) { console.log('ALERT_CALLED: ' + msg); };
window.addEventListener('load', function() {
  console.log('=== MASTER VERIFICATION TEST START ===');
  
  // 1. Mobile Responsiveness Test
  showView('home');
  const winW = window.innerWidth;
  const bodyW = document.body.scrollWidth;
  if (bodyW <= winW + 15) {
    console.log('TEST 1 (Mobile Responsiveness): PASS (winW=' + winW + ', bodyW=' + bodyW + ')');
  } else {
    console.log('TEST 1: FAIL (Overflow detected: bodyW=' + bodyW + ' > winW=' + winW + ')');
  }

  // 2. Logo & Header Elements
  const logoImg = document.querySelector('#storeHeader img[src*="logo-header.png"]');
  const deskSearch = document.getElementById('headerSearchInput');
  const mobSearch = document.getElementById('mobileSearchInput');
  const wishlistBtn = document.getElementById('headerWishlistBtn');
  if (logoImg && deskSearch && mobSearch && wishlistBtn) {
    console.log('TEST 2 (Logo & Header Elements): PASS (logo-header.png & search & wishlist present)');
  } else {
    console.log('TEST 2: FAIL');
  }

  // 3. Taskbar Golden Amber Highlight
  const navKeys = ['home', 'shop', 'flashsale', 'bestseller', 'blogs', 'gioithieu'];
  let navPass = true;
  navKeys.forEach(k => {
    setActiveNavButton(k);
    const btn = document.getElementById('nav-btn-' + k);
    if (!btn || !btn.classList.contains('text-amber-300')) {
      navPass = false;
    }
  });
  if (navPass) {
    console.log('TEST 3 (Taskbar 6-Tab Golden Highlight): PASS');
  } else {
    console.log('TEST 3: FAIL');
  }

  // 4. DANH MỤC SẢN PHẨM Mega Menu Dropdown
  const megaBtn = document.getElementById('categoryMegaMenuBtn');
  const megaDrop = document.getElementById('categoryMegaMenuDropdown');
  const headerEl = document.getElementById('storeHeader');
  const headerOverflowHidden = headerEl.classList.contains('overflow-hidden');
  
  toggleCategoryMegaMenu();
  const opened = !megaDrop.classList.contains('hidden') && megaDrop.style.display === 'block';
  const itemsCount = megaDrop.children.length;
  toggleCategoryMegaMenu();
  const closed = megaDrop.classList.contains('hidden');
  
  if (opened && closed && itemsCount >= 6 && !headerOverflowHidden) {
    console.log('TEST 4 (DANH MỤC SẢN PHẨM Dropdown): PASS (' + itemsCount + ' category items, no overflow clipping)');
  } else {
    console.log('TEST 4: FAIL');
  }

  // 5. Landing Page Onboarding & Transition
  sessionStorage.removeItem('duwcsanhlib_entered_store');
  localStorage.removeItem('duwcsanhlib_visited');
  showView('landing');
  const landingEl = document.getElementById('view-landing');
  const storeHeader = document.getElementById('storeHeader');
  const landingVisible = landingEl && !landingEl.classList.contains('hidden') && landingEl.style.display !== 'none';
  const storeHidden = storeHeader && storeHeader.style.display === 'none';
  
  enterStore();
  const enteredStoreVisible = landingEl.style.display === 'none' && storeHeader.style.display === 'block';
  
  if (landingVisible && storeHidden && enteredStoreVisible) {
    console.log('TEST 5 (Landing Page & Store Transition): PASS');
  } else {
    console.log('TEST 5: FAIL');
  }

  // 6. Flatsome Checkout View & Calculations
  cart = [];
  showView('checkout');
  const emptyPass = !document.getElementById('checkoutEmptyState').classList.contains('hidden');
  
  addToCart('DAL-001');
  addToCart('DAL-002');
  addToCart('DAL-003');
  showView('checkout');
  
  const itemsRendered = document.getElementById('checkoutCartItems')?.children.length === 3;
  setCheckoutVoucher('DUWCSANH10');
  const discText = document.getElementById('checkoutDiscountDisplay')?.textContent;
  
  if (emptyPass && itemsRendered && discText.includes('-')) {
    console.log('TEST 6 (Flatsome Checkout & Voucher DUWCSANH10): PASS');
  } else {
    console.log('TEST 6: FAIL');
  }

  // 7. MoMo QR & Order Placement
  document.getElementById('checkoutCustName').value = 'Đoàn Đức Anh';
  document.getElementById('checkoutCustPhone').value = '0933543987';
  document.getElementById('checkoutCustAddress').value = 'Trường ĐH Sài Gòn, TP.HCM';
  
  processFullCheckout();
  
  const successView = document.getElementById('view-order-success');
  const isSuccessVisible = successView && !successView.classList.contains('hidden');
  const orderCode = document.getElementById('succOrderCode')?.textContent;
  const qrImg = document.getElementById('succVietQRImage')?.src;
  const copyNum = document.getElementById('copyAccountNum')?.textContent;
  const cartCleared = cart.length === 0;

  if (isSuccessVisible && orderCode.startsWith('#DAL-') && qrImg.includes('971025') && copyNum === '0933543987' && cartCleared) {
    console.log('TEST 7 (MoMo QR Order Placement & VietQR Napas BIN 971025): PASS');
  } else {
    console.log('TEST 7: FAIL');
  }

  console.log('=== MASTER VERIFICATION TEST END ===');
});
</script>
"""

test_file = ROOT / 'duwcsanhlib-static-web' / 'test_runner_suite.html'
test_file.write_text(raw_html.replace('</body>', test_js + '</body>'), encoding='utf-8')

try:
    file_url = 'file:///' + str(test_file.resolve()).replace('\\', '/')
    res = subprocess.run([
        edge_path,
        '--headless',
        '--disable-gpu',
        '--window-size=440,956',
        '--enable-logging=stderr',
        '--v=1',
        '--dump-dom',
        file_url
    ], capture_output=True, timeout=15)

    for line in res.stderr.decode('utf-8', errors='ignore').splitlines():
        if 'TEST' in line:
            print(line)
finally:
    if test_file.exists():
        test_file.unlink()

