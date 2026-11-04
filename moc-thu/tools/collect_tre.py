"""Research only: read public edition metadata, retaining local evidence."""
import urllib.request, hashlib, json, time
from pathlib import Path
from research import Page
ROOT=Path(__file__).resolve().parents[1]/'research'
cats=['van-hoc-trong-nuoc','phat-trien-ban-than-nghe-thuat-song','kinh-te','tam-ly-giao-duc','sach-thieu-nhi']
def fetch(url):
    stem=hashlib.sha256(url.encode()).hexdigest()[:12]
    path=ROOT/(stem+'.html')
    if path.exists(): raw=path.read_text(encoding='utf-8')
    else:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=25) as response: raw=response.read().decode('utf-8')
        path.write_text(raw,encoding='utf-8'); time.sleep(.3)
    p=Page(); p.feed(raw)
    text='\n'.join(p.text)
    (ROOT/(stem+'.txt')).write_text(url+'\n'+text,encoding='utf-8')
    return p,text
rows=[]
for cat in cats:
    url='https://www.nxbtre.com.vn/tu-sach/'+cat+'/'
    try:
        p,_=fetch(url)
        links=list(dict.fromkeys(x for x in p.links if ('/sach/' in x or '/xem-them/' in x) and '.html' in x))[:7]
        for link in links:
            if link.startswith('/'): link='https://www.nxbtre.com.vn'+link
            try:
                detail,t=fetch(link)
                if '/xem-them/' in link:
                    full=next((x for x in detail.links if '/sach/' in x and '.html' in x),None)
                    if full:
                        link=('https://www.nxbtre.com.vn'+full) if full.startswith('/') else full
                        _,t=fetch(link)
                start=t.find('Tác giả:'); end=t.find('Giới thiệu tóm tắt')
                row={'category':cat,'url':link,'title':t.splitlines()[0],'metadata':t[start:end], 'intro':t[end:end+4000]}
                rows.append(row)
                print(json.dumps({k:v for k,v in row.items() if k!='intro'},ensure_ascii=False),flush=True)
            except Exception as e: print('ERROR',link,str(e),flush=True)
    except Exception as e: print('ERROR CATEGORY',cat,str(e),flush=True)
    (ROOT/'candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
