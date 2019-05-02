
import requests
from bs4 import BeautifulSoup
import csv
import time
from simdispider import settings



sec_url = 'https://book.douban.com/tag/小说'
print('[%s] 页面开始下载......' % (sec_url, ))
res = requests.get(sec_url)
html_obj = BeautifulSoup(res.text, 'html.parser')

li_list = html_obj.find_all('li', attrs = {'class': 'subject-item'})
book_list = []
for li in li_list:
    try:
        book = {}
        div_info = li.find("div", class_ = 'info')
        book_id = li.find('a').get('href').split('/')[-2]
        title = div_info.find('a').get('title')
        pub_info = div_info.find("div", class_ = 'pub').get_text().strip()
        score = div_info.find("span", class_ = 'rating_nums').get_text()
        summary = div_info.find('p').get_text()
        print(div_info)
        print('####################################################################')
        print('书籍ID为 ', book_id)
        print('标题是', title)
        print('基本信息是', pub_info)
        print('评分是', score)
        print('概述是', summary)
        print('####################################################################')
        book['id'] = book_id
        book['title'] = title
        book['pub'] = pub_info
        book['score'] = score
        book['summary'] = summary
        book_list.append(book)
    except:
        print('[加载错误!]跳过此书......')

filepath = settings.Download_Data_Path + '%s_file.csv'% (time.strftime('%m_%d_%H_%M', time.localtime()))
print(filepath)
with open(filepath, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    title = [k for k, v in book_list[0].items()]
    writer.writerow(title)
    try:
        for book_dict in book_list:
            info_list = [v for k, v in book_dict.items()]
            print(info_list)
            writer.writerow(info_list)
        print('文件存储完成......')
    except Exception as e:
        print(e)
        print('文件存储失败......')









