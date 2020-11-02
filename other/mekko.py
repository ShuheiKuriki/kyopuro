def inputs(score, quest):
    print(quest+' y/N')
    res = input()
    Yess = ['y','Y','yes','YES','Yes']
    Nos = ['N','No','n','no','NO']
    if res in Yess:
        return score
    elif res in Nos:
        return 0
    else:
        print('もう一度入力してください')
        return inputs(score,quest) 

def report(results):
    names = ['Boby', 'Spirit', 'Mind1', 'Mind2', 'Heart']
    messages = [
        '危機感をもって生活しましょう。',
        '小さな事の積み重ねが大切です。',
        '着実に変化してきています。',
        '順調です。たまにはリラックスを。',
        'あと少しです。頑張りましょう！',
        'おめでとうございます！第8の習慣をはじめましょう。'
    ]
    borders = [0,12,5,25,50,75,100,101]

    for name, result in zip(names,results):
        print('{}: {}'.format(name,result))
    
    sevenhabits = int(sum(results))
    
    print('あなたの得点は{}点です'.format(sevenhabits))

    for upper, lower, message in zip(borders[1:], borders[:-1], messages):
        if sevenhabits>=lower and sevenhabits<upper:
            print(message)

scores = [25, 25, 12.5, 12.5, 25]
questions = [
    '1週間に3時間は運動しましたか？',
    '自然の中で瞑想する時間がありましたか？',
    '1週間に1冊は本を読みましたか？',
    '毎日、日記を書きましたか？',
    '誰かとご飯に行きましたか？'
]

if __name__ == '__main__':
    results = []
    for score, question in zip(scores, questions):
        results.append(inputs(score,question))

    report(results)