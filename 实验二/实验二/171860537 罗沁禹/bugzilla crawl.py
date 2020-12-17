import requests
from bs4 import BeautifulSoup
import pandas
from concurrent.futures import ThreadPoolExecutor,as_completed
from requests.adapters import HTTPAdapter
def extractSample(bug):
    s = requests.Session()
    s.mount('https://',HTTPAdapter(max_retries=10))
    try:
        response = s.get(bug, timeout=5)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "lxml")
        status = soup.find(id="bz_field_status").get_text().strip()
        alias = soup.find(id="field_label_alias").parent.td.get_text().strip()
        product = soup.find(id="field_container_product").get_text().strip()
        component = soup.find(id="field_container_component").get_text().strip().split()[0]
        version = soup.find(id="field_label_version").parent.td.get_text().strip()
        hardware = soup.find(id="field_label_rep_platform").parent.td
        hardware = ' '.join(hardware.get_text().strip().split())
        importance = soup.find(href="page.cgi?id=fields.html#importance").parent.parent.parent.td
        importance = ' '.join(importance.get_text().strip().split()).replace("(vote)", "")
        assignee = soup.find(id="field_label_assigned_to").parent.td.get_text().strip()
        return [{'status': status, 'alias': alias, 'product': product,
                 'component': component, 'version': version, 'hardware': hardware, 'importance': importance,
                 'assignee': assignee}]
    except requests.exceptions.RequestException as e:
        print(e)
    #response = requests.get(bug,timeout=5,)


#response = open("Bug List.html",encoding = "utf-8").read()
#bugList_soup = BeautifulSoup(response,"lxml")
#bugList = bugList_soup.find_all(class_ = "first-child bz_id_column")
df = pandas.DataFrame(columns = ("status","alias","product","component","version","hardware","importance","assignee"))
num = 0
executor = ThreadPoolExecutor(max_workers=5)
all_task = [executor.submit(extractSample, (bug)) for bug in open('htmlList.txt')]
for future in as_completed(all_task):
    data = future.result()
    df = df.append(data, ignore_index = True)
    print(num)
    num+=1
    if num%100 == 0:
        df.to_csv("bugSample3.csv", index=False)

#df = df.append([{'status':"1", 'alias':"1", 'product':"1",
                # 'component':"1", 'version':"1",'hardware': "1",'importance': "1", 'assignee':"1"}], ignore_index=True)

df.to_csv("bugSample3.csv",index = False)