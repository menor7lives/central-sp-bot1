import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import templates
for k, t in templates.TEMPLATES.items():
    print(k, "|", t.get("emoji"), "|", t.get("label"), "|", t.get("desc", "")[:70])
