# -*- coding: utf-8 -*-
"""生成古诺模型课件 14 页的单页 XML（slide-01.xml ... slide-14.xml）。"""
import json

FONT = "微软雅黑"
BG = "rgb(250,245,240)"
INK = "rgb(46,32,38)"
ACC = "rgb(210,90,86)"
SEC = "rgb(160,110,105)"
MUT = "rgb(115,95,95)"
WHITE = "rgb(255,255,255)"
RULE = "rgb(214,200,194)"

COVER = "FILE_TOKEN_COVER"  # 替换为自己的上传返回值
SPRINGS = "FILE_TOKEN_SPRINGS"  # 替换为自己的上传返回值
PORTRAIT = "FILE_TOKEN_PORTRAIT"  # 替换为自己的上传返回值


def F(tex):
    return "<formula><latex><![CDATA[" + tex + "]]></latex></formula>"


def P(inner):
    return "<p>" + inner + "</p>"


def T(x, y, w, h, inner, size=20, color=INK, bold=False, align="left", ls="multiple:1.35", wrap=True, v="top"):
    b = ' bold="true"' if bold else ""
    nw = ' wrap="false"' if not wrap else ""
    return (
        f'<shape type="text" topLeftX="{x}" topLeftY="{y}" width="{w}" height="{h}">'
        f'<content textType="body" fontSize="{size}" fontFamily="{FONT}" color="{color}"{b} '
        f'textAlign="{align}" verticalAlign="{v}" lineSpacing="{ls}"{nw}>{inner}</content></shape>'
    )


def TITLE(t):
    return T(48, 34, 864, 52, P(t), size=30, bold=True, wrap=False, v="middle")


def L(x1, y1, x2, y2, color=SEC, w=2):
    return f'<line startX="{x1}" startY="{y1}" endX="{x2}" endY="{y2}"><border color="{color}" width="{w}"/></line>'


def E(cx, cy, r, fill, stroke=None):
    s = f'<border color="{stroke}" width="2"/>' if stroke else ""
    return (f'<shape type="ellipse" topLeftX="{cx - r}" topLeftY="{cy - r}" width="{2 * r}" height="{2 * r}">'
            f'<fill><fillColor color="{fill}"/></fill>{s}</shape>')


def RECT(x, y, w, h, fill):
    return f'<shape type="rect" topLeftX="{x}" topLeftY="{y}" width="{w}" height="{h}"><fill><fillColor color="{fill}"/></fill></shape>'


def TABLE(x, y, cols, rows, size=20, head_h=50, row_h=58):
    """rows: [(cells, is_header, highlight)]"""
    out = [f'<table topLeftX="{x}" topLeftY="{y}" width="{sum(cols)}" height="{head_h + row_h * (len(rows) - 1)}">',
           "<colgroup>" + "".join(f'<col width="{c}"/>' for c in cols) + "</colgroup>"]
    for i, (cells, head, hl) in enumerate(rows):
        h = head_h if head else row_h
        out.append(f'<tr height="{h}">')
        for c in cells:
            if head:
                fill = f'<fill><fillColor color="{INK}"/></fill>'
                color, bold = WHITE, True
            else:
                fill = f'<fill><fillColor color="rgba(210,90,86,0.14)"/></fill>' if hl else ""
                color, bold = INK, hl
            b = ' bold="true"' if bold else ""
            out.append(
                f'<td>{fill}<content textType="body" fontSize="{size}" fontFamily="{FONT}" color="{color}"{b} '
                f'textAlign="left" verticalAlign="middle" paddingLeft="14">{P(c)}</content></td>')
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


def S(body, note):
    paras = "".join(P(n) for n in note)
    return (
        '<slide xmlns="https://www.larkoffice.com/sml/2.0">'
        f'<style><fill><fillColor color="{BG}"/></fill></style><data>{body}</data>'
        f'<note><content textType="body" fontSize="14">{paras}</content></note></slide>'
    )


slides = {}

