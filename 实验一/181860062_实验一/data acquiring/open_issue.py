from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import json

ide_issue=open("C:\python_log\open_issue.txt",'w',encoding='utf-8')
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
for i in range(1,200):
    url = "https://github.com/microsoft/vscode/issues?page="+str(i)+"&q=is%3Aissue+is%3Aopen+sort%3Acomments-desc"
    f=requests.get(url,headers=header)
    soup=BeautifulSoup(f.content, "lxml")
    for k in soup.find_all('div', class_="float-left col-8 lh-condensed p-2"):
        a=k.find_all('a')
        print(a[0].string,file=ide_issue)


ide_issue.close()
