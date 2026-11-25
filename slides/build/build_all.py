# -*- coding: utf-8 -*-
"""按页序写入幻灯片：图表页走 build_chart.py，其余页走 lark-cli +add-slide；任一页失败即停止。"""
import json
import shutil
import subprocess
import sys

DECK = "YOUR_DECK_ID"  # 替换为自己的演示文稿 ID
CHART_PAGES = {6, 9}
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
cli = shutil.which("lark-cli")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + "\n" + (p.stderr or "")


for n in range(start, 15):
    if n in CHART_PAGES:
        code, out = run([sys.executable, "build_chart.py", str(n)])
        print(f"--- page {n} (chart) ---")
        print(out[-1500:])
        if "ok: True" not in out:
            print("STOP at page", n)
            sys.exit(1)
    else:
        code, out = run([cli, "slides", "+add-slide", "--no-lint", "--presentation", DECK, "--slide", f"@slide-{n:02d}.xml"])
        print(f"--- page {n} ---")
        try:
            data = json.loads(out)
            print("ok:", data.get("ok"), "slide_id:", (data.get("data") or {}).get("slide_id"))
            if not data.get("ok") or not (data.get("data") or {}).get("slide_id"):
                print(out[-1500:])
                print("STOP at page", n)
                sys.exit(1)
        except Exception:
            print(out[-1500:])
            print("STOP at page", n, "(unparsable response)")
            sys.exit(1)
print("ALL DONE")
