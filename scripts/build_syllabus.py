# -*- coding: utf-8 -*-
"""生成《产业组织理论课程大纲》Word 文档。"""
import pathlib

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BLACK = RGBColor(0, 0, 0)
SONG, HEI, TNR = '宋体', '黑体', 'Times New Roman'
OUT = pathlib.Path(__file__).resolve().parent.parent / '产业组织理论课程大纲.docx'


def set_rfonts(el_rpr, zh, en):
    rfonts = el_rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        el_rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), en)
    rfonts.set(qn('w:hAnsi'), en)
    rfonts.set(qn('w:eastAsia'), zh)
    rfonts.set(qn('w:cs'), en)


def style_font(style, zh, en, size, bold=False):
    style.font.name = en
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = BLACK
    set_rfonts(style.element.get_or_add_rPr(), zh, en)


def run_font(run, zh, en, size, bold=False):
    run.font.name = en
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = BLACK
    set_rfonts(run._element.get_or_add_rPr(), zh, en)


doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
for side in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
    setattr(sec, side, Cm(2.5))

# 样式
st = doc.styles
style_font(st['Normal'], SONG, TNR, 12)
pf = st['Normal'].paragraph_format
pf.line_spacing = 1.5
pf.space_after = Pt(4)
pf.first_line_indent = Pt(24)
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

style_font(st['Title'], HEI, TNR, 18, bold=True)
tpf = st['Title'].paragraph_format
tpf.alignment = WD_ALIGN_PARAGRAPH.CENTER
tpf.space_after = Pt(12)
tpf.first_line_indent = Pt(0)
tpf.line_spacing = 1.5
tpPr = st['Title'].element.get_or_add_pPr()
for b in tpPr.findall(qn('w:pBdr')):
    tpPr.remove(b)

for name, size, before, after in (('Heading 1', 14, 10, 5), ('Heading 2', 12, 8, 4)):
    style_font(st[name], HEI, TNR, size, bold=True)
    hpf = st[name].paragraph_format
    hpf.space_before = Pt(before)
    hpf.space_after = Pt(after)
    hpf.first_line_indent = Pt(0)
    hpf.left_indent = Pt(0)
    hpf.line_spacing = 1.5
    hpf.keep_with_next = True


def body(text):
    p = doc.add_paragraph(text, style='Normal')
    run_font(p.runs[0], SONG, TNR, 12)
    return p


def h1(text):
    p = doc.add_heading(text, level=1)
    run_font(p.runs[0], HEI, TNR, 14, True)
    return p


def h2(text):
    p = doc.add_heading(text, level=2)
    run_font(p.runs[0], HEI, TNR, 12, True)
    return p


def plain(text, size=10.5, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, keep=False):
    p = doc.add_paragraph(style='Normal')
    pfm = p.paragraph_format
    pfm.first_line_indent = Pt(0)
    pfm.left_indent = Pt(0)
    pfm.right_indent = Pt(0)
    pfm.alignment = align
    pfm.line_spacing = 1.0
    pfm.space_before = Pt(4)
    pfm.space_after = Pt(4)
    pfm.keep_with_next = keep
    r = p.add_run(text)
    run_font(r, SONG, TNR, size, bold)
    return p


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def fill_cell(cell, text, width, center=False, bold=False, fill=None):
    cell.width = Cm(width)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    if fill:
        shade(cell, fill)
    p = cell.paragraphs[0]
    pfm = p.paragraph_format
    pfm.first_line_indent = Pt(0)
    pfm.left_indent = Pt(0)
    pfm.right_indent = Pt(0)
    pfm.line_spacing = 1.0
    pfm.space_before = Pt(0)
    pfm.space_after = Pt(3)
    pfm.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    run_font(r, SONG, TNR, 10.5, bold)


