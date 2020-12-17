from bs4 import BeautifulSoup
import lxml
import requests
import re

url = 'https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&\
bug_status=REOPENED&field0-0-0=product&field0-0-1=component&field0-0-2=alias&field0-0-3=short_desc&\
field0-0-4=status_whiteboard&field0-0-5=content&order=bug_id&query_format=advanced&type0-0-0=substring&\
type0-0-1=substring&type0-0-2=substring&type0-0-3=substring&type0-0-4=substring&type0-0-5=matches&value0-0-0=bug&\
value0-0-1=bug&value0-0-2=bug&value0-0-3=bug&value0-0-4=bug&value0-0-5=%22bug%22'

# print(url)
"""下面是爬虫，已经爬了所以注释掉了，爬到了bugs.html文件里"""
'''response = requests.get(url)
response.encoding = 'utf-8'
with open('allbugs.html', 'w', encoding='utf-8') as fbugs:
    fbugs.write(response.text)'''

soup = BeautifulSoup(open('allbugs.html', 'r', encoding='utf-8'), 'lxml')

"""解析html文件获得每个bug条目"""
data_list = []   # 结构: [dict1, dict2, ...]
for idx, tr in enumerate(soup.find_all('tr')):
    # print(tr)
    if idx != 0:
        tds = tr.find_all('td')
        # ids = re.findall(r'<a href="show_bug.cgi?id=.*?">(.*?)</a>', , re.S)
        # print(tds[0].a.get_text())
        # print('\n')
        flag = 0
        for i in range(1, 6):
            if tds[i].span == None:
                flag = 1
                break
        if flag == 1:
            continue
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
"""判断Product"""
products = []
sumPro = []
countPro = []
countperprPro = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0}    # 每个优先级的条目数
"""判断Assignee"""
assignees = []
sumAsn = []
countAsn = []
countperprAsn = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0}      # 每个优先级条目数
"""判断标签"""
tags = []
sumTag = []
countTag = []
countperprTag = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0}       # 每个优先级条目数

for data in data_list:
    if data['Product'] not in products:
        products.append(data['Product'])
        sumPro.append(0)
        countPro.append(0)
    if data['Assignee'] not in assignees:
        assignees.append(data['Assignee'])
        sumAsn.append(0)
        countAsn.append(0)
    datatags = re.findall(r'\[(.*?)]', data['Summary'], re.S)
    for tag in datatags:
        if tag not in tags:
            tags.append(tag)
            sumTag.append(0)
            countTag.append(0)
        it = tags.index(tag)
        sumTag[it] += int(data['Priority'][1:])
        countTag[it] += 1
        countperprTag[data['Priority']] += 1

    ip = products.index(data['Product'])
    sumPro[ip] += int(data['Priority'][1:])     # 加上等级
    countPro[ip] += 1
    countperprPro[data['Priority']] += 1

    ia = assignees.index(data['Assignee'])
    sumAsn[ia] += int(data['Priority'][1:])
    countAsn[ia] += 1
    countperprAsn[data['Priority']] += 1

avgPro = []
avgAsn = []
avgTag = []
for i in range(len(products)):
    avgPro.append(sumPro[i] / countPro[i])

for i in range(len(assignees)):
    avgAsn.append(sumAsn[i] / countAsn[i])

for i in  range(len(tags)):
    avgTag.append(sumTag[i] / countTag[i])
print(products)
print(countPro)
print(avgPro)
print()
print(assignees)
print(countAsn)
print(avgAsn)
print()
print(tags)
print(countTag)
print(avgTag)
'''with open('products.txt', 'w', encoding='utf-8') as fpro:
    for i in range(len(products)):
        fpro.write(str(products[i]) + ' ')
        fpro.write(str(countPro[i]) + ' ')
        fpro.write(str(avgPro[i]) + '\n')
with open('assignees.txt', 'w', encoding='utf-8') as fasn:
    for i in range(len(assignees)):
        fasn.write(str(assignees[i]) + ' ')
        fasn.write(str(countAsn[i]) + ' ')
        fasn.write(str(avgAsn[i]) + '\n')
with open('tags.txt', 'w', encoding='utf-8') as ftag:
    for i in range(len(tags)):
        ftag.write(str(tags[i]) + ' ')
        ftag.write(str(countTag[i]) + ' ')
        ftag.write(str(avgTag[i]) + '\n')'''
