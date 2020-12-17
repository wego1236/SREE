from bs4 import BeautifulSoup
import lxml
import requests
import re
import sklearn

url = 'https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&\
bug_status=REOPENED&field0-0-0=product&field0-0-1=component&field0-0-2=alias&field0-0-3=short_desc&\
field0-0-4=status_whiteboard&field0-0-5=content&limit=0&order=bug_id&query_format=advanced&type0-0-0=substring&\
type0-0-1=substring&type0-0-2=substring&type0-0-3=substring&type0-0-4=substring&type0-0-5=matches&value0-0-0=bug&\
value0-0-1=bug&value0-0-2=bug&value0-0-3=bug&value0-0-4=bug&value0-0-5=%22bug%22'

print(url)
response = requests.get(url)
response.encoding = 'utf-8'
with open('allbugs.html', 'w', encoding='utf-8') as fbugs:
    fbugs.write(response.text)
# with open('bugs.html', 'r', encoding='utf-8') as fbugs:
    # text = fbugs.read()
soup = BeautifulSoup(open('allbugs.html', 'r', encoding='utf-8'), 'lxml')

"""解析html文件获得每个bug条目"""
data_list = []   # 结构: [dict1, dict2, ...]
for idx, tr in enumerate(soup.find_all('tr')):
    # print(tr.get('class'))
    if idx != 0:
        tds = tr.find_all('td')
        # ids = re.findall(r'<a href="show_bug.cgi?id=.*?">(.*?)</a>', , re.S)
        # print(tds[0].a.get_text())
        # print('\n')
        data_list.append({
            'Priority': tr.get('class')[2][3:],     # 优先级
            'Severity': tr.get('class')[1][3:],       # 严重性
            'ID': tds[0].a.get_text(),
            'Product': re.sub(r'[ \n]+', ' ', tds[1].span.get_text(), re.S).rstrip(),
            'Component': re.sub(r'[ \n]+', ' ', tds[2].span.get_text(), re.S).rstrip(),
            'Assignee': re.sub(r'[ \n]+', ' ', tds[3].span.get_text(), re.S).rstrip(),
            'Status': re.sub(r'[ \n]+', ' ', tds[4].span.get_text(), re.S).rstrip(),
            'Resolution': re.sub(r'[ \n]+', ' ', tds[5].span.get_text(), re.S).rstrip(),
            'Summary': re.sub(r'[ \n]+', ' ', tds[6].a.get_text(), re.S).rstrip()
        })
# print(data_list)

'''以下内容为判断各个属性每种值的优先级平均值，比较一下差异'''
"""先判断Product"""
products = []
sumPro = []
countPro = []
for data in data_list:
    if data['Product'] not in products:
        products.append(data['Product'])
        sumPro.append(0)
        countPro.append(0)
    i = products.index(data['Product'])
    sumPro[i] += int(data['Priority'][1:])     # 加上等级
    countPro[i] += 1

avgPro = []
for i in range(len(products)):
    avgPro.append(sumPro[i] / countPro[i])
print(products)
print(countPro)
print(avgPro)


