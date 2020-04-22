# coding: utf-8
###インポート###
import datetime
import random
import math
import copy
import numpy as np
import os

###dataファイルの読み込み###
with open('../Phrases/phrases_sentence.txt') as f:
    phrases_sentence = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_meaning.txt') as f:
    phrases_meaning = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_times.txt') as f:
    phrases_times = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_date.txt') as f:
    phrases_date = [s.strip() for s in f.readlines()]

###更新###
dt_today = datetime.datetime.now()
with open('../Renew/renew_times.txt') as f:
    Renew_Times = [s.strip() for s in f.readlines()]
with open('../Renew/renew_date.txt') as f:
    Renew_Date = [s.strip() for s in f.readlines()]
if os.path.exists('../Renew/renew_trigger.txt'):
    with open('../Renew/renew_trigger.txt') as f:
        Renew_Trigger = [s.strip() for s in f.readlines()]
    trigger_date = datetime.datetime.strptime(Renew_Trigger[0], '%Y-%m-%d') - dt_today
    if trigger_date.total_seconds() <= 0:
        for i in range(len(Renew_Date)):
            phrases_date[i] = Renew_Date[i]
            phrases_times[i] = Renew_Times[i]

###date,timeファイルの書き込み###
with open('../Phrases/phrases_times.txt', mode='w') as f:
    f.write('\n'.join(phrases_times))
    f.write('\n')
with open('../Phrases/phrases_date.txt', mode='w') as f:
    f.write('\n'.join(phrases_date))
    f.write('\n')

###問題部分の抽出###
N = len(phrases_sentence)
non_skip_posi = []
for i in range(len(phrases_date)):
    dt_difference = dt_today - datetime.datetime.strptime(phrases_date[i], '%Y-%m-%d')
    if dt_difference.total_seconds() >= 0:
        non_skip_posi.append(i)

###recentファイルの読み込み###
with open('../Question/recent_exam_posi.txt') as f:
    recent_exam_posi_list = [s.strip() for s in f.readlines()]
    #recent_exam_posi_list = [int(l) for l in recent_exam_posi_list]
with open('../Question/recent_exam_date.txt') as f:
    recent_exam_date_list = [s.strip() for s in f.readlines()]
    recent_exam_date = datetime.datetime.strptime(recent_exam_date_list[0],'%Y-%m-%d')
print(recent_exam_posi_list[0])
print(type(recent_exam_posi_list[0]))
recent_exam_posi_list = [int(l) for l in recent_exam_posi_list]
print(type(recent_exam_posi_list[0]))

###問題###
now_today = datetime.datetime.now()
while now_today.date() == dt_today.date():
    l = list(range(len(non_skip_posi)))
    lr = random.sample(l, len(l))
    #問題を出す#
    renew_posi = []
    for j in range(len(non_skip_posi)):
        print('%d/%d'%(j+1,len(non_skip_posi)))
        i = non_skip_posi[lr[j]]
        print(phrases_meaning[i],end='')
        next = input('')
        if next == 'c':
            break
        print(phrases_sentence[i])
        print('')
        renew_posi.append(i)

    #レベルの表示#
    #ファイルを開く
    with open('../Level/level.txt') as f:
        level_list = [s.strip() for s in f.readlines()]
    #獲得した経験値を設定
    fluctuation_level = np.random.normal(loc=1,scale=0.1)
    exam_num = len(renew_posi)
    exp = math.floor(100*exam_num*fluctuation_level)
    #expを記述
    print('#################################')
    blank_num1 = len(str(exp))
    print('# exp+%d'%exp,end='')
    for k in range(26-blank_num1):
        print(' ',end='')
    print('#')
    print('#                               #')
    #Level,expの結果を設定
    level = int(level_list[1])
    exp += int(level_list[0])
    while 500*level <= exp:
        exp -= 500*level
        level += 1
    #Level,expの結果を表示
    print('# Lv.%d'%level,end='')
    blank_num2 = len(str(level))
    for k in range(27-blank_num2):
        print(' ',end='')
    print('#')
    print('# ',end='')
    box_num = math.floor((exp*25)/(500*level))
    for k in range(box_num):
        print('■',end='')
    for k in range(25-box_num):
        print('-',end='')
    parsent = math.floor((exp*100)/(500*level))
    blank_num3 = len(str(parsent))
    if blank_num3 == 1:
        blank_num3 = 2
    else:
        blank_num3 = 1
    for k in range(blank_num3):
        print(' ',end='')
    print('%d'%parsent,end='')
    print('% #')
    print('#################################')
    #新たなレベルを記入
    level_list = [str(exp),str(level)]
    with open('../Level/level.txt', mode='w') as f:
        f.write('\n'.join(level_list))

    #更新データの作成#
    if recent_exam_date.date() == dt_today.date():
        renew_list = list(set(renew_posi) - set(recent_exam_posi_list))
        print(renew_list)
        tomorrow = dt_today + datetime.timedelta(days=1)
        renew_trigger = [str(tomorrow.date())]
        for k in range(len(Renew_Times)):
            if k in renew_list:
                Renew_Times[k] = int(Renew_Times[k])
                n = np.random.normal(loc=1.7,scale=0.2)
                day_num = math.floor(Renew_Times[k]**n)
                if day_num >= 90:
                    limit = np.random.normal(loc=90,scale=1.5)
                    new_date = dt_today + datetime.timedelta(days=limit)
                else:
                    new_date = dt_today + datetime.timedelta(days=day_num)
                Renew_Date[k] = str(new_date.date())
                Renew_Times[k] += 1
                Renew_Times[k] = str(Renew_Times[k])
        renew_list = [str(i) for i in renew_list]
        with open('../Question/recent_exam_posi.txt', mode='a') as f:
            f.write('\n'.join(renew_list))
            f.write('\n')
    else:
        renew_list = renew_posi
        tomorrow = dt_today + datetime.timedelta(days=1)
        renew_trigger = [str(tomorrow.date())]
        for k in range(len(Renew_Times)):
            if k in renew_list:
                Renew_Times[k] = int(Renew_Times[k])
                n = np.random.normal(loc=1.7,scale=0.2)
                day_num = math.floor(Renew_Times[k]**n)
                if day_num >= 90:
                    limit = np.random.normal(loc=90,scale=1.5)
                    new_date = dt_today + datetime.timedelta(days=limit)
                else:
                    new_date = dt_today + datetime.timedelta(days=day_num)
                Renew_Date[k] = str(new_date.date())
                Renew_Times[k] += 1
                Renew_Times[k] = str(Renew_Times[k])
        renew_list = [str(i) for i in renew_list]
        with open('../Question/recent_exam_date.txt', mode='w') as f:
            f.write(str(dt_today.date())+'\n')
        with open('../Question/recent_exam_posi.txt', mode='w') as f:
            f.write('\n'.join(renew_list))
            f.write('\n')
    with open('../Renew/renew_trigger.txt', mode='w') as f:
        f.write('\n'.join(renew_trigger))
    with open('../Renew/renew_times.txt', mode='w') as f:
        f.write('\n'.join(Renew_Times))
        f.write('\n')
    with open('../Renew/renew_date.txt', mode='w') as f:
        f.write('\n'.join(Renew_Date))
        f.write('\n')

    now_today = datetime.datetime.now()

    if next == 'c':
        break