def table(headers, rows, widths, centers=None, cap=None):
    """centers: 每列是否居中（首列表头之外的列默认左对齐）。"""
    if cap:
        caption(cap)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = st['Table Grid']
    t.autofit = False
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = t._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    borders = OxmlElement('w:tblBorders')
    for edge, sz in (('top', '8'), ('left', '8'), ('bottom', '8'), ('right', '8'), ('insideH', '4'), ('insideV', '4')):
        b = OxmlElement('w:' + edge)
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '000000')
        borders.append(b)
    tblPr.append(borders)
    mar = OxmlElement('w:tblCellMar')
    for edge, w in (('top', '40'), ('left', '108'), ('bottom', '40'), ('right', '108')):
        m = OxmlElement('w:' + edge)
        m.set(qn('w:w'), w)
        m.set(qn('w:type'), 'dxa')
        mar.append(m)
    tblPr.append(mar)
    centers = centers or [False] * len(headers)
    hdr = t.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader')
    trPr.append(th)
    cs = OxmlElement('w:cantSplit')
    trPr.append(cs)
    for i, htext in enumerate(headers):
        fill_cell(hdr.cells[i], htext, widths[i], center=True, bold=True, fill='F2F2F2')
    for row in rows:
        r = t.add_row()
        trPr = r._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        for i, c in enumerate(row):
            fill_cell(r.cells[i], c, widths[i], center=centers[i])
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    return t


def caption(text):
    return plain(text, align=WD_ALIGN_PARAGRAPH.CENTER, keep=True)


def page_number_footer():
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Pt(0)
    run = p.add_run()
    run_font(run, SONG, TNR, 10.5)
    begin = OxmlElement('w:fldChar')
    begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' PAGE '
    end = OxmlElement('w:fldChar')
    end.set(qn('w:fldCharType'), 'end')
    for el in (begin, instr, end):
        run._r.append(el)


page_number_footer()

# ---------- 标题 ----------
p = doc.add_paragraph('产业组织理论课程大纲', style='Title')
run_font(p.runs[0], HEI, TNR, 18, True)
plain('以知识创造的逻辑组织教学（大纲草案）', size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, bold=False)

body('本大纲以知识创造为主线组织产业组织理论。课程不按教材章节平铺，而是把学科拆成十一条线索，每条线索都按同一条路径展开：从没人回答的问题出发，设定假设，推演结论，放进已知结论中对照，接受批评，再作推广。学生学完每条线索，要能复述这条路径，并能自己走一遍。')

# ---------- 一 ----------
h1('一、课程基本信息')
table(['项目', '内容'], [
    ['课程名称', '产业组织理论'],
    ['课程性质', '经济学类专业课程，面向本科高年级或研究生，按培养方案调整'],
    ['建议学时', '32 学时（16 讲，每讲 2 学时），另有课外研讨与期末项目'],
    ['先修要求', '中级微观经济学；基本的微积分与概率统计'],
    ['教学材料', '经典文献选读为主、教材为辅；配套课件与课堂实验材料'],
    ['适用对象', '经济学、产业经济学及相关专业学生'],
], [3.2, 12.8], centers=[True, False])

# ---------- 二 ----------
h1('二、课程定位与设计思路')
h2('（一）要解决的教学问题')
body('按教材章节平铺的讲法，容易把产业组织讲成一串模型：古诺、伯特兰、霍特林、结构—行为—绩效。学生记住了结论，却不知道这些模型从哪里来、为什么互相取代，遇到新问题时也无从下手。本课程把每条理论线还原成一次知识创造，让学生看到：结论的背后是一组选择——问什么问题、保留什么假设、用什么工具、怎样回应批评。')
h2('（二）四个问题域与十一条线索')
body('全课围绕四个递进的问题展开：企业在同一市场上怎样竞争；市场结构从哪里来、绩效由谁判断；企业与市场是什么关系、信息不完全时怎样交易；产业在时间中怎样演变。在此之外，还有一个方法问题（我们怎样知道理论是对的）和一个前沿问题（新现象提出了哪些新问题）。十一个线索的编号和全貌见表2，其中四条是通常教材已经覆盖的线索，其余七条是本大纲补充的线索。')
h2('（三）一条暗线：范式之争')
body('哈佛学派与芝加哥学派、主流范式与制度主义、垄断资本学派之间的争论贯穿全课。它提醒学生：理论选择不只是判断哪个更对，还涉及看什么、不看什么。')

# ---------- 三 ----------
h1('三、教学目标')
body('学完本课程，学生应能够做到以下五件事。')
table(['序号', '学完能做什么', '对应的线索'], [
    ['1', '复述各条线索的起点问题、关键假设、核心结论和主要批评', '全部'],
    ['2', '对一篇经典文献或一篇当代论文填写知识创造卡片，指出它改掉了哪条假设、更换了哪个分析单位，或把什么外生变量变成了内生变量', '全部'],
    ['3', '独立完成一次小规模的知识创造：改一条假设或换一个分析单位，推出新的结论，并与已知结论对照', '第1、3、5、7条'],
    ['4', '评价一项产业政策或反垄断决定所依据的理论，指出其成立条件与局限', '第2、7、8条'],
    ['5', '设计一个简单的课堂实验或经验检验，说明它能回答什么、不能回答什么', '第9条'],
], [1.2, 10.8, 4.0], centers=[True, False, True], cap='表1  教学目标与线索的对应关系')

