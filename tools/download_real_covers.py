import urllib.request
import json
import sys
import io
from pathlib import Path
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path("D:/VSCode/HKDN/BookVerse")
OUT_DIR = ROOT / "duwcsanhlib/assets/covers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(ROOT / 'tools/book_images_found.json', 'r', encoding='utf-8') as f:
    images_info = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

success_count = 0

for sku_old, info in images_info.items():
    num = sku_old.split('-')[-1]
    dal_sku = f"DAL-{num}"
    url = info['img']
    if not url:
        print(f"Skipping {dal_sku}: No URL")
        continue

    # Try 'full' first if url has 'thumb'
    target_urls = []
    if 'thumb' in url:
        target_urls.append(url.replace('thumb', 'full'))
    target_urls.append(url)

    img_data = None
    for u in target_urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 1000:
                    img_data = data
                    break
        except Exception:
            continue

    if img_data:
        try:
            raw_im = Image.open(io.BytesIO(img_data)).convert('RGB')
            # Resize with aspect ratio preserved on 600x900 canvas with slight white padding
            target_w, target_h = 600, 900
            
            # Check ratio
            im_ratio = raw_im.width / raw_im.height
            target_ratio = target_w / target_h
            
            if abs(im_ratio - target_ratio) < 0.15:
                # Directly resize to 600x900 with high-quality Lanczos
                final_im = raw_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
            else:
                # Fit into 600x900
                raw_im.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                final_im = Image.new('RGB', (target_w, target_h), '#FFFFFF')
                offset = ((target_w - raw_im.width) // 2, (target_h - raw_im.height) // 2)
                final_im.paste(raw_im, offset)
            
            save_path = OUT_DIR / f"{dal_sku}.png"
            final_im.save(save_path, 'PNG', optimize=True)
            print(f"SUCCESS: {dal_sku} -> {info['title']} ({final_im.size[0]}x{final_im.size[1]})")
            success_count += 1
        except Exception as e:
            print(f"Error processing image {dal_sku}: {e}")
    else:
        print(f"FAILED to download: {dal_sku} -> {url}")

print(f"\n==========================================")
print(f"Downloaded and processed {success_count}/25 real official book covers!")
print(f"==========================================")

