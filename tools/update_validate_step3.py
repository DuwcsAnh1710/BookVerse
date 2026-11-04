import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

val_file = Path('duwcsanhlib/tools/validate.py')
content = val_file.read_text(encoding='utf-8')

target = 'check((ROOT / \'docs\' / \'03-huong-dan-thiet-lap-landingpage-flatsome.md\').exists(), "Hướng dẫn thiết lập Landing page Flatsome tồn tại")'
replacement = target + '\n    check((ROOT / \'docs\' / \'04-huong-dan-toi-uu-shop-va-chi-tiet-san-pham.md\').exists(), "Hướng dẫn tối ưu Shop và Chi tiết sản phẩm tồn tại")'

if target in content and '04-huong-dan-toi-uu-shop-va-chi-tiet-san-pham.md' not in content:
    content = content.replace(target, replacement)
    val_file.write_text(content, encoding='utf-8')
    print("validate.py updated with 16th check!")
else:
    print("Already updated or target not found.")

