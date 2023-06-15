from lxml import etree
import matplotlib.pyplot as plt
import pandas as pd
import collections
from tqdm import tqdm

import os

# A1
# folder_path = '../../datasets/xmls/'
# # paths = ['../../datasets/xmls/STR_data.xml']
# xml_files = [x for x in os.listdir() if x.endswith(".xml")]
# sizeDownLimit = 3
# sizeUpLimit = 30

# root = etree.Element('benchmark')
# entry = etree.SubElement(root,'entries')

# l = -1

# for p in xml_files:
#     t = etree.parse(p)
#     r = t.getroot()
#     # array = r.xpath('//entry/@size')

#     for each in tqdm(r.xpath(f'//entry[@size>={sizeDownLimit} and @size<{sizeUpLimit}]')):
#         entry.append(each)

# tree = etree.ElementTree(root)  
# tree.write(os.path.join(folder_path, 'STR_text.xml'), pretty_print=True, xml_declaration=True, encoding='utf-8')


# A2
paths = ['./aylien_news_finance.xml']
sizeDownLimit = 3
sizeUpLimit = 30

root = etree.Element('benchmark')
entry = etree.SubElement(root,'entries')

l = -1

for p in paths:
    t = etree.parse(p)
    r = t.getroot()
    # array = r.xpath('//entry/@size')

    for each in tqdm(r.xpath(f'//entry[@size>={sizeDownLimit} and @size<{sizeUpLimit}]')):
        entry.append(each)

tree = etree.ElementTree(root)  
tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')

# b = collections.Counter(array)

# s = [[int(x),y] for x,y in b.items()]
# s.sort()
# print(s)
# plt.title = "统计数字出现的次数"

# # 转换成dataFrame的格式
# df = pd.DataFrame([each[1] for each in s], [each[0] for each in s])

# df.plot()
# plt.savefig('./test.png')