# ---------- 四 ----------
h1('四、课程内容：知识地图')
body('表2给出十一条线索的全貌。“来源”一栏区分通常教材已经覆盖的线索与本大纲补充的线索。')
table(['编号', '线索', '起点问题', '关键节点', '主导的创造动作', '来源'], [
    ['1', '策略互动', '少数几家相互牵制，价格和产量停在哪里',
     '古诺（1838）、伯特兰（1883）、霍特林（1929）、斯塔克尔伯格（1934）、纳什（1950）；进入阻挠、限制性定价、声誉',
     '改一条假设', '已有'],
    ['2', '结构—行为—绩效', '集中是否损害绩效，政府能否据此干预',
     'Mason（1939）、Bain（1951、1956）；集中度、赫芬达尔指数、勒纳指数；“集中—利润”关系不稳健的批评',
     '创造测量工具', '已有'],
    ['3', '产品差异与定价', '去掉同质假设后，企业靠什么竞争',
     '张伯伦（1933）、霍特林（1929）、Lancaster（1966）、Dixit 与 Stiglitz（1977）；歧视定价、广告、转换成本、网络效应、捆绑',
     '更换分析单位', '已有'],
    ['4', '创新动态', '市场结构与创新，谁决定谁',
     '熊彼特（1912、1942）、Arrow（1962）、Schmookler（1966）；专利、研发溢出；Aghion 等（2005）；兼并重组；Nelson 与 Winter（1982）、Klepper（1996）',
     '把静态换成动态', '已有，补演化部分'],
    ['5', '企业边界与纵向关系', '为什么会有企业，边界在哪，上下游怎样定价',
     'Coase（1937）、Spengler（1950）、Williamson（1975）、Grossman 与 Hart（1986）；纵向约束',
     '更换分析单位：从市场到交易', '补充'],
    ['6', '信息', '信息不对称时市场还存在吗',
     'Stigler（1961）、Akerlof（1970）、Spence（1973）、Rothschild 与 Stiglitz（1976）',
     '外生变内生：信息', '补充'],
    ['7', '进入、退出与沉没成本', '市场结构是给定的，还是竞争的结果',
     'Bain（1956）、Stigler（1968）、Baumol 等（1982）、Sutton（1991）',
     '外生变内生：结构', '补充'],
    ['8', '芝加哥批评与反垄断规制', '凭什么干预，由谁干预',
     'Stigler、Demsetz（1973）、Posner（1976）、Bork（1978）；规制俘获（1971）；激励规制（Laffont 与 Tirole，1993）',
     '批评升级为学派', '补充'],
    ['9', '经验研究与实验', '怎样知道理论说的是真的',
     '张伯伦的课堂实验（1948）、Smith（1962）、Fouraker 与 Siegel（1963）；新经验产业组织；BLP（1995）；行为产业组织',
     '经验反常驱动', '补充'],
    ['10', '新前沿', '新现象提出哪些新问题',
     '双边市场（Rochet 与 Tirole，2003）；拍卖与市场设计；相互倾销（1980）、战略性贸易政策（1985）；产业政策',
     '回应新现象、移植工具', '补充'],
    ['11', '范式之争（暗线）', '主流范式看不到什么',
     'Galbraith（1952）；卡莱茨基的垄断程度；Baran 与 Sweezy（1966）；Eichner（1976）',
     '换范式', '补充'],
], [1.0, 2.3, 2.8, 6.3, 2.6, 1.0], centers=[True, False, False, False, False, True], cap='表2  产业组织理论的知识地图')
plain('注：表中年份为通行文献的通常标注，编写各讲讲义前应逐条核对版本与出处。')

