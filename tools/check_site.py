# -*- coding: utf-8 -*-
"""静态站自检：每个页面的编码/视口标签、站内链接是否都指向存在的文件、CSS 里有没有会让手机出横向滚动条的固定宽度。
用法：python tools/check_site.py   （在项目根目录运行；有错误退出码 1）"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
errors = []

for page in pages:
    html = open(os.path.join(ROOT, page), encoding="utf-8").read()
    if 'charset="utf-8"' not in html.lower():
        errors.append(f"{page}: 缺 <meta charset=\"utf-8\">，中文可能显示成乱码")
    if 'name="viewport"' not in html:
        errors.append(f"{page}: 缺 viewport 标签，手机上会显示成缩小的电脑版")
    if not re.search(r"<title>.+</title>", html):
        errors.append(f"{page}: 缺 <title>")
    for href in re.findall(r'(?:href|src)="([^"#]+)"', html):
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if not os.path.exists(os.path.join(ROOT, href)):
            errors.append(f"{page}: 链接指向的文件不存在 -> {href}")

css_path = os.path.join(ROOT, "style.css")
if os.path.exists(css_path):
    css = open(css_path, encoding="utf-8").read()
    for m in re.finditer(r"(?<![-\w])width\s*:\s*(\d+)px", css):
        if int(m.group(1)) > 480:
            errors.append(f"style.css: 固定宽度 {m.group(0)} 超过 480px，窄屏会出横向滚动条")

print(f"检查了 {len(pages)} 个页面：{', '.join(pages)}")
if errors:
    print(f"发现 {len(errors)} 个问题：")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("零问题：编码、视口、站内链接、固定宽度都正常")
