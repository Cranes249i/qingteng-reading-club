# -*- coding: utf-8 -*-
"""生成门口海报用的二维码：python tools/make_qr.py <站点网址>
上线拿到真实网址后重跑一次，把 assets/qr.png 换成真地址。"""
import os, sys
import segno

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.github.io/qingteng-reading/"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(root, "assets"), exist_ok=True)
out = os.path.join(root, "assets", "qr.png")
segno.make(url, error="m").save(out, scale=8, border=2, dark="#1f4a36", light="#ffffff")
print(f"二维码已生成：{out}\n指向：{url}")