# 1 封面
slides[1] = S(
    f'<img src="{COVER}" topLeftX="0" topLeftY="0" width="960" height="540"/>'
    + T(230, 52, 520, 96, P("古诺模型"), 60, INK, True, "center", wrap=False, v="middle")
    + T(230, 152, 520, 56, P("重走一次知识创造"), 32, ACC, False, "center", wrap=False, v="middle")
    + T(180, 216, 600, 34, P("从 1838 年的两眼矿泉出发　·　寡头竞争专题"), 18, INK, False, "center", wrap=False, v="middle"),
    ["这节课讲古诺模型，但重点不是背结论，而是把古诺当年“造出”这个模型的过程拆开来看。",
     "画面里的两眼矿泉，就是他在 1838 年书中用的例子：两位业主卖同样的矿泉水，价格由两家共同的产量决定。"])

# 2 路线图
steps = [
    ("发现空白", "垄断与竞争之间，缺一段理论"),
    ("设定假设", "同质品、选产量、对手产量给定"),
    ("形式推演", "利润最大化，求出反应函数"),
    ("对照定位", "与垄断、完全竞争放在一起比"),
    ("接受批判", "换一条假设，结论还成立吗"),
    ("推广一般化", "推广到 n 家，写成含参数的模型"),
]
body = TITLE("这节课拆开看：古诺如何“造出”模型")
body += L(92, 170, 868, 170)
for i, (lab, desc) in enumerate(steps):
    cx = 92 + i * 155.2
    body += E(cx, 170, 18, INK)
    body += T(cx - 20, 158, 40, 26, P(str(i + 1)), 18, WHITE, True, "center", wrap=False, v="middle")
    body += T(cx - 72, 198, 144, 32, P(lab), 22, INK, True, "center", wrap=False, v="middle")
    body += T(cx - 72, 236, 144, 96, P(desc), 18, MUT, False, "center")
body += T(48, 380, 864, 80,
          P("学完之后，你应该能：<span bold=\"true\" color=\"rgb(210,90,86)\">自己改掉一条假设</span>，推出一个新的寡头模型，并说出它的适用范围。"),
          22, INK, False, "left", "multiple:1.4", v="middle")
slides[2] = S(body, [
    "整节课沿六个动作推进，每一步都对应古诺做过的一件事。",
    "请大家留意的不是每一步的名词，而是动作之间的顺序：先有问题，再有假设，然后才有公式。",
    "课后的任务会让你们自己把这六个动作再走一遍。",
])

# 3 发现空白
body = TITLE("第一步 · 发现空白：垄断与竞争之间")
body += T(48, 100, 610, 100,
          P("古典经济学把竞争当作背景：卖者一多，价格自然落回成本。于是理论只剩两个端点——一家独占，价格最高；无穷多家，价格等于成本。"),
          20, INK)
body += L(70, 262, 620, 262, SEC, 3)
body += E(70, 262, 6, INK) + E(620, 262, 6, INK)
body += L(345, 244, 345, 280, ACC, 4)
body += T(40, 278, 170, 30, P("垄断：1 家"), 18, INK, wrap=False)
body += T(470, 278, 180, 30, P("完全竞争：无穷多家"), 18, INK, False, "right", wrap=False)
body += T(245, 206, 200, 34, P("少数几家卖者"), 22, ACC, True, "center", wrap=False)
body += T(245, 286, 200, 30, P("没有理论"), 18, MUT, False, "center", wrap=False)
body += T(48, 366, 610, 84,
          P("古诺的提问：两家卖同一种矿泉水，价格会停在哪里？"), 22, ACC, True, "left", "multiple:1.35", v="middle")
body += f'<img src="{PORTRAIT}" topLeftX="712" topLeftY="108" width="170" height="239"><crop type="ellipse"/></img>'
body += T(680, 356, 236, 30, P("安托万·奥古斯丁·古诺"), 18, INK, True, "center", wrap=False)
body += T(680, 384, 236, 28, P("1801–1877"), 18, MUT, False, "center", wrap=False)
body += T(600, 414, 352, 60, P("1838 年出版") + P("《财富理论的数学原理研究》"), 18, MUT, False, "center", "multiple:1.25")
slides[3] = S(body, [
    "<!-- citation: [1][2] -->",
    "古诺是法国数学家，1838 年出版了《财富理论的数学原理研究》，书里第一次用函数和微分来处理“卖者”的竞争。",
    "他看到的问题是：当时的理论只会说“人多了价格就降”，但没有人写出只有两家、三家卖者时价格停在哪里。",
    "可以让学生先猜一猜：两家卖同样的水，价格是接近垄断，还是接近成本？先不给答案。",
])

