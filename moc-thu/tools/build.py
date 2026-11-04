"""Build WooCommerce CSV, original text-card PNGs and WordPress WXR.
Run: python -X utf8 tools/build.py (requires Pillow only for PNG generation).
Does not access a website or change a WordPress installation.
"""
import csv, json, re, html, hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
books=json.loads((ROOT/'data/books.json').read_text(encoding='utf-8'))
def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

products=[]; sources=[]
for b in books:
    # Decimal commas would be interpreted as multiple attribute values by WooCommerce.
    size=b['size'].replace(',', '.').replace('x', ' × ')
    attrs=[('Tác giả',b['author']),('Nhà xuất bản',b['publisher']),('Năm xuất bản của lần in',b['year']),('Số trang',b['pages']),('Ngôn ngữ',b['language']),('Kích thước sách',size),('ISBN',b['isbn']),('Lần in',b['edition'])]
    p={'Type':'simple','SKU':b['sku'],'Name':b['title'],'Published':1,'Is featured?':b['featured'],'Visibility in catalog':'visible','Short description':b['short'],'Description':'<p>'+html.escape(b['description'])+'</p><p>Ảnh bìa minh họa. Sản phẩm trong mô hình học tập; giá và tồn kho giả lập, không thanh toán thật.</p>','Tax status':'none','In stock?':1,'Stock':b['stock'],'Low stock amount':2,'Backorders allowed?':0,'Sold individually?':0,'Allow customer reviews?':0,'Regular price':b['demo_price'],'Categories':b['category'],'Images':''}
    for n,(key,val) in enumerate(attrs,1):
        p.update({f'Attribute {n} name':key,f'Attribute {n} value(s)':val,f'Attribute {n} visible':1,f'Attribute {n} global':0})
    products.append(p)
    sources.append({'SKU':b['sku'],'Tên sách':b['title'],'Danh mục Mộc Thư':b['category'],'Tác giả':b['author'],'NXB':b['publisher'],'Số trang':b['pages'],'Năm lần in':b['year'],'Lần in':b['edition'],'ISBN nguồn':b['isbn'],'Kích thước':b['size'],'URL nguồn':b['url'],'Ngày tra cứu':b['accessed'],'Giá bán tham khảo tại nguồn (VND)':b['reference_price'],'Giá bán minh họa (VND)':b['demo_price'],'Tồn giả lập':b['stock'],'Ngôn ngữ đối chiếu':'Tiếng Việt — đối chiếu giới thiệu và thông tin ấn bản; không phải nhãn ngôn ngữ riêng trên nguồn','Ảnh giao kèm':f"assets/covers/{b['sku']}.png",'Nguồn ảnh':'Tự tạo bìa chữ cho bài Mộc Thư','Quyền ảnh':'Cho phép dùng/sửa/phân phối placeholder của gói; quyền bìa chính thức chưa xác định, không đóng gói','Ghi chú':'Một URL cho toàn bộ thông tin ấn bản; NXB Trẻ là đơn vị xuất bản trên website chính thức. Giá nguồn là nhãn Giá bán, không tự đổi thành Giá bìa.'})
write_csv(ROOT/'data/san-pham.csv',products)
write_csv(ROOT/'data/nguon-sach.csv',sources)

# Use installed Windows fonts; no font files are redistributed.
fontdir=Path('C:/Windows/Fonts')
def font(size,bold=False): return ImageFont.truetype(str(fontdir/('arialbd.ttf' if bold else 'arial.ttf')),size)
def wrapped(draw,text,f,max_width):
    lines=[]; line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if line and draw.textlength(candidate,font=f)>max_width: lines.append(line); line=word
        else: line=candidate
    if line: lines.append(line)
    return lines
def draw_lines(draw,lines,xy,f,fill,spacing):
    x,y=xy
    for line in lines: draw.text((x,y),line,font=f,fill=fill); y+=spacing
    return y
