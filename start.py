from simdispider.controler.nodecontrol import NodeControl
from queue import Queue
from multiprocessing import Process
from threading import Thread
from simdispider import settings


if __name__ == '__main__':
    url_q = Queue()
    res_q = Queue()
    conn_q = Queue()
    save_q = Queue()
    node = NodeControl(url_q, res_q, conn_q, save_q)
    manager = node.start_manager()
    #创建三个线程
    url_pro = Thread(target = node.url_control_pro, args = (settings.START_URL,))
    get_com_pro = Thread(target = node.get_comment_pro)
    save_pro = Thread(target = node.save_pro)

    url_pro.start()
    get_com_pro.start()
    save_pro.start()
    manager.get_server().serve_forever()
    print('服务端关闭......')