# 4 设定假设
body = TITLE("第二步 · 设定假设：只留相互牵制")
body += f'<img src="{SPRINGS}" topLeftX="48" topLeftY="104" width="440" height="251"/>'
body += T(48, 362, 440, 56, P("古诺的原例：两位业主各有一眼矿泉，成本可以忽略。插图为课堂示意。"), 18, MUT)
items = [
    "两家厂商，出售同一种矿泉水",
    "每家决定自己的产量，价格由市场决定",
    "每家把对手的产量当作给定不变",
    "需求是线性的：" + F("p=a-bQ"),
    "每家的边际成本同为 " + F("c"),
]
for i, it in enumerate(items):
    y = 100 + i * 60
    body += T(520, y + 4, 36, 34, P(str(i + 1)), 22, ACC, True, "left", wrap=False)
    body += T(558, y, 354, 56, P(it), 20, INK, False, "left", "multiple:1.25", v="middle")
body += T(48, 428, 864, 60,
          P("知识创造的要点：假设不求“符合现实”，而是判断——哪些细节与“相互牵制”无关，可以大胆删掉。"),
          20, INK, False, "left", "multiple:1.3", v="middle")
slides[4] = S(body, [
    "<!-- citation: [1] -->",
    "古诺的原例是矿泉水：两位业主各有一眼泉，水是同一种，取水成本几乎为零。",
    "请注意这五条假设各自删掉了什么：产品差异、定价行为、策略互动、需求形状和成本差异。",
    "可以问学生：这五条里，哪一条是“相互牵制”真正需要的？答案是第三条——把对手的产量当作给定。",
])

# 5 推演一
body = TITLE("第三步 · 推演：写出各自的反应函数")
body += T(48, 102, 520, 30, P("厂商 1 的利润＝（价格 − 成本）× 产量"), 20, MUT)
body += T(48, 134, 520, 54, P(F(r"\pi_1=\left[a-b\left(q_1+q_2\right)-c\right]q_1")), 28, INK, v="middle")
body += T(48, 200, 520, 30, P("对自己的产量 " + F("q_1") + " 求导，并令导数为零"), 20, MUT)
body += T(48, 232, 520, 48, P(F(r"a-c-2bq_1-bq_2=0")), 28, INK, v="middle")
body += T(48, 296, 520, 30, P("解出厂商 1 的反应函数"), 20, MUT)
body += T(48, 328, 520, 56, P(F(r"q_1=\frac{a-c-bq_2}{2b}")), 28, INK, v="middle")
body += T(48, 396, 520, 56, P("厂商 2 同理，只需把下标 1、2 对调。"), 18, MUT)
body += L(580, 104, 580, 404, RULE, 2)
body += T(608, 100, 304, 100,
          P("读法一：对手每多生产 1 单位，我就少生产半个单位。"), 20, INK, False, "left", "multiple:1.35")
body += T(608, 206, 304, 140,
          P("读法二：它还不是答案。它说的是——“如果对手生产这么多，我最好生产那么多”。"), 20, INK, False, "left", "multiple:1.35")
body += T(608, 348, 304, 70,
          P("两家的最优反应要同时成立，才叫均衡。"), 20, ACC, True, "left", "multiple:1.35")
slides[5] = S(body, [
    "<!-- citation: [3] -->",
    "推导只有三步：写利润，对产量求导，解出自己的产量。",
    "得到的关系叫反应函数，它把“我的最优产量”写成“对手产量”的函数。",
    "提醒学生：反应函数不是均衡，它只是半张答卷；均衡要等下一页两家的反应函数相交。",
])

# 6 推演二（图表页，由 build_p06.py 写入）
body = TITLE("第三步 · 推演：两条反应曲线的交点")
body += T(40, 462, 530, 30,
          P("图 1 · 反应曲线与古诺均衡（横纵轴均以 " + F(r"(a-c)/b") + " 为单位）"), 18, MUT, False, "center", wrap=False)
