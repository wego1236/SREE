import jieba, wordcloud, collections
import requests
import re
string = ""

stopwords = [word.strip().lower() for word in open("stopwords.txt")]
print(stopwords)

for index in range(0, 1):
    url = 'https://github.com/JetBrains/intellij-community/pulls?page=' + index.__str__() + '&q=is%3Apr+is%3Aopen'


    response = requests.get(url)
    response.encoding = 'utf-8'
    #print(response.text)
    html = response.text


    hrefs = re.findall(r'data-hovercard-url=".*?" href="/JetBrains/intellij-community/pull/(.*?)"', html, re.S)

    for href in hrefs:
        filename = href + '.html'
        try:

            with open(filename, 'r', encoding='utf-8') as file:
                string += file.read()
            print(filename)
        except IOError:

            href = "https://github.com" + "/JetBrains/intellij-community/pull/" + href
            useragent = {'user-agent': 'Mozilla/5.0'}
            res = requests.get(href, headers = useragent)
            res.encoding = 'utf-8'
            with open(filename, 'w', encoding = 'utf-8') as file:
                file.write(res.text)
            print(href)
            content = re.findall(r'<td class="d-block comment-body markdown-body  js-comment-body">\n(.*?)</td', res.text, re.S);
            for i in range(0, content.__len__()):
                content[i] = content[i].replace('<p>', '')
                content[i] = content[i].replace('</p>', '')
                content[i] = content[i].replace('<li>', '')
                content[i] = content[i].replace('</li>', '')
                content[i] = content[i].replace('<ul>', '')
                content[i] = content[i].replace('</ul>', '')
                content[i] = content[i].replace('<h3>', '')
                content[i] = content[i].replace('</h3>', '')
                content[i] = content[i].replace('<h4>', '')
                content[i] = content[i].replace('</h4>', '')
                content[i] = content[i].replace('<em>', '')
                content[i] = content[i].replace('</em>', '')
                content[i] = content[i].replace('<code>', '')
                content[i] = content[i].replace('</code>', '')
                content[i] = content[i].replace('<br>', '\n')
                content[i] = content[i].replace('<h2>', '')
                content[i] = content[i].replace('</h2>', '')
                content[i] = content[i].replace('<a>', '')
                content[i] = content[i].replace('</a>', '')
                content[i] = content[i].replace('<ol>', '')
                content[i] = content[i].replace('</ol>', '')
                #print(content[i])
                string += content[i]
                #print(href)
    #print(href)
    #print(content.__len__())

string = re.sub('<.*?>', ' ', string, flags=re.S)
string = re.sub('href', ' ', string, flags=re.S)
#string = re.sub('https://.*?', ' ', string)
string = re.sub(' +', ' ', string, flags=re.S)

string = string.lower()
result = ''
    # lline = line.strip()
    # print(lline)
strs = string.split()
print(strs)
# print(lline)
for i in strs:
    if i == "github":
        print(i)
    if i not in stopwords:
       result += i
#print(result)

w = wordcloud.WordCloud(background_color="white", width =800, height = 660, margin = 2).generate(result);
w.to_file("picture.png")