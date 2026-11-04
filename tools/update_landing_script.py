from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'landing-page.html'
text = p.read_text(encoding='utf-8')

old_script = """  <script>
    function enterStore(cat) {
      // Mark visitor as having entered store
      try {
        localStorage.setItem('duwcsanhlib_has_entered_store', 'true');
      } catch (e) {}
      
      let targetUrl = '/shop';
      if (cat) {
        targetUrl = '/shop?cat=' + encodeURIComponent(cat);
      }
      window.location.href = targetUrl;
    }
  </script>"""

new_script = """  <script>
    // Smart visitor logic:
    // Lan dau truy cap -> Hien thi Landing Page.
    // Neu da vao cua hang 1-2 lan -> Tu dong chuyen thang vao Cua Hang (/shop).
    try {
      const hasEntered = localStorage.getItem('duwcsanhlib_has_entered_store') === 'true';
      const urlParams = new URLSearchParams(window.location.search);
      const isForced = urlParams.get('view') === 'landing';
      if (hasEntered && !isForced) {
        window.location.replace('/shop');
      }
    } catch (e) {}

    function enterStore(cat) {
      try {
        localStorage.setItem('duwcsanhlib_has_entered_store', 'true');
      } catch (e) {}
      
      let targetUrl = '/shop';
      if (cat) {
        targetUrl = '/shop?cat=' + encodeURIComponent(cat);
      }
      window.location.href = targetUrl;
    }
  </script>"""

assert old_script in text, "old_script not found"
text = text.replace(old_script, new_script, 1)
p.write_text(text, encoding='utf-8')
print("Updated duwcsanhlib/landing-page.html with smart returning visitor logic!")

