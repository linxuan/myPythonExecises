import json

while True: 
    idiom = input('输入要接龙的成语:')
    with open('idiom.json', mode='r',encoding='utf-8') as f:
        dic = json.load(f)
        for i in dic:
            if idiom[-1] == i['word'][0]:
                print(idiom, '->', i['word'])