body += T(596, 104, 316, 30, P("两个反应函数同时成立，解得"), 18, MUT)
body += T(596, 134, 316, 58, P(F(r"q_1^{*}=q_2^{*}=\frac{a-c}{3b}")), 28, INK, v="middle")
body += T(596, 192, 316, 58, P(F(r"p^{*}=\frac{a+2c}{3}")), 28, INK, v="middle")
body += T(596, 262, 316, 76, P("在这一点，任何一家单独改变产量都会吃亏。"), 20, INK, False, "left", "multiple:1.35")
body += T(596, 342, 316, 110,
          P("一百多年后，纳什把这种“谁都不愿单独改变”的状态叫作均衡；古诺均衡是它最早的例子之一。"),
          20, INK, False, "left", "multiple:1.35")
slides[6] = S(body, [
    "<!-- citation: [3][10] -->",
    "横轴是厂商 1 的产量，纵轴是厂商 2 的产量，两条直线分别是两家的反应函数。",
    "两条线的交点就是古诺均衡：每家生产 (a − c)/3b，总产量是 2(a − c)/3b，价格是 (a + 2c)/3。",
    "可以带学生走一遍“调整过程”：从任意一点出发，两家交替按反应曲线移动，会逐步收敛到交点。",
])

# 7 对照
rows = [
    (["市场结构", "每家产量", "行业总产量", "价格", "行业总利润"], True, False),
    (["垄断（1 家）", F(r"\frac{a-c}{2b}"), F(r"\frac{a-c}{2b}"), F(r"\frac{a+c}{2}"), F(r"\frac{(a-c)^2}{4b}")], False, False),
    (["古诺双寡头（2 家）", F(r"\frac{a-c}{3b}"), F(r"\frac{2(a-c)}{3b}"), F(r"\frac{a+2c}{3}"), F(r"\frac{2(a-c)^2}{9b}")], False, True),
    (["完全竞争（无穷多家）", "趋于 0", F(r"\frac{a-c}{b}"), F("c"), "0"], False, False),
]
body = TITLE("第四步 · 对照：落在垄断与竞争之间")
body += TABLE(48, 96, [230, 150, 180, 140, 164], rows, size=20, head_h=50, row_h=60)
body += T(48, 340, 864, 70,
          P("只多出一个竞争者，行业总产量就增加三分之一，价格与行业利润随之下降；但离完全竞争还差三分之一。"),
          20, INK, False, "left", "multiple:1.35", v="middle")
body += T(48, 418, 864, 50,
          P("知识创造的要点：新结论只有放进已知结论的坐标系里，才显出它的位置和价值。"),
          22, ACC, True, "left", "multiple:1.3", v="middle")
slides[7] = S(body, [
    "<!-- citation: [4] -->",
    "把垄断、古诺和完全竞争三行并排：古诺的总产量是 2/3，正好在垄断的 1/2 和完全竞争的 1 之间。",
    "价格也一样：垄断加成是一半，古诺是三分之一，完全竞争为零。",
    "这一步是知识创造里最容易被忽略的一步——对照。没有对照，一个数字只是数字；有了对照，它才是一个有位置的结论。",
])

# 8 批判
body = TITLE("第五步 · 批判：换一条假设，结论就变")
body += T(48, 100, 420, 76, P("1883 年，伯特兰在书评里提出：厂商明明是在定价格，不是定产量。"), 20, INK, False, "left", "multiple:1.35")
body += T(48, 184, 420, 104,
          P("如果两家定价格、产品又完全相同——只要我的价格略高于成本，对手稍降一点就能抢走全部生意。"),
          20, INK, False, "left", "multiple:1.35")
