import json

ar = []
with open('list.txt') as file:
    for i in file:
        n = i.lower().split("\n")[0]
        if n != "":
            ar.append(n)
with open('../list.json', "w", encoding='utf-8') as f:
    json.dump(ar, f, indent=4, ensure_ascii=False)