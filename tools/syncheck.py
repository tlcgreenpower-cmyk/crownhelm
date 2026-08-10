# -*- coding: utf-8 -*-
"""Extract the module body and node --check it (no browser, no CDN)."""
import io, re, subprocess, sys, os
p = r"C:\Users\fresh1969\Desktop\Crownhelm\Crownhelm3D.html"
h = io.open(p, encoding="utf-8").read()
m = re.search(r'<script type="module">(.*?)</script>', h, re.S)
if not m:
    sys.exit("no module script found")
body = m.group(1)
body = body.replace("THREE=await import('three');", "THREE={};")
body = re.sub(r'^\s*import .*$', '', body, flags=re.M)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check.mjs")
io.open(out, "w", encoding="utf-8").write(body)
r = subprocess.run(["node", "--check", out], capture_output=True, text=True)
print("EXIT", r.returncode)
print(r.stdout[-3000:])
print(r.stderr[-3000:])
