181860062 罗树汉

这一部分主要是对bug的部分属性的分析和最终排序结果的分析。

bugs.html是有1000个bug的html文件，还有一个allbugs.html是有三万多个bug的html文件，由于过大，这里没上传，魏宇阳同学应该上传至他的目录下了。

pachong.py是统计bug属性的爬虫，其中一部分是魏宇阳同学写的，我作了一点补充。

status&component.txt是对bugs的status和component属性的统计，每种属性分三行，分别是属性有哪些取值，每种取值的优先级平均值，以及每种取值的bug数目。

result2.csv是对三万多个bug排序后的结果。按列从左至右分别是原始数据下标，原始数据id，原始数据的得分（分越低越p1），bug的实际优先级，bug的预计优先级。

SRE_2.m是利用matlab对csv文件分析的代码。

結果1.docx是分析的结果，figure1--5.png是结果的可视化呈现。