body += T(48, 296, 420, 76, P("结果：价格直接跌到成本，两家利润为零。"), 22, ACC, True, "left", "multiple:1.35", v="middle")
body += T(48, 372, 420, 76, P("只有两家卖者，却得到了完全竞争的结果。这就是“伯特兰悖论”。"), 18, INK, False, "left", "multiple:1.35")
body += L(496, 104, 496, 430, RULE, 2)
body += T(520, 100, 392, 70, P("批评没有推翻古诺，而是指出："), 20, INK, True, "left", "multiple:1.3", v="middle")
body += T(520, 166, 392, 56, P("此后每一种新模型，几乎都是改掉古诺的某一条假设。"), 18, MUT, False, "left", "multiple:1.3")
crit = [
    ("霍特林（1929）", "产品有位置差异 → 改“同质”"),
    ("斯塔克尔伯格（1934）", "一先一后决策 → 改“同时”"),
    ("张伯伦（1933）", "卖者意识到相互依赖 → 改“对手产量给定”"),
]
for i, (who, what) in enumerate(crit):
    y = 236 + i * 68
    body += T(520, y, 392, 30, P(who), 20, INK, True, wrap=False)
    body += T(520, y + 30, 392, 34, P(what), 18, SEC, wrap=False)
body += T(48, 462, 864, 40, P("知识创造的要点：一条反例，就是一个新模型的入口。"), 22, ACC, True, "left", v="middle")
slides[8] = S(body, [
    "<!-- citation: [5][6] -->",
    "伯特兰的批评只有一句话：厂商选的是价格，不是产量。",
    "按价格竞争重新推一遍，结论变成价格等于成本、利润为零，这被称为伯特兰悖论。",
    "这里的教训是：批评没有杀死古诺模型，而是揭示了结论依赖哪一条假设；之后几十年的寡头理论，基本都是在改古诺的假设。",
])

# 9 推广一（图表页，由 build_p09.py 写入）
body = TITLE("第六步 · 推广：厂商数量连起两个极端")
body += T(40, 462, 530, 30, P("图 2 · 价格加成随厂商数量的变化（按公式计算）"), 18, MUT, False, "center", wrap=False)
body += T(596, 100, 316, 30, P("推广到 n 家厂商，均衡变为"), 18, MUT)
body += T(596, 130, 316, 54, P(F(r"Q^{*}=\frac{n}{n+1}\cdot\frac{a-c}{b}")), 26, INK, v="middle")
body += T(596, 186, 316, 54, P(F(r"p^{*}-c=\frac{a-c}{n+1}")), 26, INK, v="middle")
body += T(596, 254, 316, 84,
          P("n＝1 回到垄断，n＝2 是古诺，n 趋于无穷时价格趋近成本。"), 20, INK, False, "left", "multiple:1.35")
body += T(596, 340, 316, 112,
          P("“竞争程度”不再是定性标签，而是可以用厂商数量刻画、可以取极限的变量。"),
          20, ACC, True, "left", "multiple:1.35")
slides[9] = S(body, [
    "<!-- citation: [7] -->",
    "把两家推广到 n 家，每家产量是 (a − c)/[(n+1)b]，价格高于成本的部分是 (a − c)/(n+1)。",
    "这张图是按公式算出来的：厂商越多，加成越薄，但下降速度越来越慢。",
    "这是古诺最重要的创造：垄断和完全竞争不再是两种互不相干的市场，而是同一条曲线上的两个点。",
])

# 10 推广二
body = TITLE("第六步 · 推广：一个参数装下竞争与合谋")
body += T(48, 96, 864, 60,
          P("后人把“对手产量给定”改写成一个猜想：我多生产 1 单位时，预计对手会跟着变动多少？记这个量为 " + F("v") + "。"),
          20, INK, False, "left", "multiple:1.3", v="middle")
body += T(48, 154, 400, 62, P(F(r"q=\frac{a-c}{(3+v)\,b}")), 30, INK, v="middle")
body += T(430, 154, 482, 62, P("每家厂商的均衡产量"), 20, MUT, False, "left", v="middle")
rows = [
    (["v 的取值", "含义", "每家产量", "行业总产量"], True, False),
    ([F("v=0"), "对手不回应（古诺）", F(r"\frac{a-c}{3b}"), F(r"\frac{2(a-c)}{3b}")], False, False),
    ([F("v=1"), "对手等量跟随（合谋）", F(r"\frac{a-c}{4b}"), F(r"\frac{a-c}{2b}")], False, True),
]
body += TABLE(48, 228, [150, 300, 190, 224], rows, size=20, head_h=48, row_h=56)
body += T(48, 354, 864, 60,
          P(F("v=1") + " 时行业总产量等于垄断产量：谁都知道多卖会引来报复，谁也就不敢多卖。"),
          20, INK, False, "left", "multiple:1.3", v="middle")
