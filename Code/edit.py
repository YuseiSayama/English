###dataファイルの読み込み###
with open('../Phrases/phrases_sentence.txt') as f:
    phrases_sentence = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_meaning.txt') as f:
    phrases_meaning = [s.strip() for s in f.readlines()]
with open('../Phrases/phrases_times.txt') as f:
    phrases_times = [s.strip() for s in f.readlines()]

###modeの初期設定###
mode = 's'

###編集の繰り返し###
while True:

    ###問題番号の検索###
    while True:
        number = input('編集する問題の番号を入力してください>>')
        if str.isdecimal(number) or number == 's' or number == 'f' or number == 'c':
            break
        else:
            print('入力は数字、もしくはs,f,cのいずれかです')

    ###modeの設定###
    if str.isdecimal(number):
        number = int(number)
        ###編集###
        if mode == 's':
            print(phrases_sentence[number])
            print(phrases_meaning[number])
            print('')
            phrases_sentence[number] = input('新たな英文>>')
            phrases_meaning[number] = input('新たな訳文>>')
            print('')
        if mode == 'f':
            print('')
            print('No.%dの問題はすでに%s回、解いたことになっています'%(number,phrases_times[number]))
            while True:
                phrases_times[number] = input('修正後の解答回数>>')
                if str.isdecimal(phrases_times[number]):
                    break
                else:
                    print('入力は数字です')
    else:
        mode = number
        if mode == 'c':
            break

###書き込み###
with open('../Phrases/phrases_sentence.txt', mode='w') as f:
    f.write('\n'.join(phrases_sentence))
    f.write('\n')
with open('../Phrases/phrases_meaning.txt', mode='w') as f:
    f.write('\n'.join(phrases_meaning))
    f.write('\n')
with open('../Phrases/phrases_times.txt', mode='w') as f:
    f.write('\n'.join(phrases_times))
    f.write('\n')
