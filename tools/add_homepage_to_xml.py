import sys
from pathlib import Path
import xml.etree.ElementTree as ET

xml_path = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'content' / 'duwcsanhlib-noi-dung.xml'
shortcode_path = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'content' / 'trang-chu-flatsome-shortcodes.txt'

shortcode_text = shortcode_path.read_text(encoding='utf-8')
xml_text = xml_path.read_text(encoding='utf-8')

homepage_item = f"""    <item>
      <title>Trang chủ — DuwcsAnhLib</title>
      <link>http://duwcsanhlib.vn/</link>
      <dc:creator>duwcsanhlib</dc:creator>
      <content:encoded><![CDATA[{shortcode_text}]]></content:encoded>
      <excerpt:encoded />
      <wp:post_id>2000</wp:post_id>
      <wp:post_date>2026-11-04 10:00:00</wp:post_date>
      <wp:post_date_gmt>2026-11-04 03:00:00</wp:post_date_gmt>
      <wp:comment_status>closed</wp:comment_status>
      <wp:ping_status>closed</wp:ping_status>
      <wp:post_name>trang-chu</wp:post_name>
      <wp:status>publish</wp:status>
      <wp:post_parent>0</wp:post_parent>
      <wp:menu_order>0</wp:menu_order>
      <wp:post_type>page</wp:post_type>
      <wp:post_password />
      <wp:is_sticky>0</wp:is_sticky>
    </item>
"""

# Check if already added
if '<wp:post_name>trang-chu</wp:post_name>' not in xml_text:
    target = '    <item>\n      <title>Về DuwcsAnhLib</title>'
    assert target in xml_text, "Target item not found in XML"
    xml_text = xml_text.replace(target, homepage_item + target, 1)
    xml_path.write_text(xml_text, encoding='utf-8')
    print("Successfully added Trang chu to duwcsanhlib-noi-dung.xml!")
else:
    print("Trang chu already present in XML.")

