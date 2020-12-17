import jieba, wordcloud, collections, bs4, lxml
import requests
import re
string = ""

alltags = []
tagstring = ''

try:
    with open('tag.txt', 'r', encoding='utf-8') as ftags:
        tagstring = ftags.read()
except IOError:
    with open('tag.txt', 'w', encoding='utf-8') as ftags:
        for index in range(0, 358):
            # 首先从这622页问答中爬取每一页的数据
            url = 'https://stackoverflow.com/questions/tagged/visual-studio-code?tab=newest&page=' + (index+1).__str__() + '&pagesize=50'

            response = requests.get(url)
            response.encoding = 'utf-8'
            # print(response.text)

            # 用html解析器解析网页
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            html = soup.prettify()
            # print(html)

            tags = re.findall(r"show questions tagged '(.*?)'", html, re.S);

            print(tags)

            for tag in tags:
                # if tag not in alltags:
                    # alltags.append(tag)
                if tag != 'visual-studio-code':
                    tagstring += tag + ' '
            print(url)
            # print(href)
            # print(content.__len__())
        ftags.write(tagstring)
# print(result)

w = wordcloud.WordCloud(background_color="white", width =800, height = 660, margin = 2).generate(tagstring)
w.to_file("tag.png")
