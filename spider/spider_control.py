from simdispider.spider.htmldownload import HtmlDownload, HtmlResolv
from multiprocessing.managers import BaseManager
import time

print(HtmlDownload, HtmlResolv)


class Spider_Control(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        server_addr = '127.0.0.1'
        print('正在连接到 %s ......' % server_addr)
        self.m = BaseManager(address = (server_addr, 8200), authkey = 'WMmanager'.encode())
        self.m.connect()
        print('连接成功......')
        self.url_q = self.m.get_task_queue()
        self.result_q = self.m.get_result_queue()
        self.download = HtmlDownload()
        self.resolv = HtmlResolv()
        print('初始化完成......')

    def run(self):
        while True:

            if not self.url_q.empty():
                url = self.url_q.get()
                print(url)
                if url == 'end':
                    print('爬虫程序结束......')
                    self.result_q.put('end')
                    return None
                try:
                    html_text = self.download.download(url)
                    if html_text:
                        print('[%s] 页面下载成功......' % url)
                        res = self.resolv.resolv(url, html_text)
                        if res:
                            print('%s 页面解析成功......' % url)
                            self.result_q.put(res)
                        else:
                            print('%s 页面解析失败......' % url)

                    else:
                        print('%s 页面下载失败......' % url)
                except:
                    print('此URL连接失败......')

            else:
                print('等待传输URL.....')
                time.sleep(2)







