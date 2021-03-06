#

from simdispider import settings as st
from simdispider.controler.log import logger
import hashlib
import json


class URLcontrol(object):
    def __init__(self):
        self.new_urls = self.get_file_comment(st.NEW_URL_PATH)
        self.old_urls = self.get_file_comment(st.OLD_URL_PATH)
        self.diode = False
        self.this_url_counts = 0

    #读取和保存URL文件
    def get_file_comment(self, path):
        logger.write_log(level = 'info', data = "正在加载文件......")
        try:
            with open(path, 'r') as x:
                comment = json.load(x)
                logger.write_log(level = 'info', data = "加载文件成功......")
                if isinstance(comment, list):
                    comment = set(comment)
                return comment
        except Exception as e:
            data = '[' + st.URL_NAME + ']' + str(e)
            logger.write_log(level = 'error', data = data)
        return set()

    def save_file_comment(self, path, data):
        mes = '[%s]保存中......' % path
        logger.write_log(level = 'info', data = mes)
        if isinstance(data, set):
            data = list(data)
        with open(path, 'w') as x:
            json.dump(data, x)
            logger.write_log(level = 'info', data = "文件保存完成......")

    def save_url(self):
        try:
            self.save_file_comment(st.NEW_URL_PATH, self.new_urls)
            self.save_file_comment(st.OLD_URL_PATH, self.old_urls)
        except Exception as f:
            data = '[' + st.URL_NAME + ']' + f
            logger.write_log(level = 'error', data = data)

    #添加单个URL和URL集合
    def add_url(self, url):
        if url:
            md5 = hashlib.md5()
            md5.update(url.encode())
            hash_url = md5.hexdigest()
            if url not in self.new_urls and hash_url not in self.old_urls:
                mes = "[%s]链接添加......" % url
                logger.write_log(level = 'run', data = mes)
                self.this_url_counts += 1
                self.new_urls.add(url)

    def add_all_urls(self, urls):
        if urls:
            for url in urls:
                if 'http' not in url:
                    url = 'https://book.douban.com' + url
                if 'book' in url:
                    self.add_url(url)

    def get_new_url(self):

        new_url = self.new_urls.pop()
        md5 = hashlib.md5()
        md5.update(new_url.encode())
        self.old_urls.add(md5.hexdigest())
        return new_url

    @property
    def new_urls_size(self):
        return len(self.new_urls)

    @property
    def old_urls_size(self):
        return len(self.old_urls)

    @property
    def have_new(self):
        if self.new_urls_size:
            return True
        return False

url_controler = URLcontrol()