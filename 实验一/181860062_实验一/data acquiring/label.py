from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import json

ide_label=open("C:\python_log\label.txt",'w')
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
for i in range(1,9):
    url = "https://github.com/microsoft/vscode/labels?page="+str(i)+"&sort=name-asc"
    f=requests.get(url,headers=header)
    soup=BeautifulSoup(f.content, "lxml")
    for k in soup.find_all('div', class_="table-list-cell"):
        a=k.find_all('span')
        print(a[0].string,file=ide_label)


ide_label.close()
