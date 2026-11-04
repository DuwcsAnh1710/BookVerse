from pathlib import Path
import re, json, sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path('moc-thu')
books = json.loads((ROOT / 'data/books.json').read_text(encoding='utf-8'))
for b in books:
    found = False
    for f in (ROOT / 'research').glob('*.html'):
        content = f.read_text(encoding='utf-8', errors='ignore')
        if b['title'] in content or b['isbn'] in content:
            m = re.search(r'og:image\"\s+content=\"([^\"]+)\"', content)
            if not m:
                m = re.search(r'id=\"Content_ctl00_imgMain\"\s+src=\"([^\"]+)\"', content)
            img = m.group(1) if m else 'N/A'
            print(f"{b['sku']}: {b['title']} -> {img}")
            found = True
            break
    if not found:
        print(f"{b['sku']}: NOT FOUND")