body += T(48, 416, 864, 60,
          P("知识创造的要点：把一条“非此即彼”的假设换成可取值的参数，模型就从解释一种情况，变成解释一整族情况。"),
          22, ACC, True, "left", "multiple:1.3", v="middle")
slides[10] = S(body, [
    "<!-- citation: [8] -->",
    "把“对手不会理我”这条硬假设，换成一个参数 v：我多卖一单位，对手会跟着变动多少。",
    "代入利润最大化，得到 q＝(a − c)/[(3＋v)b]。v 取 0 就是古诺；v 取 1 时行业产量正好是垄断产量。",
    "经济学里把这类猜想叫作推测变差；它说明一个模型可以同时容纳竞争与合谋两种结果。",
])

# 11 时间线
tl = [
    ("1838", "出版，同时代人读不懂其中的数学"),
    ("1883", "伯特兰发表批评性书评"),
    ("1897", "英译本出版，费雪编制文献目录"),
    ("1929", "霍特林改造；1934 年斯塔克尔伯格提出领导者模型"),
    ("1950", "纳什：古诺均衡是纳什均衡的特例"),
    ("1960s", "实验经济学在实验室里检验古诺与伯特兰"),
]
body = TITLE("一个模型的后半生：被冷落、被批评、被命名")
body += L(90, 250, 870, 250, SEC, 3)
for i, (yr, desc) in enumerate(tl):
    cx = 90 + i * 156
    body += E(cx, 250, 9, ACC)
    body += T(cx - 74, 196, 148, 40, P(yr), 26, INK, True, "center", wrap=False, v="middle")
    body += T(cx - 74, 272, 148, 104, P(desc), 18, MUT, False, "center", "multiple:1.25")
body += T(48, 396, 864, 70,
          P("知识生成不等于“提出那一刻就被承认”：出版、批评、转译、再命名，都是创造的一部分。"),
          22, ACC, True, "left", "multiple:1.3", v="middle")
slides[11] = S(body, [
    "<!-- citation: [5][6][9][10][11] -->",
    "这本 1838 年的书在古诺生前几乎没有反响，他在 1863 年用通俗语言重写了一遍，仍然没有引起重视。",
    "真正的转机来自三件事：1883 年伯特兰的批评性书评，1897 年的英译本，以及二十世纪博弈论的重新表述。",
    "可以让学生讨论：如果一项成果要等几十年才被理解，作者、同行和教科书各起了什么作用？",
])

# 12 复盘
rows = [(["动作", "古诺做了什么", "你可以怎样练习"], True, False)]
data = [
    ("发现空白", "指出垄断与竞争之间的“少数几家”没有理论", "找到现有理论解释不了的中间地带"),
    ("设定假设", "同质品、选产量、对手产量给定", "写下假设，并说明为什么保留它"),
    ("形式推演", "利润最大化，求出反应函数与交点", "把假设变成可以求解的关系式"),
    ("对照定位", "与垄断、完全竞争的结果并排比较", "把新结果放进已知结论的坐标系"),
    ("接受批判", "伯特兰改选价格，得到悖论", "主动改一条假设，检验结论是否稳健"),
    ("推广一般化", "推广到 n 家，写成含参数的模型", "把特例推广为一族模型"),
]
for a, b, c in data:
    rows.append(([a, b, c], False, False))
body = TITLE("复盘：知识创造的六个动作")
body += TABLE(48, 88, [140, 350, 374], rows, size=18, head_h=46, row_h=56)
slides[12] = S(body, [
    "这张表把整节课收拢起来：左边是动作，中间是古诺的做法，右边是学生在自己的练习里可以做的事。",
    "六个动作可以迁移到其他模型：伯特兰、霍特林、斯塔克尔伯格，走的都是同一条路。",
    "建议让学生用这张表自查课后的任务，看自己是不是每一步都做了。",
])

# 13 课堂任务
body = TITLE("课堂任务：轮到你做一次知识创造")
body += T(48, 96, 864, 70,
          P("两人一组，从下面三条中选一条，改掉古诺的一条假设，推出新的均衡，再与古诺结果对照。时间 25 分钟。"),
          22, INK, False, "left", "multiple:1.3", v="middle")
