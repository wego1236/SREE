import wordcloud
import bs4
import requests
import re
string = ""

with open('title.txt', 'r', encoding='utf-8') as ftitles:
    sentence = ftitles.readline()
    words1line = sentence.split() # 这一行中的所有词汇
    # if ...开始进行关键词分类
# print(result)

w = wordcloud.WordCloud(background_color="white", width =800, height = 660, margin = 2).generate(tagstring)
w.to_file("tag.png")
