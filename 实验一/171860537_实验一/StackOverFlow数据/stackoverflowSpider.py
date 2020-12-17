import jieba, wordcloud, collections, bs4, lxml
import requests
import re
string = ""

stopwords = [word.strip().lower() for word in open("stopwords.txt")]
print(stopwords)

try:
    with open('titles.txt', 'r', encoding='utf-8') as ftitles:
        string = ftitles.read()
        sentences = ftitles.readlines()
except IOError:
    with open('title.txt', 'w', encoding='utf-8') as ftitles:
        for index in range(0, 1):
            # 首先从这622页问答中爬取每一页的数据
            url = 'https://stackoverflow.com/questions/tagged/ide?tab=newest&page=' + (index+1).__str__() + '&pagesize=15'

            response = requests.get(url)
            response.encoding = 'utf-8'
            # print(response.text)

            # 用html解析器解析网页
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            html = soup.prettify()
            print(html)
            pattern = re.compile(r'<a class="question-hyperlink" href="/questions.*?>(.*)</a>', re.S)
            titles = re.findall(r'<a class="question-hyperlink" href="/questions.*?>\n +(.*?)\n +</a>', html, re.S)

            print(titles)

            for title in titles:
                titles = re.sub(r'\r*\n*', ' ', title, flags=re.S)
                title = re.sub(r'<.*>', ' ', title, flags=re.S)
                string += title + ' ';
                ftitles.write(title + '\n')

            # print(href)
            # print(href)
            # print(content.__len__())
string = re.sub(r'\n+', ' ', string, flags=re.S)
string = re.sub(r'<.*?>', ' ', string, flags=re.S)
string = re.sub(' +', ' ', string, flags=re.S)

string = string.lower()
result = ''
# lline = line.strip()
# print(lline)
strs = string.split()

print(strs)
# print(lline)
for i in strs:
    if i not in stopwords:
        result += i + ' '
# print(result)
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(result)

w = wordcloud.WordCloud(background_color="white", width =800, height = 660, margin = 2).generate(result)
w.to_file("picture.png")