covers=ROOT/'assets/covers'; covers.mkdir(exist_ok=True)
colors=['#6B4226','#4C5D45','#684C43','#66503C','#3F615C']
for i,b in enumerate(books):
    im=Image.new('RGB',(600,900),'#FAF6EE'); d=ImageDraw.Draw(im); accent=colors[i//5]
    d.rectangle((0,0,26,900),fill=accent)
    d.text((65,54),'MỘC THƯ',font=font(29,True),fill=accent)
    d.line((65,115,535,115),fill=accent,width=2)
    f=font(36,True); lines=wrapped(d,b['title'],f,470)
    if len(lines)>8: f=font(31,True); lines=wrapped(d,b['title'],f,470)
    draw_lines(d,lines,(65,190),f,'#2D241E',47)
    draw_lines(d,wrapped(d,b['author'],font(24),460),(65,620),font(24),'#675B50',32)
    d.rectangle((65,775,535,831),fill=accent)
    d.text((86,787),'BÌA MINH HỌA',font=font(26,True),fill='white')
    d.text((65,852),b['sku']+'  •  Không phải bìa chính thức',font=font(18),fill='#675B50')
    im.save(covers/(b['sku']+'.png'),optimize=True)
logo=Image.new('RGBA',(720,180),(0,0,0,0)); d=ImageDraw.Draw(logo)
d.text((18,12),'Mộc Thư',font=font(112,True),fill='#6B4226'); logo.save(ROOT/'assets/logo-moc-thu.png')
banner=Image.new('RGB',(1200,800),'#F0E5D5'); d=ImageDraw.Draw(banner)
for i,b in enumerate(books[::5][:3]):
    c=Image.open(covers/(b['sku']+'.png')).resize((240,360))
    banner.paste(c,(170+i*310,180+(i%2)*55))
d.text((170,650),'Một góc đọc, dành riêng cho bạn.',font=font(42),fill='#2D241E')
banner.save(ROOT/'assets/banner-moc-thu.png',optimize=True)

# Basic semantic HTML only; not UX Builder elements or exported UX shortcodes.
def markdown_content(path):
    blocks=path.read_text(encoding='utf-8').strip().split('\n\n'); title=blocks.pop(0).removeprefix('# ')
    def inline(t): return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',html.escape(t))
    out=[]
    for text in blocks:
        if text.startswith('## '): out.append('<h2>'+inline(text[3:])+'</h2>')
        elif text.startswith('- '): out.append('<ul>'+''.join('<li>'+inline(x[2:])+'</li>' for x in text.splitlines())+'</ul>')
        else: out.append('<p>'+inline(text.replace('\n',' '))+'</p>')
    return title,'\n'.join(out)
ns={'wp':'http://wordpress.org/export/1.2/','content':'http://purl.org/rss/1.0/modules/content/','dc':'http://purl.org/dc/elements/1.1/','excerpt':'http://wordpress.org/export/1.2/excerpt/'}
for name,url in ns.items(): ET.register_namespace(name,url)
def sub(node,name,text):
    if ':' in name:
        prefix,local=name.split(':'); name='{'+ns[prefix]+'}'+local
    e=ET.SubElement(node,name); e.text=str(text); return e
rss=ET.Element('rss',version='2.0'); channel=ET.SubElement(rss,'channel')
sub(channel,'title','Mộc Thư — nội dung học tập'); sub(channel,'link','https://mocthu.example'); sub(channel,'description','Nội dung nguyên bản, không kèm sản phẩm hay ảnh từ xa')
sub(channel,'language','vi'); sub(channel,'wp:wxr_version','1.2'); sub(channel,'wp:base_site_url','https://mocthu.example'); sub(channel,'wp:base_blog_url','https://mocthu.example')
author=sub(channel,'wp:author',''); sub(author,'wp:author_id','1'); sub(author,'wp:author_login','moc-thu-demo'); sub(author,'wp:author_email','demo@mocthu.example'); sub(author,'wp:author_display_name','Mộc Thư — mô hình học tập')
files=['gioi-thieu','lien-he','giao-hang','doi-tra','bao-mat','blog-01','blog-02','blog-03']
for i,slug in enumerate(files,1):
    title,body=markdown_content(ROOT/'content'/(slug+'.md'))
    item=ET.SubElement(channel,'item'); sub(item,'title',title); sub(item,'link','https://mocthu.example/'+slug+'/'); sub(item,'dc:creator','moc-thu-demo')
    sub(item,'content:encoded',body); sub(item,'excerpt:encoded',''); sub(item,'wp:post_id',1000+i); sub(item,'wp:post_date','2026-11-04 09:00:00'); sub(item,'wp:post_date_gmt','2026-11-04 02:00:00')
    sub(item,'wp:comment_status','closed'); sub(item,'wp:ping_status','closed'); sub(item,'wp:post_name',slug); sub(item,'wp:status','draft'); sub(item,'wp:post_parent',0); sub(item,'wp:menu_order',0); sub(item,'wp:post_type','post' if slug.startswith('blog') else 'page'); sub(item,'wp:post_password',''); sub(item,'wp:is_sticky',0)
ET.indent(rss); ET.ElementTree(rss).write(ROOT/'content/noi-dung.xml',encoding='utf-8',xml_declaration=True)

# Evidence contains edition facts only, no complete copyrighted publisher text.
facts=['# Đối chiếu 25 ấn bản','Tra cứu trực tiếp website NXB Trẻ ngày 04/11/2026. Không tải ảnh bìa.\n']
for b in books:
    facts.extend([f"## {b['sku']} — {b['title']}",f"Nguồn: {b['url']}",f"Tác giả: {b['author']}; NXB: {b['publisher']}; {b['pages']} trang; khổ {b['size']}; ISBN {b['isbn']}; in lần {b['edition']} năm {b['year']}; Giá bán trên nguồn: {b['reference_price']:,} VND."])
    cached=ROOT/'research'/(hashlib.sha256(b['url'].encode()).hexdigest()[:12]+'.html')
    if cached.exists(): facts.append('SHA-256 bản HTML đã đọc (không phân phối toàn trang): '+hashlib.sha256(cached.read_bytes()).hexdigest())
(ROOT/'data/doi-chieu-an-ban.md').write_text('\n\n'.join(facts)+'\n',encoding='utf-8')
print('Built: 25 products, 25 sources, 25 covers, logo/banner, 8 draft WXR items')
