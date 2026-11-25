# -*- coding: utf-8 -*-
import sys

SKILL = r"C:\Users\youxu\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\ppt"
sys.path.insert(0, SKILL)
from scripts.gen_svg_charts import chart_slide
from scripts.svg_lib.atomize_svg_to_slide import publish_slide

DECK = "YOUR_DECK_ID"  # 替换为自己的演示文稿 ID


def run(page, frag):
    page_xml = open(f"slide-{page:02d}.xml", encoding="utf-8").read()
    r = publish_slide(page_xml, frag, presentation=DECK, page=page)
    print("ok:", r.get("ok"), "slide_id:", r.get("slide_id"))
    print("errors:", r.get("errors"))
    print("summary:", r.get("summary"))
    return r


if __name__ == "__main__":
    which = int(sys.argv[1])
    if which == 6:
        r1 = [{"x": 0, "y": 1}, {"x": 0.25, "y": 0.5}, {"x": 0.5, "y": 0}]
        r2 = [{"x": 0, "y": 0.5}, {"x": 0.5, "y": 0.25}, {"x": 1, "y": 0}]
        frag = chart_slide(
            "scatter", 40, 98, 530, 356,
            points=[
                {"name": "厂商 1 的反应曲线", "points": r1, "curve": r1, "marker": "none"},
                {"name": "厂商 2 的反应曲线", "points": r2, "curve": r2, "marker": "none"},
            ],
            x_title="厂商 1 的产量 q₁", y_title="厂商 2 的产量 q₂",
            fit=None, show_ci=False, end_labels=False,
            annotations=[{"x": 1 / 3, "y": 1 / 3, "text": "古诺均衡 (1/3, 1/3)"}],
            palette="coral_patient", font_family="微软雅黑",
        )
    else:
        pts = [{"x": n, "y": 1.0 / (n + 1)} for n in range(1, 21)]
        frag = chart_slide(
            "scatter", 40, 98, 530, 356,
            points=[{"name": "价格高于成本的部分", "points": pts, "curve": pts, "marker": "none"}],
            x_title="厂商数量 n", y_title="价格加成占 (a − c) 的比例",
            fit=None, show_ci=False,
            annotations=[
                {"x": 1, "y": 0.5, "text": "n＝1：垄断"},
                {"x": 2, "y": 1.0 / 3, "text": "n＝2：古诺"},
            ],
            reference_lines=[{"value": 0, "label": "完全竞争", "axis": "y"}],
            palette="coral_patient", font_family="微软雅黑",
        )
    run(which, frag)
