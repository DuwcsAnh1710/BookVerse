"""Validate delivered files locally. Does not claim WooCommerce runtime success."""
import csv, json, re, hashlib, collections, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(condition,label):
    checks.append({'check':label,'result':'PASS' if condition else 'FAIL'})
    if not condition: print('FAIL:',label)
def csv_rows(name):
    p=ROOT/'data'/name
    check(p.read_bytes().startswith(b'\xef\xbb\xbf'),name+' UTF-8 BOM')
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
rows=csv_rows('san-pham.csv'); sources=csv_rows('nguon-sach.csv')
books=json.loads((ROOT/'data/books.json').read_text(encoding='utf-8'))
check(len(rows)==len(sources)==len(books)==25,'25 sản phẩm và 25 nguồn')
check(len({r['SKU'] for r in rows})==25,'SKU không trùng')
check(collections.Counter(r['Categories'] for r in rows)==collections.Counter({k:5 for k in ['Văn học','Kỹ năng và phát triển bản thân','Kinh tế và kinh doanh','Tâm lý và đời sống','Thiếu nhi']}),'5 danh mục, mỗi nhóm 5 sách')
check(all(None not in r and all(v is not None for v in r.values()) for r in rows),'CSV không lệch cột')
check(all(r['Images']=='' for r in rows),'Không hotlink ảnh')
check(all(r['Type']=='simple' and r['Tax status']=='none' and r['Backorders allowed?']=='0' for r in rows),'Sản phẩm đơn giản, không backorder, thuế demo tắt')
check(sum(int(r['Is featured?']) for r in rows)==5,'5 sản phẩm nổi bật')
check(all(r['Allow customer reviews?']=='0' for r in rows),'Không nhập đánh giá khách hàng')
check(all('http' not in r['Description'] and 'http' not in r['Short description'] for r in rows),'Nguồn nội bộ tách khỏi mô tả khách hàng')
check(all(not re.search(r'<(script|iframe|form)\b',r['Description'],re.I) for r in rows),'Mô tả không có script/iframe/form')
for b,r,s in zip(books,rows,sources):
    sku=b['sku']; digits=re.sub(r'\D','',b['isbn'])
    check(len(digits)==13 and sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(digits))%10==0,sku+' ISBN checksum (không thay thế đối chiếu nguồn)')
    check(sku==r['SKU']==s['SKU'] and r['Name']==b['title'],sku+' ánh xạ nguồn/sản phẩm')
    check(int(r['Regular price'])==b['demo_price']>0 and int(r['Stock'])==b['stock']>0,sku+' giá và tồn giả lập hợp lệ')
    check(r['Attribute 4 value(s)']==str(b['pages']) and r['Attribute 3 value(s)']==str(b['year']),sku+' số trang và năm khớp hồ sơ')
    check(',' not in r['Attribute 6 value(s)'],sku+' kích thước không bị tách theo dấu phẩy')
    check(s['URL nguồn']==b['url'] and b['url'].startswith('https://www.nxbtre.com.vn/sach/'),sku+' URL nguồn NXB cùng ấn bản')
    im=Image.open(ROOT/'assets/covers'/(sku+'.png')); im.verify()
    check(Image.open(ROOT/'assets/covers'/(sku+'.png')).size==(600,900),sku+' ảnh PNG 600×900 đọc được')
ns={'wp':'http://wordpress.org/export/1.2/','content':'http://purl.org/rss/1.0/modules/content/'}
root=ET.parse(ROOT/'content/noi-dung.xml').getroot(); items=root.findall('./channel/item')
check(len(items)==8,'WXR parse được, 8 nội dung')
check(collections.Counter(x.findtext('wp:post_type',namespaces=ns) for x in items)=={'page':5,'post':3},'WXR 5 trang và 3 blog')
check(all(x.findtext('wp:status',namespaces=ns)=='draft' for x in items),'WXR nhập dạng nháp')
check(all(not re.search(r'<(script|iframe|form)\b',x.findtext('content:encoded',namespaces=ns),re.I) for x in items),'WXR chỉ nội dung HTML cơ bản')
check(rows[0]['Name']=='Nhà Cũ Trong Phố Cũ','Tiếng Việt giữ nguyên qua vòng đọc CSV')
check(int(rows[0]['Regular price'])*2+25000==223000 and int(rows[24]['Regular price'])*3+25000==106000,'Phép tính 2 ca checkout tham chiếu (không chạy checkout)')
def luminance(h):
    v=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(x*w for x,w in zip(v,(.2126,.7152,.0722)))
ratios=[]
for fore,back in [('#2D241E','#FAF6EE'),('#675B50','#FAF6EE'),('#FFFFFF','#6B4226')]:
    a,b=sorted((luminance(fore),luminance(back))); ratio=(b+.05)/(a+.05)
    ratios.append(f'{fore} trên {back}: {ratio:.2f}:1'); check(ratio>=4.5,'Tương phản '+ratios[-1])
report={'date':'2026-11-04','scope':'Static data/artifact checks only; no WordPress, WooCommerce or Flatsome runtime','checks':checks,'summary':dict(collections.Counter(x['result'] for x in checks))}
(ROOT/'docs/kiem-tra-tu-dong.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
check(all(c['result']=='PASS' for c in checks),'Toàn bộ kiểm tra tĩnh đạt')
print(json.dumps(report['summary'],ensure_ascii=False)); print('\n'.join(ratios))
if any(c['result']=='FAIL' for c in checks): raise SystemExit(1)
