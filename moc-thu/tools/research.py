"""Fetch public publisher pages for edition verification; no image downloads."""
import sys, re, urllib.request, hashlib
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1] / 'research'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.text=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden += 1
        if tag=='a':
            a=dict(attrs)
            if a.get('href'): self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
    def handle_data(self, data):
        if not self.hidden and data.strip(): self.text.append(data.strip())

for url in sys.argv[1:]:
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=35) as res: raw=res.read().decode('utf-8')
        name=hashlib.sha256(url.encode()).hexdigest()[:12]
        ROOT.mkdir(exist_ok=True)
        (ROOT/(name+'.html')).write_text(raw,encoding='utf-8')
        p=Page(); p.feed(raw)
        text='\n'.join(p.text)
        (ROOT/(name+'.txt')).write_text(url+'\n'+text,encoding='utf-8')
        print('URL',url,'FILE',name)
        print(text[:22000] if len(sys.argv)>2 else '\n'.join(dict.fromkeys(p.links))[:24000])
    except Exception as exc: print(url, type(exc).__name__,str(exc))
