import urllib.request
import json
import socket

domains = [
    'https://httpbin.org/get',
    'https://raw.githubusercontent.com',
    'https://images.unsplash.com',
    'https://covers.openlibrary.org/b/isbn/9780140328721-M.jpg',
    'https://upload.wikimedia.org',
    'https://books.google.com',
    'https://www.nxbtre.com.vn',
    'https://cdn0.fahasa.com',
    'https://salt.tikicdn.com'
]

for d in domains:
    try:
        req = urllib.request.Request(d, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as r:
            print(f"SUCCESS: {d} -> status {r.status}")
    except Exception as e:
        print(f"FAILED: {d} -> {e}")

