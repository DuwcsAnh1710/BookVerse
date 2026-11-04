from pathlib import Path

shortcode_file = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'content' / 'trang-chu-flatsome-shortcodes.txt'
text = shortcode_file.read_text(encoding='utf-8')

old_hero = '[section bg_color="#8B1E22" padding="60px" padding__sm="30px" class="hero-book-section"]'
new_hero = '[section bg="assets/hero-bookstore-bg.jpg" bg_overlay="rgba(55, 6, 9, 0.90)" padding="80px" padding__sm="40px" class="hero-book-section"]'

if old_hero in text:
    text = text.replace(old_hero, new_hero, 1)
    shortcode_file.write_text(text, encoding='utf-8')
    print("[OK] Updated trang-chu-flatsome-shortcodes.txt with hero-bookstore-bg.jpg!")

# Also update XML
xml_file = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'content' / 'duwcsanhlib-noi-dung.xml'
xml_text = xml_file.read_text(encoding='utf-8')
if old_hero in xml_text:
    xml_text = xml_text.replace(old_hero, new_hero, 1)
    xml_file.write_text(xml_text, encoding='utf-8')
    print("[OK] Updated duwcsanhlib-noi-dung.xml with hero-bookstore-bg.jpg!")

