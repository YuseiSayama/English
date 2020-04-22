# coding: utf-8
##########データの読み込み・編集インポート############
import datetime
import shutil
import os
###########pdf作成インポート###########
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

############データの読み込み###############
with open('../Phrases/phrases_sentence.txt') as f:
    phrases_sentence = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_meaning.txt') as f:
    phrases_meaning = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_date.txt') as f:
    phrases_date = [s.strip() for s in f.readlines()]

##############データの更新##############
dt_today = datetime.datetime.now()
with open('../Renew/renew_trigger.txt') as f:
    Renew_Trigger = [s.strip() for s in f.readlines()]
with open('../Renew/renew_times.txt') as f:
    Renew_Times = [s.strip() for s in f.readlines()]
with open('../Renew/renew_date.txt') as f:
    Renew_Date = [s.strip() for s in f.readlines()]
trigger_date = datetime.datetime.strptime(Renew_Trigger[0], '%Y-%m-%d') - dt_today
if trigger_date.total_seconds() <= 0:
    for i in range(len(Renew_Date)):
        phrases_date[i] = Renew_Date[i]

############問題範囲の抽出##############
dt_today = datetime.datetime.now()
non_skip_posi = []
for i in range(len(phrases_date)):
    dt_difference = dt_today - datetime.datetime.strptime(phrases_date[i], '%Y-%m-%d')
    if dt_difference.total_seconds() >= 0:
        non_skip_posi.append(i)

############Data作成###########
data=[['問題番号','日本語','英語']]
l = list(range(len(non_skip_posi)))
for j in l:
    i = non_skip_posi[j]
    data.append(['No.'+str(i),phrases_meaning[i],phrases_sentence[i]])

############pdf作成############
def pdf_gen_proc(file_pdf,data):
    doc = SimpleDocTemplate(file_pdf,pagesize=A4)
    fontname = "GenShinGothic"
    pdfmetrics.registerFont(TTFont(fontname,"../Fonts/GenShinGothic-Light.ttf"))
    elements = []

    #dataを改行に対応させる
    style = ParagraphStyle(name='Normal', fontName=fontname, fontSize=10)
    for i in range(1,len(data)):
        for j in range(len(data[0])):
            data[i][j] = Paragraph(data[i][j],style)

    #TableStyleの設定
    table_style = [
    #全体の設定
    ('GRID',(0, 0),(-1,-1),1,'#7aaadc'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    #一行目の設定
    ('ALIGN',(0,0),(-1,0),'CENTER'),
    ('VALIGN',(0,0),(-1,0),'TOP'),
    ('FONT',(0,0),(-1,0),fontname,10),
    ('BACKGROUND',(0,0),(-1,0),'#3997e2'),
    ('TEXTCOLOR',(0,0),(-1,0),'#ffffff')
    ]
    for i in range(2,len(data)):
        if i%2 == 0:
            table_style.append(('BACKGROUND',(0,i),(-1,i),'#eff5fc'))

    #tableの作成
    table=Table(data, colWidths=(20*mm,85*mm,85*mm))
    table.setStyle(TableStyle(table_style))
    elements.append(table)

    doc.build(elements)

############pdf実行##############
file_pdf = 'PhrasesTest.pdf'
pdf_gen_proc(file_pdf,data)

#############バックナンバーの保存とファイルの移動#############
desktop_path = os.path.expanduser('~') + '/desktop/'
shutil.copy('PhrasesTest.pdf', '../BackNumber/PhrasesTest'+str(dt_today.date())+'.pdf')
shutil.copy('PhrasesTest.pdf', desktop_path + 'PhrasesTest.pdf')
os.remove('PhrasesTest.pdf')
