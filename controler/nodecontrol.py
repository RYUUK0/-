from simdispider.controler.datasave import data_controler
from simdispider.controler.urlcontrol import url_controler
from multiprocessing.managers import BaseManager
from simdispider.controler.timecontrol import time_controler
from simdispider.controler.log import logger
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
        logger.write_log(level = 'info', data = "URL管理程序启动......")
        if not url_controler.have_new:
            url_controler.add_url(start_url)
        while True:
            #活跃模式(输出URL)
            if not url_controler.diode:
                while url_controler.have_new:
                    new_url = url_controler.get_new_url()
                    self.url_q.put(new_url)
                    if url_controler.this_url_counts > st.NEED_URL_COUNTS:
                        logger.write_log(level = 'info', data = '已经爬取了%s个URL......'% st.NEED_URL_COUNTS)
                        url_controler.diode = True
                        self.url_q.put('end')
                        logger.write_log(level = 'info', data = "URL管理程序进入休眠模式......")


            try:
                if not self.conn_q.empty():
                    new_urls = self.conn_q.get()
                    url_controler.add_all_urls(new_urls)
                    time_controler.reset_time(st.URL_NAME)
                else:
                    logger.write_log(level = 'info', data = '等待数据提取URL......')
                    time.sleep(1)
                    if time_controler.judge_timeout(st.URL_NAME):
                            url_controler.save_url()
                            logger.write_log(level = 'info', data = '退出URL管理程序......')
                            logger.save_all()
                            return
            except Exception as e:
                data = '[' + st.URL_NAME + ']' + e
                logger.write_log(level='error', data=data)
    #数据提取进程
    def get_comment_pro(self):
        logger.write_log(level='info', data='数据提取程序启动......')
        while True:
            try:
                if not self.res_q.empty():
                    comment = self.res_q.get()
                    logger.write_log(level = 'info', data = '得到数据......')
                    if comment == 'end':
                        self.save_q.put('end')
                        logger.write_log(level = 'info', data = '通知存储进程结束......')
                        return
                    new_url = comment.get('url')
                    data = comment.get('data')
                    if new_url:
                        self.conn_q.put(new_url)
                    if data:
                        self.save_q.put(data)
                    time_controler.reset_time(st.GET_NAME)
                else:
                    logger.write_log(level='info', data='等待爬虫传输......')
                    time.sleep(1)
                    if time_controler.judge_timeout(st.GET_NAME):
                        logger.write_log(level='info', data='退出数据提取程序......')
                        logger.save_all()
                        return

            except Exception as e:
                data = '[' + st.GET_NAME + ']' + e
                logger.write_log(level = 'error', data = data)


    #数据存储过程
    def save_pro(self):
        logger.write_log(level='info', data='数据存储程序启动......')
        while True:
            try:
                if not self.save_q.empty():
                    data = self.save_q.get()
                    time_controler.reset_time(st.SAVE_NAME)
                    if data == 'end':
                        data_controler.save()
                        logger.write_log(level='info', data='存储进程结束......')
                        return
                    data_controler.write_data(data)
                else:
                    logger.write_log(level='info', data='等待数据传输......')
                    time.sleep(1)
                    if time_controler.judge_timeout(st.SAVE_NAME):
                        logger.write_log(level='info', data='退出数据存储程序......')
                        logger.save_all()
                        return

            except Exception as e:
                data = '[' + st.SAVE_NAME + ']' + e
                logger.write_log(level = 'error', data = data)