# ---------- 五 ----------
h1('五、教学安排')
body('16讲按“先看竞争的行为，再看结构与政策，然后进入企业与信息，最后到时间、方法和前沿”的顺序排列。每讲给出核心内容、训练的创造动作和课前的学生任务。')
table(['讲次', '模块', '主题', '核心内容', '训练的创造动作'], [
    ['1', '一、导论', '从一个模型看知识如何被造出来', '古诺模型的完整推演；六个动作；课程地图；知识创造卡片的填法', '六个动作的整体认知'],
    ['2', '二、竞争的行为', '同质产品下的产量竞争', '古诺模型的假设、反应函数、均衡；与垄断和完全竞争对照；n 家厂商的推广；推测变差', '设定假设、对照定位'],
    ['3', '', '价格、位置与先后', '伯特兰悖论；霍特林的线性城市；斯塔克尔伯格的领导者模型', '接受批判、改一条假设'],
    ['4', '', '策略性行为', '进入阻挠、限制性定价、声誉与掠夺性定价；案例研讨', '把静态换成动态（初步）'],
    ['5', '', '产品差异', '垄断竞争；特征方法；多样性偏好；需求估计的基本思想', '更换分析单位'],
    ['6', '', '定价与产品策略', '歧视定价；广告；转换成本；网络效应与标准；捆绑', '更换分析单位、推广一般化'],
    ['7', '三、结构、绩效与政策', '结构—行为—绩效', '哈佛学派；测量指标；经验规律及其批评', '创造测量工具'],
    ['8', '', '结构从哪里来', '进入壁垒；可竞争市场；内生沉没成本', '外生变内生'],
    ['9', '', '芝加哥批评与反垄断', '效率解释；规制俘获；反垄断的执法标准；案例研讨', '批评升级为学派'],
    ['10', '', '规制与激励规制', '回报率规制；激励规制；政策案例研讨', '接受批判、对照定位'],
    ['11', '四、企业、合约与信息', '企业边界与纵向关系', '交易成本；资产专用性；不完全合约；双重加价与纵向约束', '更换分析单位'],
    ['12', '', '信息与市场', '搜寻；柠檬市场；信号；筛选；与歧视定价和广告的联系', '外生变内生'],
    ['13', '五、时间中的产业', '创新与市场结构', '熊彼特；阿罗的替代效应；专利；研发溢出；竞争与创新的倒U形关系', '把静态换成动态'],
    ['14', '', '演化、生命周期与兼并', '惯例与搜寻；产业生命周期；兼并重组与创新', '把静态换成动态、推广一般化'],
    ['15', '六、怎样知道', '经验研究与实验', '结构—行为—绩效回归的局限；新经验产业组织；需求估计；课堂实验；行为产业组织', '经验反常驱动'],
    ['16', '七、前沿与范式', '平台、市场设计、产业政策', '双边市场；拍卖；开放经济中的产业组织；产业政策；范式之争', '回应新现象、换范式'],
    ['课末', '', '汇报', '学生展示自己的“一次知识创造”', '综合运用'],
], [1.0, 2.6, 3.2, 6.6, 2.6], centers=[True, False, False, False, False], cap='表3  讲次安排')

# ---------- 六 ----------
h1('六、贯穿全课的知识创造方法')
h2('（一）六个基本动作')
body('发现空白、设定假设、形式推演、对照定位、接受批判、推广一般化。第1讲以古诺为范例完整走一遍，之后每条线索都按这六步复述，使学生形成固定的分析习惯。')
h2('（二）五种学科层面的动作')
body('更换分析单位（产品换成特征，市场换成交易）；把外生变内生（结构、信息、企业边界）；创造测量工具（集中度、勒纳指数、需求估计）；回应经验反常与新现象；换范式。这五种动作用于解释一条线索如何成长为另一个方向。')
h2('（三）知识创造卡片')
body('卡片是全课统一的学习工具，格式见表4。每个模块至少完成一张，全课程不少于八张。')
table(['栏目', '填写要求'], [
    ['空白', '这篇文献之前，哪个问题没有答案，或哪个结论解释不了观察到的现象'],
    ['假设', '作者保留和删掉了什么，为什么可以这样删'],
    ['推演', '从假设到结论的核心机制，逐步写清'],
    ['对照', '结论与哪些已知结论放在一起才有意义，差别在哪里'],
    ['批评', '主要的反例或替代解释，它针对的是哪条假设'],
    ['推广', '能否一般化，边界在哪里'],
    ['未解问题', '留给下一个研究者的问题'],
    ['我能做什么', '我可以改哪条假设或换哪个分析单位'],
], [3.0, 13.0], centers=[True, False], cap='表4  知识创造卡片的格式')

