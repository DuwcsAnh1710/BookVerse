"""
Automated End-to-End Headless Verification Test Suite for DuwcsAnhLib
Verifies the complete frontend user flow using Microsoft Edge Headless:
1. Mobile Responsiveness (Viewport 440x956 iPhone 16 Pro Max without overflow)
2. Logo & Header Elements (logo-header.png, search sync, wishlist badge)
3. Taskbar Golden Amber Highlight on All 6 Tabs
4. DANH MUC SAN PHAM Mega Menu Dropdown Toggle & Category Filtering
5. Landing Page Onboarding & Store Entry Transition
6. Flatsome Checkout Flow (Empty state, Cart listing, Voucher calculation)
7. MoMo QR & COD Order Placement with Dynamic QR & 1-Click Copy
"""
import unittest
import subprocess
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class TestCheckoutFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        cls.html_path = ROOT / 'duwcsanhlib-static-web' / 'index.html'
        
        if not cls.html_path.exists():
            raise FileNotFoundError(f"Missing {cls.html_path}. Run tools/build_master_unified_web.py first.")

    def test_complete_frontend_flow(self):
        """Chay bo kiem thu 7/7 chuc nang giao dien va luong thanh toan tren Microsoft Edge Headless."""
        raw_html = self.html_path.read_text(encoding='utf-8')

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
    console.log('TEST 3 (Taskbar Golden Amber Highlight): PASS');
  } else {
    console.log('TEST 3: FAIL');
  }

  // 4. DANH MUC SAN PHAM Mega Menu Dropdown
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
    console.log('TEST 4 (DANH MUC SAN PHAM Dropdown): PASS (' + itemsCount + ' category items, no overflow clipping)');
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

        test_file = ROOT / 'duwcsanhlib-static-web' / 'test_checkout_runner.html'
        test_file.write_text(raw_html.replace('</body>', test_js + '</body>'), encoding='utf-8')

        try:
            file_url = 'file:///' + str(test_file.resolve()).replace('\\', '/')
            res = subprocess.run([
                self.edge_path,
                '--headless',
                '--disable-gpu',
                '--window-size=440,956',
                '--enable-logging=stderr',
                '--v=1',
                '--dump-dom',
                file_url
            ], capture_output=True, timeout=15)

            stderr = res.stderr.decode('utf-8', errors='ignore')
            test_lines = [line for line in stderr.splitlines() if re.search(r'TEST \d.*: PASS', line)]
            
            self.assertEqual(len(test_lines), 7, f"Kỳ vọng 7 bài kiểm thử PASS, thực tế đạt {len(test_lines)}: {test_lines}")
            for t_line in test_lines:
                self.assertIn(': PASS', t_line, f"Thất bại ở bài: {t_line}")
        finally:
            if test_file.exists():
                test_file.unlink()

if __name__ == '__main__':
    unittest.main(verbosity=2)
