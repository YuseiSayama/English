# coding: utf-8
import sys
import datetime

dt_today = datetime.datetime.now()

while True:
    sentence = input('英文>>')
    meaning = input('邦文>>')

    print('以下の入力でいいですか？')
    print(sentence)
    print(meaning)
    confr = input('OK:Enter No:Other >>')

    if confr == '':
        with open('../Phrases/phrases_sentence.txt',mode='a') as f:
            f.write(sentence+'\n')

        with open('../Phrases/phrases_meaning.txt',mode='a') as f:
            f.write(meaning+'\n')

        with open('../Phrases/phrases_times.txt',mode='a') as f:
            f.write('0'+'\n')

        with open('../Phrases/phrases_date.txt',mode='a') as f:
            f.write(str(dt_today.date())+'\n')

        with open('../Renew/renew_times.txt',mode='a') as f:
            f.write('0'+'\n')

        with open('../Renew/renew_date.txt',mode='a') as f:
            f.write(str(dt_today.date())+'\n')

        print('------------------------------')
    else:
        pass
