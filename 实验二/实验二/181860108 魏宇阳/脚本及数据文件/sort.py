import re
import numpy as np
def takeThird(elem):
    return elem[2]

def sortdata(data_list, weights, products, avgPro, assignees, avgAsn, tags, avgTag, statuses, avgStatus, comps, avgComp):
    P = []  # 优先级结果
    scores = []
    prs = [] # 原始优先级
    for data in data_list:
        score = avgPro[products.index(data['Product'])] * weights[0]\
            + avgAsn[assignees.index(data['Assignee'])] * weights[1]\
            + avgStatus[statuses.index(data['Status'])] * weights[3]\
            + avgComp[comps.index(data['Component'])] * weights[4]
        datatags = re.findall(r'\[(.*?)]', data['Summary'], re.S)
        tagscore = 0
        for tag in datatags:
            tagscore += avgTag[tags.index(tag)]
        if len(datatags) != 0:
            tagscore /= len(datatags)
        else: tagscore = 3
        score += weights[2] * tagscore
        scores.append(score)
    items = []
    for i in range(0, len(data_list)):
        items.append((i, int(data_list[i]['ID']), scores[i], int(data_list[i]['Priority'][1:])))
    items.sort(key=takeThird)
    print(items)
    return items

def writeitems(items):
    with open('result1.csv', 'w', encoding='utf-8') as fr:
        for item in items:
            fr.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3]) + '\n')