opts = [
    ("A", "两家成本不同：" + F("c_1\\neq c_2") + "。各自的均衡产量是多少？成本更低的一家多生产多少？"),
    ("B", "政府按每单位征税 " + F("t") + "：新的价格是多少？税由谁负担，消费者承担几分之几？"),
    ("C", "三家厂商、成本相同：求出均衡产量，并试着归纳 " + F("n") + " 家时的一般公式。"),
]
for i, (k, txt) in enumerate(opts):
    y = 184 + i * 74
    body += T(48, y, 48, 44, P(k), 28, ACC, True, "left", wrap=False, v="middle")
    body += T(100, y, 812, 60, P(txt), 20, INK, False, "left", "multiple:1.25", v="middle")
body += L(48, 414, 912, 414, RULE, 2)
body += T(48, 426, 864, 60,
          P("提交一张纸，写清四项：新假设、推导过程、与古诺结果的对照、你认为的模型局限。"),
          20, INK, False, "left", "multiple:1.3", v="middle")
slides[13] = S(body, [
    "任务的目的不是得到标准答案，而是完整走一遍六个动作。",
    "巡视时可以只问两个问题：你改掉的是哪一条假设？你的结果和古诺差在哪里？",
    "参考答案供教师使用：A 题两家产量分别为 (a − 2c₁ + c₂)/3b 和 (a − 2c₂ + c₁)/3b；B 题价格上升 t/3，消费者承担三分之一；C 题每家产量为 (a − c)/4b。",
])

# 14 结尾
body = RECT(72, 96, 84, 6, ACC)
body += T(72, 122, 816, 150,
          P("知识不是被“找到”的，是在假设的缝隙里被“造”出来的。"), 40, INK, True, "left", "multiple:1.3", v="middle")
body += T(72, 288, 816, 44,
          P("古诺模型 ＝ 一个空白的问题 ＋ 五条克制的选择 ＋ 一次可以检验的推演"), 24, ACC, False, "left", wrap=False)
body += T(72, 356, 816, 70,
          P("延伸阅读：古诺《财富理论的数学原理研究》（1838）；泰勒尔《产业组织理论》（1988）。"),
          20, MUT, False, "left", "multiple:1.3")
slides[14] = S(body, [
    "<!-- citation: [1] -->",
    "最后回到主题：古诺模型的价值不只在那个公式，而在于它示范了知识是怎样被造出来的。",
    "一个没人回答的问题，五条敢于删繁就简的假设，一次经得起对照和批评的推演。",
    "希望学生带走的不是 q＝(a − c)/3b，而是这六个动作。",
])

for n, xml in slides.items():
    with open(f"slide-{n:02d}.xml", "w", encoding="utf-8") as f:
        f.write(xml)

