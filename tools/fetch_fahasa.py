import urllib.request
import re
import json

urls = [
    'https://www.fahasa.com/cay-cam-ngot-cua-toi.html',
    'https://www.fahasa.com/dac-nhan-tam-kho-lon-tai-ban-2023.html',
    'https://www.fahasa.com/nha-gia-kim-tai-ban-2020.html',
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https://cdn0\.fahasa\.com/media/catalog/product/[^"\'\s]+\.(?:jpg|png|jpeg)', html)
            print(f"URL: {u}")
            print("Found images:", list(set(imgs))[:3])
    except Exception as e:
        print(f"Error {u}: {e}")

