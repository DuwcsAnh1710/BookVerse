from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'duwcsanhlib' / 'tools' / 'validate.py'
text = p.read_text(encoding='utf-8')
old = "check((ROOT / 'duwcsanhlib' / 'docs' / '03-huong-dan-thiet-lap-landingpage-flatsome.md').exists(), \"H\u01b0\u1edbng d\u1eabn thi\u1ebft l\u1eadp Landing page Flatsome t\u1ed3n t\u1ea1i\")"
new = "check((ROOT / 'docs' / '03-huong-dan-thiet-lap-landingpage-flatsome.md').exists(), \"H\u01b0\u1edbng d\u1eabn thi\u1ebft l\u1eadp Landing page Flatsome t\u1ed3n t\u1ea1i\")"
assert old in text, 'old not found'
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print('validate.py path fixed!')