# 方差。求方差以确定权值，方差越高权值越高：
def variance(avgs, counts):
    D = 0
    avgofavgs = sum(avgs) / len(avgs)
    countofcounts = sum(counts)
    j = 0
    for i in avgs:
        D += (i - avgofavgs) ** 2
        j += 1
    D /= len(avgs)
    return D
# 方差们
DPro = variance(avgPro, countPro)
DAsn = variance(avgAsn, countAsn)
DTag = variance(avgTag, countTag)

statuses = ['ASSI', 'NEW', 'REOP', 'UNCO']
avgStatus = [3.36523598092419, 3.0463403460549037, 3.054253181513731, 3.0191897654584223]
countStatus = [6081, 28377, 1493, 469]

comps = ['UI', 'Componen', 'Text', 'Launcher', 'Resource', 'Core', 'SWT', 'IDE', 'Debug', 'Doc', 'CVS', 'Compare', 'User Ass', 'cdt-core', 'Search', 'cdt-debu', 'Stellati', 'Ant', 'Compiler', 'GEF-Lega', 'Team', 'cdt-pars', 'Compendi', 'Releng', 'VE', 'Runtime', 'Docs', 'cdt-buil', 'CME', 'wst.wsi', 'cdt-refa', 'cdt-othe', 'Pollinat', 'Scriptin', 'wst.sse', 'wst.xml', 'jst.jsp', 'wst.xsd', 'cdt-coda', 'eSWT', 'website', 'Build', 'wst.comm', 'wst.wsdl', 'wst.dtd', 'wst.web', 'UI Guide', 'wst.html', 'Report', 'wst.inte', 'Report D', 'jst.ws', 'Bugzilla', 'Framewor', 'Report E', 'wst.ws', 'Jet', 'jst.j2ee', 'wst.vali', 'Data', 'Lepido', 'Report V', 'jst.serv', 'Edit', 'General', 'gmt', 'JSR220or', 'Tasks', 'XML', 'SQLDevTo', 'wst.serv', 'Faceted', 'Testing', 'Higgins', 'Examples', 'DD', 'Snippets', 'Website', 'Architec', 'simdebug', 'cdt-edit', 'JSF Tool', 'API', 'eWorkben', 'Laszlo', 'releng', 'JDBC Con', 'Data Sou', 'Chart', 'Data Acc', 'Document', 'LTWeavin', 'Java', 'JPA', 'Samples-', 'document', 'RSE', 'Tool', 'Incubato', 'Mozilla', 'p2', 'Server-S', 'Security', 'Trac', 'jst.ejb', 'APT', 'Connecti', 'ALF', 'Content', 'Terminal', 'Grid', 'Code Fol', 'Code For', 'OHF', 'bundles', 'Cosmos', 'maven-pl', 'Installe', 'Internal', 'cdt-sour', 'Geclipse', 'Ruby', 'API Tool', 'JavaScri', 'Monitor', 'AMW', 'Common', 'Web', 'Table Da', 'Jet Edit', 'SQL Quer', 'Transact', 'EMFT sea', 'SQL Edit', 'Project', 'Enableme', 'Debugger', 'Engine', 'Foundati', 'BPMN', 'SOC', 'Network', 'DataTool', 'cdo.net4', 'MWE', 'RWT', 'PHP Expl', 'Common-D', 'Albireo', 'wst.css', 'Mobile', 'Server', 'Gallery', 'Metamode', 'Tcl', 'Maynstal', 'STP', 'cdo.core', 'Process', 'Editor', 'wst.xsl', 'Python', 'Ruby-Deb', 'ecf.prov', 'ecf.disc', 'package', 'Corona', 'Composit', 'Weaving', 'Plugins', 'UMLX', 'SBVR', 'ecf.prot', 'Hibachi', 'e4', 'rcp-pack', 'IMP', 'EMFT.Ser', 'Samples', 'Accounts', 'JFace', 'MOXy', 'wtp.inc.', 'Emfatic', 'cpp-pack', 'WE', 'Buckmins', 'jee-pack', 'Cross-Pr', 'Workbenc', 'cdt-qt', 'cdo.ui', 'IDE4EDU', 'EIS', 'org.ecli', 'Utils', 'Nab', 'jst.jem', 'cdt-auto', 'DDL Gene', 'SQL Mode', 'Outline', 'IAM', 'Problems', 'EMF4Net', 'OFMP', 'Glimmer', 'cdt-memo', 'translat', 'Sequoyah', 'EclipseB', 'UFacekit', 'Dash Sub', 'SDO', 'design', 'jst.ws.j', 'navigati', 'OProfile', 'SQL Resu', 'ModelBas', 'Xpand', 'Code Ass', 'Transfor', 'ecf.core', 'cdt-doc', 'Validati', 'ecf.remo', 'Visualiz', 'gef3d', 'Valgrind', 'SWTBot', 'cdo.db', 'runtime', 'Language', 'ridget', 'Usage Da', 'Deployme', 'Desktop', 'E4', 'Photran.', 'SDK Mana', 'ecf.ui', 'Xtext Ba', 'Tools', 'Keyboard', 'incubato', 'wst.xpat', 'OSEE App', 'Handbook', 'Browser', 'Xtext', 'Sca', 'GanttCha', 'Call Gra', 'Escape', 'emfvm', 'Swordfis', 'cdt-rele', 'MDT.MST', 'Others', 'CBI p2 R', 'AMF', 'Pave', 'PaperCli', 'Targets', 'Forums a', 'Diagram', 'Tasks Co', 'JGit', 'SDK', 'RPM', 'Rta', 'User Int', 'Libhover', 'TMF.TCS', 'b3', 'cdt-inde', 'OSLC', 'GUI', 'wizard', 'Marketpl', 'unknown', 'build.sy', 'Infrastr', 'Mylyn', 'download', 'DB Defin', 'Technolo', 'Toolbox', 'OTDT', 'ecf.file', 'Sketch', 'Systemta', 'FoE Disb', 'GProf', 'RDT', 'JAXB', 'Action T', 'draw3d', 'php-pack', 'Template', 'cdo.lega', 'DBWS', 'cdo.dawn', 'Teneo', 'Analysis', 'C/C++', 'GEF DOT', 'Connecto', 'Integrat', 'WAR Prod', 'Install', 'OSEE Tes', 'GIT', 'ecf.rele', 'GCov', 'Debug UI', 'AJBrowse', 'PLDT', 'Hudson C', 'Dynamic', 'ui', 'ecf.doc', 'OTJ', 'Test', 'EMFIndex', 'Debug Co', 'Marte', 'Platform', 'Wikitext', 'Debug SD', 'AGF Char', 'IP Log T', 'snaps', 'Views', 'EPFWiki', 'tooling', 'Main', 'CVS Conn', 'Gerrit C', 'Gemini D', 'Units', 'Remote r', 'ETFw', 'Web Temp', 'linuxtoo', 'Packager', 'Library', 'EDT', 'RC', 'Release', 'Demo', 'ecf.serv', 'AMF UI', 'AXF', 'SysML', 'HtmlText', 'Experime', 'Client', 'Editors', 'AXF UI', 'Maven', 'OSGi Fac', 'Model', 'Query2', 'Look And', 'TPTP', 'OTEquino', 'java-pac', 'Git', 'Swing', 'M2x IDE', 'EMF Conn', 'Launch', 'Notifica', 'extensio', 'Servers', 'Backlog', 'modeling', 'Remote T', 'AGF', 'EPUB', 'virgo-bu', 'jdt', 'LTS', 'CDateTim', 'GMF Conn', 'Misc', 'RM', 'IPZilla', 'demo & e', 'artifact', 'Wiki', 'Formatte', 'Reqif-1.', 'Maven 3', 'DateChoo', 'Recommen', 'Yearly R', 'docs', 'Simulati', 'general', 'Bootstra', 'Disease', 'ecf.news', 'UA', 'gyrex', 'MailingL', 'LuaDevel', 'Xcore', 'MTJ proj', 'jetty', 'GEFBot', 'Git Conn', 'RDT.sync', 'Models', 'overlay', 'Oscillos', 'WWW', 'Designer', 'GitHub', 'Contribu', 'ManPage', 'web-admi', 'RCP', 'VJET', 'ProR', 'Query', 'build', 'prototyp', 'parallel', 'build he', 'Moka', 'Table', 'XSD', 'Generati', 'EclipseC', 'Agent', 'Discover', 'jsf', 'Stardust', 'Proposal', 'Tooling', 'Gerrit', 'TMF', 'Data Bin', 'perf', 'Location', 'SVN', 'Other', 'OTMvn', 'ReleaseE', 'Damos', 'Recorder', 'Featurem', 'Remote', 'Sonar', 'IoT', 'LTTng', 'JS Tools', 'AJDoc', 'Aether', 'Nexus Pl', 'Setup', 'Inject', 'cdt-gdb-', 'Target', 'GEF Layo', 'Nexus', 'HMI', 'Drivers', 'other', 'committe', 'MQTT-Lua', 'License', 'jBPM5 Ta', 'Paginati', 'MST', 'Scout SD', 'Paho', 'Scout', 'GEF Grap', 'EMS', 'C Revers', 'BlockDia', 'EMF Form', 'Flux', 'reportin', 'dsl-pack', 'Koneki', 'launchba', 'MDMWeb', 'State sy', 'ecf.tool', 'Automate', 'webtools', 'Automoti', 'GEF Zest', 'ECL', 'Refactor', 'Xtext Er', 'Errors', 'Help', 'Engines', 'ide-core', 'Diagrams', 'Version', 'Utilitie', 'RelEng', 'UserInte', 'codegen', 'UseCases', 'GEF Clou', 'Navigato', 'Targlets', 'Gitflow', 'Committe', 'Golo', 'Docker', 'examples', 'Target E', 'P2 Manag', 'Editor U', 'Californ', 'cdo.rele', 'Java Gen', 'GEF FX', 'test', 'tool', 'Scandium', 'DSL', 'DSE', 'cdt-ardu', 'Vagrant', 'Preferen', 'Target -', 'Modeling', 'SSH Slav', 'User', 'API.ecli', 'textual', 'PMC', 'MQTT-And', 'PapyrusR', 'p2 Repos', 'MQTT', 'signing-', 'FHIR', 'Charter', 'XY Graph', 'Paho.MQT', 'signing', 'ide', 'testing-', 'CI-Jenki', 'iOS', 'javascri', 'CDA', 'Collabor', 'Tinydtls', 'android-', 'Informat', 'GEF MVC', 'FORTE', 'Properti', 'Plug-ins', 'Web Stan', 'Composer', 'core', 'ide-temp', 'wst.json', 'My Accou', 'Articles', 'Obfuscat', 'Model Wo', 'Mattermo', 'Interope', 'Plexus', 'Tree', 'Node', 'Modules', 'Profilin', 'cdt-lsp', 'Toolsmit', 'IWG', '4DIAC-ID', 'vservers', 'ChangeLo', 'Converte', 'New Feat', 'Electron', 'CTF', 'editors', 'IDE Inte', 'XWT', 'Debug Ad', 'Glassfis', 'symbex', 'MXF.Edit', 'Query La', 'Interpre', 'eclipse-', 'R IDE', 'XViewer', 'Hosted S', 'AI', 'Robotics', 'Incubati', 'cdt-cmak', 'Protocol', 'Metalua', 'plugin-g', 'Vulnerab', 'Runner', 'license', 'OrionHub', 'Generato', 'Trace ty', 'Polarsys', 'Model2Do']
avgComp = [3.227978615071283, 3.0125, 3.3403880070546736, 2.993939393939394, 3.1166666666666667, 3.060083594566353, 3.018884120171674, 3.3590844062947065, 3.0396975425330814, 3.0583941605839415, 4.0, 3.0872817955112217, 3.048780487804878, 3.0033222591362128, 3.3, 3.0, 3.0, 2.9953917050691246, 3.43, 3.0, 3.175771971496437, 3.0, 3.0, 2.975, 2.943548387096774, 3.007843137254902, 3.2222222222222223, 2.997084548104956, 3.0, 2.9444444444444446, 3.0, 3.0, 3.0, 3.0, 2.953488372093023, 2.98019801980198, 2.9836065573770494, 2.9655172413793105, 3.0, 3.0, 3.0, 3.024, 2.9361702127659575, 3.0, 3.0, 2.7777777777777777, 3.0625, 3.0384615384615383, 3.2222222222222223, 3.0, 3.0833333333333335, 2.892857142857143, 3.0405405405405403, 2.9218241042345277, 3.044642857142857, 2.9615384615384617, 2.9166666666666665, 2.975206611570248, 3.0, 3.022222222222222, 3.0, 3.0697674418604652, 3.0, 3.0, 3.0077220077220077, 3.0, 3.0, 3.160839160839161, 3.5, 2.8333333333333335, 3.0, 2.9523809523809526, 3.5, 3.2857142857142856, 3.25, 3.0, 3.0, 2.992857142857143, 3.0294117647058822, 3.0, 3.0, 3.0, 3.5, 3.0, 2.875, 2.9767441860465116, 3.6666666666666665, 2.9, 3.05, 3.0, 2.977272727272727, 3.175, 3.2142857142857144, 2.687002652519894, 3.0, 3.0, 3.0246913580246915, 3.129032258064516, 2.990740740740741, 2.9166666666666665, 3.0019175455417066, 3.0, 3.0754716981132075, 3.4285714285714284, 3.0, 3.0416666666666665, 3.0, 3.25, 3.25, 2.980769230769231, 3.4545454545454546, 2.8, 2.789473684210526, 3.1818181818181817, 3.0, 2.869565217391304, 3.0, 3.0, 4.0, 3.0, 3.037037037037037, 2.75, 3.010869565217391, 3.0, 3.2, 3.0, 2.8974358974358974, 3.090909090909091, 3.0, 3.0, 3.0, 2.7777777777777777, 3.0, 3.0, 2.948905109489051, 3.0, 2.802197802197802, 3.0, 3.109004739336493, 3.0, 3.0, 3.0, 3.0, 3.2, 3.0, 2.983050847457627, 2.7, 3.0, 3.0, 3.0, 3.0, 3.0285714285714285, 1.6, 2.857142857142857, 3.0, 3.0, 3.0, 2.9878048780487805, 2.98, 2.723404255319149, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 1.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.6666666666666665, 3.0, 3.0, 3.176470588235294, 3.0, 3.0, 3.0, 3.0, 3.096774193548387, 3.0434782608695654, 3.0, 3.0, 3.0, 3.0128205128205128, 3.0, 2.9375, 3.1875, 3.0, 3.090909090909091, 3.0, 3.0, 3.0, 3.1, 3.0, 3.0, 3.0, 3.0, 3.0, 2.7142857142857144, 3.0, 2.5, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.875, 4.333333333333333, 3.0, 3.0, 2.8333333333333335, 3.0, 3.0, 3.0, 3.08, 2.789473684210526, 3.0, 3.0, 3.0, 2.857142857142857, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8181818181818183, 3.0, 3.0, 3.0, 3.3260869565217392, 2.6666666666666665, 3.0, 3.8, 2.8372093023255816, 3.0, 3.0, 3.0, 3.090909090909091, 2.9473684210526314, 3.0, 3.0481927710843375, 3.0, 3.0, 3.0, 2.8, 3.0, 3.0, 3.0, 3.0, 3.0136986301369864, 2.9545454545454546, 3.0, 2.0, 3.0, 3.0, 2.95, 3.0093457943925235, 3.0, 3.0, 3.0, 3.0, 2.3333333333333335, 3.0, 3.0, 3.0, 3.142857142857143, 3.0, 3.0, 3.0, 2.9523809523809526, 3.022222222222222, 3.0, 3.0, 4.318181818181818, 3.0, 3.0, 3.0, 4.5675675675675675, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.8333333333333335, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.6666666666666665, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 3.0, 3.0, 2.9696969696969697, 4.243243243243243, 3.0, 2.7884615384615383, 3.0, 4.5, 3.0, 2.0, 4.0, 3.0, 3.0, 3.0, 2.937007874015748, 2.942857142857143, 3.0, 3.0, 3.0, 3.0, 3.0, 3.017857142857143, 3.0, 3.0, 3.066666666666667, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.5, 3.0, 3.04, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.1, 2.3333333333333335, 3.0, 3.0, 2.9285714285714284, 3.0, 2.8333333333333335, 3.0, 3.0, 2.992481203007519, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 3.0, 3.0, 2.0, 3.0, 3.0, 2.9545454545454546, 3.0, 3.0, 3.0, 3.0, 3.0, 2.8823529411764706, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.9615384615384617, 3.25, 3.0, 3.0, 3.0, 3.0, 3.111111111111111, 3.0, 3.0, 3.25, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.870967741935484, 3.0, 3.0, 3.0, 2.6, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 5.0, 3.0, 3.125, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.290909090909091, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0784313725490198, 3.0, 3.0, 2.5, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.2222222222222223, 4.0, 3.0, 3.0, 3.0, 3.0, 3.3333333333333335, 3.0, 3.0, 3.3333333333333335, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0919540229885056, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.2857142857142856, 3.0, 3.0, 3.0, 3.0, 2.875, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.9545454545454546, 3.0, 3.0, 3.0, 3.0, 2.75, 3.0, 3.6666666666666665, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.2, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.6666666666666665, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
countComp = [7856,80,1134,165,360,3828,2330,699,1587,137,607,401,574,301,120,1301,13,217,200,119,421,73,81,440,124,255,9,343,7,18,74,50,3,16,43,101,61,58,42,8,10,125,47,63,4,18,32,26,36,2,72,56,222,307,112,26,12,121,22,45,2,43,77,11,777,13,1,143,2,12,88,21,4,7,24,5,8,140,68,10,100,36,2,2,8,86,3,10,40,20,44,40,14,754,29,15,324,31,108,12,1043,24,53,14,10,72,20,8,8,52,11,5,19,11,36,46,5,4,1,7,54,28,184,3,5,2,39,33,7,3,27,9,1,5,137,33,91,92,211,14,1,4,7,10,23,118,10,16,1,15,1,35,5,7,9,2,6,82,50,47,24,4,21,21,3,9,4,1,16,50,2,3,4,9,1,8,17,1,6,16,10,62,23,6,13,16,78,22,48,16,4,11,32,3,2,10,1,4,7,1,2,7,5,2,2,1,1,12,6,3,6,1,8,3,1,6,6,6,19,2,25,19,4,2,11,7,9,3,4,18,18,26,35,1,10,11,2,1,8,46,3,2,10,43,4,2,15,11,57,1,166,1,5,4,5,5,4,14,1,73,44,6,1,1,5,20,428,7,134,1,14,3,5,4,1,7,72,1,20,21,45,18,1,22,6,1,1,37,1,14,4,1,4,3,9,2,6,1,1,6,2,8,5,5,4,2,3,8,11,1,5,19,1,9,6,8,6,4,5,14,2,31,1,9,2,1,6,10,12,49,7,1,8,2,59,2,33,74,1,52,1,2,2,2,1,2,17,4,127,35,3,2,1,2,1,56,1,1,30,2,3,3,1,1,2,1,4,7,13,15,14,1,6,5,4,1,25,12,7,4,1,2,3,12,5,2,1,5,10,3,1,3,14,1,6,6,1,133,1,11,1,1,1,2,2,6,4,10,12,6,2,2,2,1,22,1,2,2,5,28,34,2,1,1,12,18,1,26,4,2,3,2,10,36,4,2,4,17,1,1,1,46,16,31,58,1,7,5,2,4,1,7,1,1,1,4,10,1,14,14,1,7,1,35,4,6,2,3,3,1,1,1,8,2,9,1,1,1,3,10,4,1,1,1,2,55,5,3,4,2,7,3,2,1,51,4,1,2,5,4,35,13,1,10,1,1,2,1,2,7,9,1,1,1,3,3,6,1,53,3,2,5,9,1,1,1,3,4,87,1,1,2,18,5,5,10,3,1,1,7,5,3,1,2,8,2,3,1,2,2,2,2,1,1,22,1,3,1,3,4,1,3,5,12,10,3,2,3,5,1,2,1,1,2,1,4,2,1,4,7,1,2,5,2,1,8,4,1,1,1,1,3,3,1,1,5,1,1,1,2,1,1,3,1,2,1,5,1,1,1,1,1,3,2,1,2,2,2,1,1]
DStatus = variance(avgStatus, countStatus)
DComp = variance(avgComp, countComp)

print(DPro)
print(DAsn)
print(DTag)
print(DStatus)
print(DComp)

