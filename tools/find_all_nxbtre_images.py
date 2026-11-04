from pathlib import Path
import re, json, sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path('moc-thu')
books = json.loads((ROOT / 'data/books.json').read_text(encoding='utf-8'))

results = {}

for b in books:
    sku = b['sku']
    title = b['title']
    isbn = b['isbn']
    img_url = None
    
    for f in (ROOT / 'research').glob('*.html'):
        text = f.read_text(encoding='utf-8', errors='ignore')
        if title in text or isbn in text:
            # Look for /Images/Book/...
            matches = re.findall(r'(/Images/Book/[^"\'\s>]+\.(?:jpg|png|jpeg))', text, re.I)
            if matches:
                # Prefer 'full' over 'thumb'
                fulls = [m for m in matches if 'full' in m.lower()]
                if fulls:
                    img_url = "http://www.nxbtre.com.vn" + fulls[0]
                else:
                    img_url = "http://www.nxbtre.com.vn" + matches[0]
                break
            # Also check absolute URLs
            abs_matches = re.findall(r'(https?://(?:www\.)?nxbtre\.com\.vn/Images/Book/[^"\'\s>]+\.(?:jpg|png|jpeg))', text, re.I)
            if abs_matches:
                fulls = [m for m in abs_matches if 'full' in m.lower()]
                if fulls:
                    img_url = fulls[0]
                else:
                    img_url = abs_matches[0]
                break
    results[sku] = {'title': title, 'url': b['url'], 'img': img_url}
    print(f"{sku}: {title} -> {img_url}")

with open('tools/book_images_found.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