# ---------- 七 ----------
h1('七、研讨式学习设计')
body('每个模块配一次研讨，形式统一：课前读一篇文献并填好卡片；课上由两组汇报，另有一组专门负责批评；教师只做三件事——纠正史实、追问假设、把讨论引回未解问题。')
table(['模块', '研讨主题', '核心问题', '学生产出'], [
    ['二', '同质品行业的产量竞争', '选取一个产品差异很小的行业，判断它更接近古诺、伯特兰还是斯塔克尔伯格', '两页的行业分析'],
    ['二', '定价策略比较', '同一企业在不同渠道、不同时间定价不同，属于哪一类价格歧视，需要哪些信息条件', '案例卡片'],
    ['三', '一项反垄断决定的依据', '这项决定依据的是结构标准还是行为标准，芝加哥学派的批评是否成立', '辩论提纲'],
    ['三', '规制方案设计', '针对一个自然垄断环节设计激励规制方案，并说明它依赖哪些信息前提', '一页方案'],
    ['四', '纵向一体化的理由', '某企业并购上下游，是为了效率还是为了封锁', '证据清单'],
    ['五', '专利制度的两难', '加强专利保护，对创新是促进还是阻碍', '立场陈述'],
    ['六', '重做一次检验', '选一个已有的经验结论，讨论它的识别策略与可能偏误', '评述笔记'],
    ['七', '平台定价', '平台一边免费、另一边收费，怎样用双边市场模型解释', '模型草图'],
], [1.2, 3.4, 8.2, 3.2], centers=[True, False, False, False], cap='表5  各模块的研讨设计')

# ---------- 八 ----------
h1('八、考核方式（建议）')
table(['项目', '占比', '内容与标准'], [
    ['知识创造卡片', '30%', '不少于八张，每张能说清假设、批评和推广'],
    ['课堂研讨', '20%', '两次主讲、一次批评'],
    ['期末项目', '40%', '“一次知识创造”：改一条假设或换一个分析单位，写出推演、对照与局限；或对一个现实行业做出有证据的产业组织分析'],
    ['课堂实验参与', '10%', '参加实验并提交实验记录'],
], [3.4, 1.6, 11.0], centers=[True, True, False], cap='表6  考核构成')

# ---------- 九 ----------
h1('九、参考文献')
table(['线索', '代表性文献'], [
    ['1', 'Cournot（1838）；Bertrand（1883）；Hotelling（1929）；Stackelberg（1934）；Nash（1950）；Tirole（1988）'],
    ['2', 'Mason（1939）；Bain（1956）'],
    ['3', 'Chamberlin（1933）；Lancaster（1966）；Dixit 与 Stiglitz（1977）'],
    ['4', 'Schumpeter（1942）；Arrow（1962）；Aghion 与 Griffith（2005）；Nelson 与 Winter（1982）'],
    ['5', 'Coase（1937）；Williamson（1985）；Grossman 与 Hart（1986）'],
    ['6', 'Stigler（1961）；Akerlof（1970）；Spence（1973）'],
    ['7', 'Bain（1956）；Baumol、Panzar 与 Willig（1982）；Sutton（1991）'],
    ['8', 'Stigler（1968）；Posner（1976）；Laffont 与 Tirole（1993）'],
    ['9', 'Smith（1962）；Fouraker 与 Siegel（1963）；Berry、Levinsohn 与 Pakes（1995）'],
    ['10', 'Brander 与 Krugman（1980）；Rochet 与 Tirole（2003）'],
    ['11', 'Galbraith（1952）；Baran 与 Sweezy（1966）'],
    ['教材', 'Tirole《产业组织理论》；Cabral《产业组织导论》'],
], [1.6, 14.4], centers=[True, False], cap='表7  各线索的代表性文献')
plain('注：以上为各线索的代表性文献，具体篇目与版本在每讲讲义中列明。')

# ---------- 十 ----------
h1('十、使用说明')
body('本大纲为草案。学时、适用对象和考核比例可按培养方案调整；学时不足时，可压缩第10讲和第14讲，保留每条线索的起点问题、关键假设和主要批评。导论课的配套课件《古诺模型：重走一次知识创造》已另行制作，可直接用于第1讲。')

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))
print(OUT)