refs = {
    "references": [
        {"id": 1, "fact": "古诺 1838 年出版《财富理论的数学原理研究》，首次用函数与微分分析卖者的竞争，书中以矿泉水双寡头为例",
         "sources": [
             {"source": "Internet Archive 全文", "locator": "Bacon 1897 英译本卷首", "evidence": "His Principes mathématiques having met with little or no success, in 1863 he paraphrased it in popular language"},
             {"source": "维基百科 Cournot competition", "locator": "History", "evidence": "first outlined his theory of competition in his 1838 volume ... describing the competition with a market for spring water dominated by two suppliers (a duopoly)"}],
         "kind": "direct", "status": "已出版著作"},
        {"id": 2, "fact": "古诺生于 1801 年，卒于 1877 年",
         "sources": [
             {"source": "HandWiki: Antoine Augustin Cournot", "locator": "首段", "evidence": "Born 28 August 1801 ... Died 31 March 1877"}],
         "kind": "direct", "status": "传记资料"},
        {"id": 3, "fact": "线性需求 p=a−bQ、边际成本 c 下，双寡头反应函数 q₁=(a−c−bq₂)/2b，均衡 q₁*=q₂*=(a−c)/3b，p*=(a+2c)/3",
         "sources": [], "kind": "calculated", "status": "按模型假设推导",
         "derivation": "π₁=[a−b(q₁+q₂)−c]q₁，对 q₁ 求偏导得 a−c−2bq₁−bq₂=0；对称解 q=(a−c)/3b，代入需求得 p=a−2(a−c)/3=(a+2c)/3。"},
        {"id": 4, "fact": "垄断、古诺双寡头、完全竞争的行业总产量分别为 (a−c)/2b、2(a−c)/3b、(a−c)/b，价格加成分别为 (a−c)/2、(a−c)/3、0",
         "sources": [], "kind": "calculated", "status": "按模型假设推导",
         "derivation": "垄断：max (a−bQ−c)Q 得 Q=(a−c)/2b；完全竞争 p=c 得 Q=(a−c)/b；与 [3] 对照。"},
        {"id": 5, "fact": "伯特兰 1883 年发表书评，批评古诺模型应以价格而非产量为厂商的选择变量",
         "sources": [{"source": "用户消息以外的通识", "locator": "", "evidence": "Bertrand, J. (1883), Journal des Savants 书评"}],
         "kind": "direct", "status": "教科书通行叙述，未在本轮联网核对"},
        {"id": 6, "fact": "霍特林 1929、张伯伦 1933、斯塔克尔伯格 1934 分别在位置差异、产品差异化、先后决策方向上改造寡头模型",
         "sources": [], "kind": "direct", "status": "教科书通行叙述，未在本轮联网核对"},
        {"id": 7, "fact": "n 家同成本厂商的古诺均衡：行业总产量 n(a−c)/[(n+1)b]，价格高于成本 (a−c)/(n+1)",
         "sources": [], "kind": "calculated", "status": "按模型假设推导",
         "derivation": "对称均衡下 a−c−b(n+1)q=0，得 q=(a−c)/[(n+1)b]，Q=nq，p−c=a−bQ−c=(a−c)/(n+1)。"},
        {"id": 8, "fact": "推测变差形式下每家均衡产量 q=(a−c)/[(3+v)b]；v=0 为古诺，v=1 时行业产量等于垄断产量",
         "sources": [], "kind": "calculated", "status": "按模型假设推导",
         "derivation": "令 q₂=q+v q₁ 代入一阶条件 a−c−2bq₁−bq₂−bq₁ dq₂/dq₁=0，对称解 q(3+v)=(a−c)/b。"},
        {"id": 9, "fact": "1897 年古诺著作英译本出版，Nathaniel T. Bacon 翻译，Irving Fisher 编制数理经济学文献目录；原书在古诺生前收效甚微，1863 年以通俗语言重写",
         "sources": [
             {"source": "Internet Archive 全文", "locator": "卷首译序", "evidence": "TRANSLATED BY NATHANIEL T. BACON / BIBLIOGRAPHY OF MATHEMATICAL ECONOMICS / BY IRVING FISHER / 1897"},
             {"source": "Internet Archive 全文", "locator": "卷首译序", "evidence": "His Principes mathématiques having met with little or no success, in 1863 he paraphrased it in popular language"}],
         "kind": "direct", "status": "已出版著作"},
        {"id": 10, "fact": "纳什 1950 年提出非合作博弈均衡概念，古诺均衡被视为纳什均衡的早期特例",
         "sources": [], "kind": "direct", "status": "教科书通行叙述，未在本轮联网核对"},
        {"id": 11, "fact": "1960 年代 Fouraker 与 Siegel 等人在实验室中检验寡头（产量与价格）竞争",
         "sources": [{"source": "斯坦福 Alvin Roth 实验经济学史页面", "locator": "A. Industrial organization", "evidence": "Fouraker, Lawrence E., Martin Shubik, and Sidney Siegel. 1961. Oligopoly Bargaining: The Quantity Adjuster Models ... Fouraker, Lawrence E. and Sidney Siegel. 1963. Bargaining Behavior"}],
         "kind": "direct", "status": "已发表研究"},
    ],
    "gaps": ["伯特兰 1883 年书评、霍特林 1929、张伯伦 1933、斯塔克尔伯格 1934、纳什 1950 的具体出处为教科书通行说法，本轮未逐条联网核对。"],
}
with open("references.json", "w", encoding="utf-8") as f:
    json.dump(refs, f, ensure_ascii=False, indent=2)
print("ok", len(slides))
