import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL



user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
class HtmlDownload(object):
    def __init__(self, user_agent = user_agent):
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}
    def download(self, url):
        if url:
            try:
                response = requests.get(url, headers = self.headers)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    return response.text
            except InvalidURL as e:
                print(e)
                print('[%s]页面跳过......'% url)

        return None

class HtmlResolv(object):

    def resolv(self, url, html_text):
        res = {}
        if url and html_text:
            html_obj = BeautifulSoup(html_text, 'html.parser')
            new_url = self.get_new_url(url, html_obj)
            new_data = self.get_new_data(url, html_obj)
            res['url'] = new_url
            res['data'] = new_data

        return res

    #提取URL和内容
    def get_new_url(self, url, html_obj):
        url_list = []
        a_list = html_obj.find_all('a')
        for a in a_list:
            url = a.get('href')
            if url:
                url_list.append(url)

        return url_list

    def get_new_data(self, url ,html_obj):
        res_list = []
        li_list = html_obj.find_all('li', attrs={'class': 'subject-item'})
        for li in li_list:
            try:
                book_dict = {}
                div_info = li.find("div", class_='info')
                id = li.find('a').get('href').split('/')[-2]
                title = div_info.find('a').get('title')
                pub_info = div_info.find("div", class_='pub').get_text().strip()
                score = div_info.find("span", class_='rating_nums').get_text()
                summary = div_info.find('p').get_text()
                # print(div_info)
                #             print('####################################################################')
                # print('标题是', title)
                # print('基本信息是', pub_info)
                # print('评分是', score)
                # print('概述是', summary)
                # print('####################################################################')
                book_dict['id'] = id
                book_dict['title'] = title
                book_dict['pub'] = pub_info
                book_dict['score'] = score
                book_dict['summary'] = summary
                res_list.append(book_dict)
            except:
                print('[加载错误!]跳过此书......')

        return res_list

