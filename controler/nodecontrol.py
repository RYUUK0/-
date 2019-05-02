from simdispider.controler.datasave import DataSave
from simdispider.controler.urlcontrol import URLcontrol
from multiprocessing.managers import BaseManager
import time
from simdispider import settings as st


class NodeControl(object):
    def __init__(self, url_q, res_q, conn_q, save_q):
        """
            :param url_q:  URL管理 --> 爬虫
            :param res_q:  爬虫 --> 数据提取
            :param conn_q:  数据提取 --> URL管理
            :param save_q:  数据提取 --> 数据存储

        """
        self.url_q = url_q
        self.res_q = res_q
        self.conn_q = conn_q
        self.save_q = save_q

    def get_url_q(self):
        return self.url_q

    def get_res_q(self):
        return self.res_q



    #将URL和返回结果队列暴露给爬虫节点
    def start_manager(self):
        BaseManager.register('get_task_queue', callable = self.get_url_q)
        BaseManager.register('get_result_queue', callable = self.get_res_q)
        manager = BaseManager(address = ('', 8200), authkey = st.MANAGER_AUTHKEY.encode())

        return manager

    #URL管理进程
    def url_control_pro(self, start_url):
        print("URL管理程序启动......")
        urlcontrol = URLcontrol()
        urlcontrol.add_url(start_url)
        while True:
            while urlcontrol.have_new:
                new_url = urlcontrol.get_new_url()
                self.url_q.put(new_url)
                if urlcontrol.this_url_counts > st.NEED_URL_COUNTS:
                    print('已经爬取了%s个URL......'% st.NEED_URL_COUNTS)
                    urlcontrol.save_url()
                    self.url_q.put('end')
                    print("URL管理程序结束......")
                    return

            try:
                if not self.conn_q.empty():

                    new_urls = self.conn_q.get()
                    urlcontrol.add_all_urls(new_urls)

            except:
                print('等待数据提取URL......')
                time.sleep(0.5)

    #数据提取进程
    def get_comment_pro(self):
        print("数据提取程序启动......")
        while True:
            try:
                if not self.res_q.empty():
                    comment = self.res_q.get()
                    print('得到数据......')

                    if comment == 'end':
                        self.save_q.put('end')
                        print('通知存储进程结束......')
                        return
                    new_url = comment.get('url')
                    data = comment.get('data')
                    # print(new_url)
                    # print(data)
                    if new_url:
                        self.conn_q.put(new_url)
                    if data:
                        self.save_q.put(data)

            except:
                print('等待爬虫传输......')
                time.sleep(0.5)

    #数据存储过程
    def save_pro(self):
        print("数据存储程序启动......")
        data_control = DataSave()
        while True:
            try:
                data = self.save_q.get()
                if data == 'end':
                    print('存储进程结束......')
                    return
                data_control.write_data(data)

            except:
                print('等待数据传输......')
                time.sleep(0.5)


# if __name__ == '__main__':
#     url_q = Queue()
#     res_q = Queue()
#     conn_q = Queue()
#     save_q = Queue()
#     node = NodeControl(url_q, res_q, conn_q, save_q)
#     manager = node.start_manager()
#     #创建三个进程
#     url_pro = Process(target = node.url_control_pro, args = START_URL)
#     get_com_pro = Process(target = node.get_comment_pro)
#     save_pro = Process(target = node.save_pro)
#
#     url_pro.start()
#     get_com_pro.start()
#     save_pro.start()
#     manager.get_server().serve_forever()



