import sys
import os
MAIN_PATH = os.path.dirname(os.path.abspath((__file__)))

#新旧URL存储位置
NEW_URL_PATH = MAIN_PATH + '\\URL_Data\\new_url.txt'
OLD_URL_PATH = MAIN_PATH + '\\URL_Data\\old_url.txt'

#开始的URL
START_URL = 'http://book.douban.com'

#队列连接口令
MANAGER_AUTHKEY = 'WMmanager'

#文件下载位置
Download_Data_Path = MAIN_PATH + '\\Download_Data\\'

#爬取URL个数
NEED_URL_COUNTS = 200

