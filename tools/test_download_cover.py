import urllib.request

url = 'http://www.nxbtre.com.vn/Images/Book/nxbtre_full_19462026_024602.jpg'
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        content = r.read()
        print(f"Downloaded full image: {len(content)} bytes")
except Exception as e:
    print(f"Failed full image, trying thumb: {e}")
    thumb_url = 'http://www.nxbtre.com.vn/Images/Book/nxbtre_thumb_19462026_024602.jpg'
    req2 = urllib.request.Request(thumb_url, headers=headers)
    try:
        with urllib.request.urlopen(req2, timeout=10) as r2:
            print(f"Downloaded thumb image: {len(r2.read())} bytes")
    except Exception as e2:
        print(f"Failed thumb: {e2}")

